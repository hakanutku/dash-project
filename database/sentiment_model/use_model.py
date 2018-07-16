import pickle
import pandas as pd

model_pickle_path = "C:\\Users\\HAKAN.OZDEMIR\\Desktop\\dash-project\\database\\sentiment_model\\model.pickle"
vectorizer_pickle_path = "C:\\Users\\HAKAN.OZDEMIR\\Desktop\\dash-project\\database\\sentiment_model\\vectorizer.pickle"

with open(model_pickle_path, "rb") as pickle_in:
    model = pickle.load(pickle_in)

with open(vectorizer_pickle_path, "rb") as pickle_in:
    vect = pickle.load(pickle_in)


def predict(raw_text):
    vector = vect.transform(raw_text)
    return [i[1] for i in model.predict_proba(vector)]
