1.Environment Requirement:
 json,re,os,string,itertools,nltk,Levenshtein,tqdm,csv

2.dir tree
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

3. run 'entity_resolution.py' (the example in dataset Y_Moniter)
This script will load the dataset, match these productions and generate the file named 'submission.csv'. This submission.csv contains the matches in the dataset.

4. this work is based on the 'JNU_Cybers' team, the url of competition result:
ACM SIGMOD 2020: http://www.inf.uniroma3.it/db/sigmod2020contest/leaders.html
DI2KG: http://di2kg.inf.uniroma3.it/2020/leaderboard.html
