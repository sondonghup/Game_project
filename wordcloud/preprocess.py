from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def preprocess(results):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(results)
    tfidf_weights = [(word, tfidf.getcol(idx).sum()) for word, idx in vectorizer.vocabulary_.items()]
    df = pd.DataFrame(tfidf_weights, columns = ['word', 'tfidf'])
    df = df.sort_values('tfidf', ascending=False)
    df = df.reset_index(drop=True)
    final = df.head(100)
    final_dict = final.set_index('word').to_dict()['tfidf']
    return final_dict