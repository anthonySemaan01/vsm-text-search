import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


def clean_text(text):
    wnl = WordNetLemmatizer()
    ps = PorterStemmer()

    text = text.lower()
    tokens = word_tokenize(text)

    words = [word for word in tokens if word.isalnum()]

    stop_words = set(stopwords.words('english'))

    words = [w for w in words if w not in stop_words]
    lemmatized = [wnl.lemmatize(word) for word in words]
    stemmed = [ps.stem(word) for word in lemmatized]

    return " ".join(stemmed)
