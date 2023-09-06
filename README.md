1. Requirements (Python 3)
 * json, re, os, string, itertools, nltk, Levenshtein, tqdm, csv

2. Dir Tree
``` sh
|-datasets
    |-Y_Moniter
    |-Y_Moniter_labels.csv
|-brands
    |-Brands_Moniter.json
    |-Brands_Notebook.json
    |-Brands_Camara
|-codes
    |-entity_resolution.py
    |-preprocess.py
    |-tokenizer.py
    |-block_scheme.py
    |-block_clustering.py
    |-profile_similarity.py
    |-(submission.csv)
    |-measure.py
|-readme.txt
```
3. Run 'entity_resolution.py' (the example in dataset Y_Moniter)
This script will load the dataset, match these productions, and generate the file named 'submission.csv'. This submission.csv contains the matches in the dataset.

4. This work is based on the 'JNU_Cybers' team in the following competitions:
 * ACM SIGMOD 2020: http://www.inf.uniroma3.it/db/sigmod2020contest/leaders.html
 * DI2KG: http://di2kg.inf.uniroma3.it/2020/leaderboard.html
