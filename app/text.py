import spacy

nlp = spacy.load("en_core_web_sm")

text = "I have experience in Python, SQL, FastAPI and Machine Learning."

doc = nlp(text)

for token in doc:
    print(token.text)