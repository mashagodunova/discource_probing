import os
from conllu import parse
import pandas as pd
from time import time
start = time()
files= ["ru_pud-ud-test.conllu"]
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
        if df['num_non'][index] < 10:
            df = df.drop([index])
    # df = df.drop(0, axis=1)
    # df = df.drop(0, axis=1)
    df.to_csv(f'{lang}-next_pred.tsv')
print(df.columns)