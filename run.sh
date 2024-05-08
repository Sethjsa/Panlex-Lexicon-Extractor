!#/bin/bash

python /home/saycock/personal/data/panlex/Panlex-Lexicon-Extractor/panlex_bilingual_extract.py \
    --source_language $1 --target_language $2 \
    --output_directory /home/saycock/personal/data/panlex/updated/data/lexicons \
    --panlex_dir /home/saycock/personal/data/panlex/updated/data/ \
    --sql_database /home/saycock/personal/data/panlex/updated/data/panlex.db

# usage:
# bash run.sh spa eng