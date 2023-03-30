from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
from nltk.tokenize.treebank import TreebankWordDetokenizer
import pandas as pd
from ast import literal_eval


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

def predict(artist, length, gram, textSeed, seeding):
    print("start predicting")
    data = pd.read_csv(f"text/{artist}.csv")
    for i in range(data.shape[0]):
        tmp = data["lyric_ckip"].iat[i]
        tmp = literal_eval(tmp)
        data["lyric_ckip"].iat[i] = tmp
    corpus = list(data['lyric_ckip'])
    data_train, padded_sents = padded_everygram_pipeline(gram, corpus)
    model = MLE(gram)
    model.fit(data_train, padded_sents)
    result = "".join(generate_sent(model, num_words=length, text_seed = [f"{textSeed}"], random_seed=seeding).split(" "))
    return result
