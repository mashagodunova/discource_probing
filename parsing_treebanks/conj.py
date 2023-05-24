import os
import pandas as pd
from time import time
start = time()
import random
import numpy as np
import csv
files= ["ru_pud-ud-test.conllu",'bg_btb-ud-train.conllu.txt','ca_ancora-ud-dev.conllu.txt',
        'en_ewt-ud-dev.conllu.txt', 'fr_pud-ud-test.conllu.txt','hyw_armtdp-ud-train.conllu.txt',
        'la_perseus-ud-test.conllu.txt', 'tr_pud-ud-test.conllu.txt', 'cs_fictree-ud-test.conllu.txt',
        'sr_set-ud-test.conllu.txt']
#del ml sv
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
    print(records[0])
    df = pd.DataFrame(records, columns=['SENT_NO', 'TEXT', 'CONJ'])
    df = df.drop_duplicates().reset_index()
    result = []
    for index in range(len(df)):
        if df['CONJ'].loc[index] is not None and index-1 in df['TEXT'].index:
            result.append(df['TEXT'].loc[index-1])
        else:
            result.append('')
    df['PRECEDING']=result
    for index, row in df.iterrows():
        if df.loc[index,'CONJ'] is None :
            df = df.drop(index=[index])
    df['TEXT'] = df['TEXT'].apply(lambda x: x.split()[1:])
    df['TEXT'] = df['TEXT'].str.join(" ")
    df_true = df.reset_index().loc[0:len(df) // 2, :]
    df_false = df.reset_index().loc[(len(df) // 2) + 1:len(df), :]
    df_true['answer'] = 1
    df_false['answer'] = 0
    with open(f'{lang}-output.csv', 'w', encoding="utf-8") as newf:
        my_writer = csv.writer(newf, delimiter="\t", lineterminator="\n")
        for index, row in df_true.iterrows():
            my_writer.writerow([row['PRECEDING'], row['TEXT'], row['CONJ'], row['answer']])
        for index, row in df_false.iterrows():
            my_writer.writerow([row['PRECEDING'], row['TEXT'], row['CONJ'], row['answer']])
    columns = ['sent_1', 'sent_2','conj', 'answer']
    new_df = pd.read_csv(f'{lang}-output.csv', delimiter="\t", lineterminator="\n", names=columns)
    n_df = new_df.sample(frac=1).reset_index()
    n_df['index'] = new_df.reset_index()['index']
    n_df['tr_te'] = 0
    for index in n_df.index:
        if n_df.loc[index, 'index'] in range(int(0.8 * len(n_df))):
            n_df.loc[index, 'tr_te'] = 'tr'
        if n_df.loc[index, 'index'] not in range(int(0.8 * len(n_df))):
            n_df.loc[index, 'tr_te'] = 'te'
    n_df = n_df.drop('index', axis=1)
    with open(f'{lang}-output.csv', 'w', encoding="utf-8") as newf:
        my_writer = csv.writer(newf, delimiter="\t", lineterminator="\n")
        for index, row in n_df.iterrows():
            my_writer.writerow([row['answer'], row['tr_te'], row['sent_1'], row['sent_2'], row['conj']])
# # смешать, разделить, записать
