# Panlex-Lexicon-Extractor
The script is a tool to extract bilingual lexicon for pair of languages from the [Panlex Database](https://db.panlex.org/) released by [Panlex](https://panlex.org/).
# Extracted Lexicons (English-{target})
Extracted lexicons for all languages are available in data/lexicons
# Usage
The code is written in Python 3.7

[Download](https://drive.google.com/file/d/1tyACWPYrOQJ4m20dTjDPWtpX1XGYWtyf/view?usp=sharing) the required file of Panlex language information. Put the downloaded file under the folder of 'data'

[Download](https://db.panlex.org/panlex_lite-20240401.zip) and unzip the SQLite file of Panlex database, put the panlex.db under the folder of 'data'

The script accepts 3-digit [ISO 639-3](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) language codes.
```
# extract one lexicon
tgt_lang="xxx"
python panlex_bilingual_extract.py --source_language="eng" --target_language="${tgt_lang}" \
        --output_directory="data/lexicons" \
        --panlex_dir="data/" \
        --sql_database="data/panlex.db"

# extract all lexicons
python extract_all.py 
  --source_language="eng" --target_language="eng"
  --output_directory="data/lexicons"
  --panlex_dir="data/"
  --sql_database="data/panlex.db"
```

# Citation
If you find the lexicon extractor useful, please cite the following paper: [Embracing non-traditional linguistic resources for low-resource language name tagging](http://www.aclweb.org/anthology/I17-1037)
```
@inproceedings{zhang2017embracing,
  title={Embracing non-traditional linguistic resources for low-resource language name tagging},
  author={Zhang, Boliang and Lu, Di and Pan, Xiaoman and Lin, Ying and Abudukelimu, Halidanmu and Ji, Heng and Knight, Kevin},
  booktitle={Proceedings of the Eighth International Joint Conference on Natural Language Processing (Volume 1: Long Papers)},
  volume={1},
  pages={362--372},
  year={2017}
}
```
Contact: Di Lu, lud2@rpi.edu
