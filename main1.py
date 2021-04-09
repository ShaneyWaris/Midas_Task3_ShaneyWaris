from num2words import num2words
import nltk
nltk.download('brown')
nltk.download('names')
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re, joblib
from normalise import normalise
from sklearn.feature_extraction.text import TfidfVectorizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

clf = joblib.load('./model/TfidfVectorizer__MLPClassifier.pkl')
vocab = joblib.load('./vocab.pkl')
d = {
    0: 'Clothing',
    1: 'Furniture',
    2: 'Footwear',
    3: 'Pet',
    4: 'Pens',
    5: 'Sports',
    6: 'Beauty',
    7: 'Bags',
    8: 'Home',
    9: 'Automotive',
    10: 'Tools',
    11: 'Baby',
    12: 'Mobiles',
    13: 'Watches',
    14: 'Toys',
    15: 'Jewellery',
    16: 'Sunglasses',
    17: 'Kitchen',
    18: 'Computers',
    19: 'Cameras',
    20: 'Health',
    21: 'Gaming',
    22: 'Olvin',
    23: 'Clovia',
    24: 'Eyewear',
    25: 'eBooks'
}

def removeLen1words_num2words(text):
    new_text = []
    for word in text.split():
        if word.isnumeric():
            try:
                new_text.append(num2words(word))
            except:
                continue
        else:
            new_text.append(word)

    text = " ".join(new_text)
    text = " ".join([word for word in text.split() if len(word) > 1])
    return text

def PreProcessing(text):
    # Lower-case
    text = str(text).lower()
    
    text = removeLen1words_num2words(text)

    # Remove Stopwords.
    word_tokens = word_tokenize(text)
    text = " ".join([w for w in word_tokens if not w in stop_words])
    
    # Remove urls.
    text = re.sub(r"(http\S+)|(www\S+)|(\w*.com\b)", " ", str(text))

    # Remove Punctuations.
    text = re.sub(r'[+*|/\\\-?.>,<\"\';:!@#$%^&()_`~]', ' ', str(text))
    
    # Lemmetization
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])

    # Normalize the text.
    try:
        text = " ".join(normalise(text, variety="BrE", user_abbrevs={}, verbose=False))
    except:
        pass
    
    text = removeLen1words_num2words(text)
    
    return str(text).strip()


def return_category(text):
    text = PreProcessing(text)
    vec = TfidfVectorizer(vocabulary=vocab).fit_transform([text]).toarray()
    category = clf.predict(vec)
    return d.get(category[0])

