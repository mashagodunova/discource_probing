import os
from conllu import parse
import pandas as pd
from time import time
import csv
import numpy as np
start = time()

files= ["ru_pud-ud-test.conllu",'bg_btb-ud-train.conllu.txt','ca_ancora-ud-dev.conllu.txt',
        'en_ewt-ud-dev.conllu.txt', 'fr_pud-ud-test.conllu.txt','hyw_armtdp-ud-train.conllu.txt',
        'la_perseus-ud-test.conllu.txt', 'tr_pud-ud-test.conllu.txt', 'cs_fictree-ud-test.conllu.txt',
        'sr_set-ud-test.conllu.txt']
for file_path in files:
    full=[]
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
                    elif 'text' in line[0] and 'english_text' not in line[0] and 'text_en' not in line[0]:
                        text = line[1].strip()
                        records.append([doc_id, sent_id, text])
    # full.append(records)
    for i in records:
        for d in records:
            if i[0]==d[0]:
                if i[-2:] < d[-2:]:
                    i[2]+=f' {d[2]}'
                    records.remove(d)
                elif i[-2:] > d[-2:]:
                    d[2] += f' {i[2]}'
                    if i in records:
                        records.remove(i)
    end = time()
    print("Time elapsed:", end-start, "seconds")
    df = pd.DataFrame(records, columns=['DOC_NO', 'SENT_NO', 'TEXT'])
    df = df.drop_duplicates()
    punct = ['.']
    # for item in punct:
    #     for count, elem in enumerate(df['TEXT'][0].split(item)):
    #         if len(df['TEXT'][0].split(item)) >=2:
    #             list = []
    #             list_f'{count}'.append(elem)
    #             df[count] = list_f'{count}'
    new_df = df.TEXT.str.split('.', expand=True)
    new_df = new_df.reset_index(drop=True)
    # df.rename(columns={'DOC_NO':'DOC_NO', 'SENT_NO':'SENT_NO', 'TEXT':'TEXT'})
    # new_df.rename(columns={"A": "a", "B": "c"})
    df = df.join(new_df)
    df['num_non'] = df.notna().sum(axis=1)
    for index in df.index:
        if df['num_non'][index] < 9:
            df = df.drop([index])
    # df = df.drop(0, axis=1)
    # df = df.drop(0, axis=1)
    #df.to_csv(f'{lang}-cloze_test.tsv')
    df_true = df.reset_index().loc[0:len(df) // 2, :]
    df_false = df.reset_index().loc[(len(df) // 2) + 1:len(df), :]
    df_true['answer'] = 1
    df_false['answer'] = 0
    print(df_false.columns)
   #df_false.iloc[:, 7:11] = df_false.iloc[:, 7:11].sample(frac=1).reset_index(drop=True)
    with open(f'{lang}-cloze_test.csv', 'w', encoding="utf-8") as newf:
        my_writer = csv.writer(newf, delimiter="\t", lineterminator="\n")
        df_false1= pd.DataFrame(df_false.iloc[:, [4,5,6,7,8,-1]])
        df_false1[4] = np.random.permutation(df_false1[4].values)
        for index, row in df_false1.iterrows():
            my_writer.writerow([row[0], row[1], row[2], row[3],row[4], row['answer']])
        for index,row in df_false.iterrows():
            if df_false[5] is not None:
                df_false2= pd.DataFrame(df_false.iloc[:, [5,6,7,8,9,-1]])
                df_false2[5] = np.random.permutation(df_false2[5].values)
                for index, row in df_false2.iterrows():
                    if row[5] is not None:
                        my_writer.writerow([row[1], row[2], row[3], row[4],row[5], row['answer']])
        for index,row in df_false.iterrows():
            if df_false[6] is not None:
                df_false3= pd.DataFrame(df_false.iloc[:, [6,7,8,9,10,-1]])
                df_false3[6] = np.random.permutation(df_false3[6].values)
                for index, row in df_false3.iterrows():
                    if row[6] is not None:
                        my_writer.writerow([row[2], row[3], row[4],row[5],row[6], row['answer']])
        for index,row in df_false.iterrows():
            if df_false[7] is not None:
                df_false4= pd.DataFrame(df_false.iloc[:, [7,8,9,10,11,-1]])
                df_false4[7] = np.random.permutation(df_false4[7].values)
                for index, row in df_false4.iterrows():
                    if row[7] is not None:
                        my_writer.writerow([row[3], row[4],row[5],row[6], row[7], row['answer']])
        # for index,row in df_false.iterrows():
        #     if df_false[8] is not None:
        #         df_false5= pd.DataFrame(df_false.iloc[:, [8,9,10,11,12,-1]])
        #         df_false5[8] = np.random.permutation(df_false5[8].values)
        #         for index, row in df_false5.iterrows():
        #             if row[8] is not None:
        #                 my_writer.writerow([row[4],row[5],row[6], row[7], row[8],row['answer']])
        for index, row in df_true.iterrows():
            my_writer.writerow([row[0], row[1], row[2], row[3], row[4], row['answer']])
        for index, row in df_true.iterrows():
            my_writer.writerow([ row[1], row[2], row[3], row[4], row[5],row['answer']])
        for index, row in df_true.iterrows():
            my_writer.writerow([row[2], row[3], row[4],row[5],row[6], row['answer']])
        for index, row in df_true.iterrows():
            my_writer.writerow([row[3], row[4],row[5],row[6],row[7], row['answer']])
        # for index, row in df_true.iterrows():
        #     my_writer.writerow([row[4],row[5],row[6],row[7],row[8],row['answer']])

    columns = ['sent_1', 'sent_2', 'sent_3', 'sent_4', 'sent_5','answer']
    new_df = pd.read_csv(f'{lang}-cloze_test.csv', delimiter="\t", lineterminator="\n", names=columns)
    n_df = new_df.sample(frac=1).reset_index()
    n_df['index'] = new_df.reset_index()['index']
    n_df['tr_te'] = 0
    for index in n_df.index:
        if n_df.loc[index, 'index'] in range(int(0.8 * len(n_df))):
            n_df.loc[index, 'tr_te'] = 'tr'
        if n_df.loc[index, 'index'] not in range(int(0.8 * len(n_df))):
            n_df.loc[index, 'tr_te'] = 'te'
    n_df = n_df.drop('index', axis=1)
    with open(f'{lang}-cloze_test.csv', 'w', encoding="utf-8") as newf:
        my_writer = csv.writer(newf, delimiter="\t", lineterminator="\n")
        for index, row in n_df.iterrows():
            my_writer.writerow(
                [row['answer'], row['tr_te'], row['sent_1'], row['sent_2'], row['sent_3'], row['sent_4'], row['sent_5']])

#print(df_false.iloc[:, [4,5,6,7,8,14]].columns)
