import os
import pandas as pd
from time import time
start = time()
files= ["ru_pud-ud-test.conllu","en_ewt-ud-dev.conllu.txt", "ca_ancora-ud-dev.conllu.txt"]
for file_path in files:
    lang = str(file_path).split('-')[0].split('_')[0]
    with open(file_path, 'r', encoding='utf-8') as file:
        mylist = [line.rstrip('\n') for line in file]
        file_prefix = file_path.split('.')[0] + '_'
        doc_id = ''
        sent_id = ''
        records = list()
        for i in range(len(mylist)):
            if len(mylist[i]) > 1 :
                if mylist[i][0] == '#':
                    line = mylist[i].split('=')
                    if 'newdoc' in line[0]:
                        doc_id = file_prefix + line[1].strip()
                    elif 'sent_id' in line[0]:
                        sent_id = line[1].strip()
                    elif 'text' in line[0] and 'english_text' not in line[0]:
                        text = line[1].strip()
                else:
                    info = mylist[i].split('\t')
                    if len(info) == 10:
                        if info[0]=="1" and (info[3]=='CCONJ' or info[3]=='SCONJ'):
                            records.append([sent_id, text] + [info[1]])
                        else:
                            records.append([sent_id, text])
    for i in records:
        for d in records:
            if i[1]==d[1]:
                if len(i)>len(d) and i in records:
                    records.remove(d)
                if len(d)>len(i) and d in records:
                    records.remove(i)
    end = time()
    print("Time elapsed:", end-start, "seconds")
    df = pd.DataFrame(records, columns=['SENT_NO', 'TEXT', 'CONJ'])
    df = df.drop_duplicates().reset_index()
    result = []
    for index in range(len(df)):
        if df['CONJ'].loc[index] is not None:
            result.append(df['TEXT'].loc[index-1])
        else:
            result.append('')
    df['PRECEDING']=result
    df.to_csv(f'{lang}-output.tsv')
print(df.head())