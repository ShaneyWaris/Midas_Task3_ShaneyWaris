from num2words import num2words
import re, joblib
stop_words = [
    'to', 'you', 'this', 'itself', 'as', 'there', 'very', 'does', 'couldn', 'of', "you'll", 
    'himself', 'didn', "hasn't", 'here', 'then', "mightn't", 'just', 'after', 'wouldn', 'having', 
    'the', 'doesn', 'did', 'these', "you're", 'your', "it's", 'if', 'all', 'm', 'such', 'will', 'above', 
    'before', 'do', 'where', "shan't", 'won', 'at', 'or', 'was', 'than', 'it', 'hadn', 'his', "won't", 'o', 
    'mustn', 'ma', 's', "haven't", 'own', 'be', 'other', 'she', 'only', 'mightn', "she's", 'off', 'theirs', 
    "wouldn't", 'more', 'ourselves', 'each', 'yourselves', 'about', "weren't", 'whom', 'needn', 't', 'up', 'from', 
    'its', 'with', 'nor', 'i', 'are', 'aren', 'y', 'once', 'in', "don't", 'being', 'some', 'when', 've', 'doing', 
    'haven', 'yourself', 'had', 'd', 'ain', 'our', 'wasn', 'herself', "doesn't", 'by', 'they', 'most', 'hers', 
    'those', 'hasn', 'that', 'we', 'how', "that'll", 'has', 'and', 'few', 'ours', 'him', 'again', 'same', 'further', 
    "couldn't", "wasn't", 'into', 'should', 'what', "hadn't", 'shan', 'any', 'why', 'their', 'yours', 'have', 'while', 
    'both', 'under', 'until', 'themselves', 'so', 'which', 'between', 'me', 're', "you've", 'shouldn', 'he', 'them', 'an',
     "isn't", 'over', 'not', 'for', 'but', 'can', "shouldn't", "needn't", 'on', 'below', 'my', "aren't", 'a', 'because', 'against', 
     "mustn't", 'myself', 'were', 'is', 'weren', 'now', 'no', 'll', 'isn', 'out', 'am', 'during', "didn't", 'through', 'don', "should've", 
     "you'd", 'her', 'down', 'who', 'too', 'been']


clf = joblib.load('./model/TfidfVectorizer__MLPClassifier.pkl')
vocab = joblib.load('./pkl files/vocab.pkl')
test = joblib.load('./pkl files/new_tf.pkl')
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
    word_tokens = text.split()
    text = " ".join([w for w in word_tokens if not w in stop_words])
    
    # Remove urls.
    text = re.sub(r"(http\S+)|(www\S+)|(\w*.com\b)", " ", str(text))

    # Remove Punctuations.
    text = re.sub(r'[+*|/\\\-?.>,<\"\';:!@#$%^&()_`~]', ' ', str(text))
    
    text = removeLen1words_num2words(text)
    
    return str(text).strip()


def return_category(text):
    text = PreProcessing(text)
    vec = test.fit_transform([text]).toarray()
    category = clf.predict(vec)
    return d.get(category[0])
