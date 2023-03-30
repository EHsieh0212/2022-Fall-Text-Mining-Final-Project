from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
from nltk.tokenize.treebank import TreebankWordDetokenizer
import pandas as pd
from ast import literal_eval

data = pd.read_csv("text/PiggyLo2_new_2.csv")
data2 = pd.read_csv("text/JayChou2_new_2.csv")
data3 = pd.read_csv("text/AllMalePrizedArtist_2.csv")
data4 = pd.concat([data, data2, data3], axis = 0)
print(len(data4['lyric_ckip']))


for i in range(data3.shape[0]):
    tmp = data3["lyric_ckip"].iat[i]
    tmp = literal_eval(tmp)
    data3["lyric_ckip"].iat[i] = tmp

for i in range(data.shape[0]):
    tmp = data["lyric_jieba"].iat[i]
    tmp = literal_eval(tmp)
    data["lyric_jieba"].iat[i] = tmp


corpus1 = list((data3['lyric_ckip']))
corpus2 = list((data['lyric_jieba']))


n = 2   #設定n-gram長度 (要以前多少個字計算字的機率)
data_train1, padded_sents1 = padded_everygram_pipeline(n, corpus1)   #前處理: pad句子 + 切割n-gram + pad n-gram + 將所有內容壓平為一段text
# data_train2, padded_sents2 = padded_everygram_pipeline(n, corpus2)

model1 = MLE(n) #建模
model1.fit(data_train1, padded_sents1)  #訓練mle model，計算n-gram機率

model2 = MLE(n) #建模
# model2.fit(data_train2, padded_sents2)  #訓練mle model，計算n-gram機率


detokenize = TreebankWordDetokenizer().detokenize

def generate_sent(model, num_words, text_seed, random_seed=42):   
    content = []
    n = 0
    for token in model.generate(num_words, text_seed=text_seed, random_seed=random_seed):   #根據random seed產出tokens，並將mle model產出的token list合併，通常以<s>為始</s>為後
        if token == '<s>':
            continue
        if token == '</s>':
            break
        content.append(token)
        n+=1
    return detokenize(content)
