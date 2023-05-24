import torch
import tensorflow as tf
import transformers
import numpy as np
from transformers import BertTokenizer, BertModel, AutoTokenizer, AutoModelForMaskedLM, GPT2Tokenizer, GPT2Model, MT5Model, T5Tokenizer
import sklearn
from transformers import BertForSequenceClassification
import pandas as pd
from sklearn.linear_model import LogisticRegression
import json
def acc(file, tokenizer_name, model_name):
    train = pd.read_csv(file, delimiter="\t", lineterminator="\n")
    train = train.rename(columns={train.columns[0]: 'answer', train.columns[1]: 'tr_te',
                              train.columns[2]: 'sent_1',train.columns[3]: 'sent_2',
                              train.columns[4]: 'sent_3', train.columns[5]: 'sent_4', train.columns[6]: 'sent_5',
                              train.columns[7]: 'sent_6'})
    train = train.fillna('.')
    train_tr = train[train['tr_te']=='tr']
    train_te = train[train['tr_te']=='te']
    tokenizer = tokenizer_name
    model = model_name
    labels1 = train_tr['answer']
    texts1 = (train_tr['sent_1'].map(str) +
                    '.'+ train_tr['sent_2'].map(str) + '.'+ train_tr['sent_3'].map(str) + '.'+ train_tr['sent_4'].map(str)
                    + '.'+ train_tr['sent_5'].map(str)+ '.'+ train_tr['sent_6'].map(str))
    tokenized1 = texts1.apply((lambda x: tokenizer.encode(x, add_special_tokens=True, max_length=50)))
    max_len1 = 0
    for i in tokenized1.values:
        if len(i) > max_len1:
            max_len1 = len(i)

    padded1 = np.array([i + [0]*(max_len1-len(i)) for i in tokenized1.values])
    attention_mask1 = np.where(padded1 != 0, 1, 0)
    input_ids1 = torch.tensor(padded1)
    attention_mask1 = torch.tensor(attention_mask1)
    #decoder_input_ids, input_ids
    with torch.no_grad():
        last_hidden_states1 = model(decoder_input_ids=input_ids1,
                                    input_ids=input_ids1,
                                    attention_mask=attention_mask1)
    features1 = last_hidden_states1[0][:,0,:].numpy()
    labels2 = train_te['answer']
    texts2 = (train_te['sent_1'].map(str) +
                    '.'+ train_te['sent_2'].map(str)+
                    '.'+ train_te['sent_3'].map(str)+
                    '.'+ train_te['sent_4'].map(str)+
                    '.'+ train_te['sent_5'].map(str)+
                    '.'+ train_te['sent_6'].map(str))
    tokenized2 = texts2.apply((lambda x: tokenizer.encode(x, add_special_tokens=True, max_length=50)))
    max_len2 = 0
    for i in tokenized2.values:
        if len(i) > max_len2:
            max_len2 = len(i)

    padded2 = np.array([i + [0]*(max_len2-len(i)) for i in tokenized2.values])
    attention_mask2 = np.where(padded2 != 0, 1, 0)
    input_ids2 = torch.tensor(padded2)
    attention_mask2 = torch.tensor(attention_mask2)
    #decoder_input_ids, input_ids
    with torch.no_grad():
        last_hidden_states2 = model(decoder_input_ids=input_ids2,
                                    input_ids=input_ids2, attention_mask=attention_mask2)
    features2 = last_hidden_states2[0][:,0,:].numpy()
    logreg = sklearn.linear_model.LogisticRegression(
    solver='liblinear')
# There is a bug with solver='lbfgs'
# AttributeError: 'str' object has no attribute 'decode'
# in fitting Logistic Regression Model

    logreg.fit(features1, labels1)
    score = logreg.score(features2, labels2)
    score = round(score, 5)
    return score

files = ['/content/bg-disco_coh.csv','ca-disco_coh.csv',
         '/content/en-disco_coh.csv','/content/fr-disco_coh.csv',
         '/content/hyw-disco_coh.csv','/content/la-disco_coh.csv',
          '/content/ru-disco_coh.csv', '/content/cs-disco_coh.csv',
         '/content/tr-disco_coh.csv','/content/sr-disco_coh.csv']


#langs = ['Bulgarian','Catalan','English','French','Armenian','Latin','Russian','Czech','Turkish','Serbian']
mod_names = ['bert','roberta','gpt-2']
model_token = [[BertTokenizer.from_pretrained('bert-base-multilingual-cased'),
                 BertModel.from_pretrained("bert-base-multilingual-cased")],
               [AutoTokenizer.from_pretrained('xlm-roberta-base'),
                AutoModelForMaskedLM.from_pretrained("xlm-roberta-base")],
               [GPT2Tokenizer.from_pretrained('gpt2'),
                GPT2Model.from_pretrained('gpt2')],
               [T5Tokenizer.from_pretrained("google/mt5-small"),
               MT5Model.from_pretrained("google/mt5-small")]]
dc = {}
c_d={}
for i, mod_name in zip(model_token,mod_names):
    for file,name in zip(files,langs):
        c_d[name] = acc(file,i[0],i[1])
    dc[mod_name]=c_d
with open('result.json', 'a') as fp:
    json.dump(dc,fp)
    fp.write('\n')

# fin_dc = {}
# slovik = []
# for line in open('result.json', 'r'):
#     slovik.append(line)
# fin_dc['binary_sentence_ordering']=slovik
# with open('/content/final.json', 'a') as fp:
#     json.dump(fin_dc,fp)