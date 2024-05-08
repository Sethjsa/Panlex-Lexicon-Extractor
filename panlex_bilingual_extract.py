#author: Di Lu
# updated by: Seth Aycock
# -*- coding: utf-8 -*-                                                                                                  
import argparse
import sqlite3 as lite
import xml.etree.ElementTree as ET
import os
import tqdm
import json
def langid_extract(source_language, target_language, panlex_dir):
	source_langid = None
	target_langid = None
	wiktionary_file= os.path.join(panlex_dir, 'langvar.json')
	with open(wiktionary_file) as f:
		lines = f.read()
	json_lines = json.loads(lines)
	for line in json_lines:
		if line['lang_code'] == source_language and line['var_code'] == 0:
			source_langid = str(line['id'])
		if line['lang_code'] == target_language and line['var_code'] == 0:
			target_langid = str(line['id'])
	return source_langid, target_langid


def extract_bilingual_lexicon(source_language, target_language, source_langid, target_langid, output_directory, sql_database):
	con = lite.connect(sql_database, timeout=10)
	with con:
		print('loading expression file')
		src = {}
		tgt = {}
		expr_dic = {}
		mention_dic = {}	
		cur = con.cursor()

		print("executing query")

		# old panlex (2017) - 
		# cur.execute("""
		# 	SELECT e.ExprID, e.langvar, e.txt, d.meaning 
		# 	FROM (
		# 		SELECT * FROM Exprs WHERE langvar = ? OR langvar = ?
		# 	) e 
		# 	JOIN Denotations d ON e.ExprID = d.expr
		# 	""", (target_langid,source_langid))

		# new panlex (updated, 2024) 
		cur.execute("""
		SELECT e.ex, e.lv, e.tt, d.mn
		FROM (
			SELECT * FROM ex WHERE lv = ? OR lv = ?
		) e 
		JOIN (SELECT * FROM dnx WHERE lv = ? OR lv = ?) d ON e.ex = d.ex
		""", (target_langid,source_langid,target_langid, source_langid))

		print("fetching rows")
		rows = cur.fetchall()
		print(len(rows))

		# uncomment to save rows to a file - avoids fetching each time
		# with open('data/exprs_denotations.txt', 'w') as f:
		# 	for row in rows:
		# 		f.write(f"{row}\n")

		# meanings = {}

		for row in tqdm.tqdm(rows):
			# with new panlex  meaning_expr
			expr_id, langvar, txt, meaning_id  = row

			# for debugging
			# if meaning_id not in meanings:
			# 	meanings[meaning_id] = []
			# meanings[meaning_id].append(row)

			if row == rows[0]:
				print(f"expr_id: {expr_id}, langvar: {langvar}, txt: {txt}, meaning_id: {meaning_id}")
			expr_dic[expr_id] = txt

			if int(langvar) == int(source_langid):
				src[expr_id] = txt
			elif int(langvar) == int(target_langid):
				tgt[expr_id] = txt

			if meaning_id not in mention_dic:
				mention_dic[meaning_id] = [None, None]

			if int(langvar) == int(source_langid):
				mention_dic[meaning_id][0] = expr_id
			elif int(langvar) == int(target_langid):
				mention_dic[meaning_id][1] = expr_id

	print('writing to output file')
	output_file_path = os.path.join(output_directory, f"{source_language}-{target_language}.txt")
	written = set()
	with open(output_file_path, 'w') as f_out:
		mm = 0
		for meaning_id, (source_expr, target_expr) in mention_dic.items():
			if source_expr and target_expr:
				pair = (source_expr, target_expr)
				if pair not in written:
					f_out.write(f"{src[source_expr]}\t{tgt[target_expr]}\n")
					mm += 1
					written.add(pair)
	print(f"Processed {mm} pairs.")
		

if __name__=="__main__":
		parser = argparse.ArgumentParser(description='Extracting bi-lingual lexicion from Panlex')
		parser.add_argument('--source_language', default='', help='identify the 3-digit language code for source language')
		parser.add_argument('--target_language', default='eng', help='identify the 3-digit language code for target language')
		parser.add_argument('--output_directory', default='data/lexicons/', help='identify the path of the folder to save the extracted lexicon')
		parser.add_argument('--panlex_dir', default='data/', help='path of folder for original Panlex json files')
		parser.add_argument('--sql_database', default='data/panlex.db', help='path of processed sqlite database of panlex')
		args = parser.parse_args()
		if not os.path.exists(args.output_directory):
				os.mkdir(args.output_directory)

		# retrive the language variantion code from panlex database
		source_langid,target_langid = langid_extract(args.source_language, args.target_language, args.panlex_dir)
		if source_langid == None:
				print("Error: incorrect source language code")
		if target_langid == None:
				print("Error: incorrect target language code")
		else:
				assert source_langid != None and target_langid != None
				print("Extracting %s_%s -- %s_%s lexicon"%(args.source_language, source_langid, args.target_language, target_langid))

				extract_bilingual_lexicon(args.source_language, args.target_language, source_langid, target_langid, args.output_directory, args.sql_database)
		print("Extraction completed")
