import re

import numpy as np
import requests

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

class StrUtil:

    # stop words from nltk
    STOPWORDS = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during',
                 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours',
                 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from',
                 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through',
                 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their',
                 'while', 'above', 'both', 'up', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any',
                 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then',
                 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you',
                 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few',
                 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further',
                 'was', 'here', 'than'}

    # common sense for expanding resource-id
    EXPAND = {
        'EditText': {'et': ['edit', 'text']},
        'ImageButton': {'bt': ['button'], 'btn': ['button'], 'fab': ['floating', 'action', 'button']},
        'Button': {'bt': ['button'], 'btn': ['button']},
        'TextView': {'tv': ['text', 'view']}
    }

    # common sense for merging resource-id
    MERGE = [
        ['to', 'do', 'todo'],  # a21-a23-b21, 0-step
        ['sign', 'up', 'signup'],  # Yelp
        ['log', 'in', 'login']  # Yelp
    ]

    TEXT_MERGE = [
        ['Log', 'In', 'Login']  # Yelp
    ]

    SIBLING_TEXT_MERGE = [
        ['Sign', 'in', 'Signin'],  # Yelp
        ['Sign', 'Up', 'Sign_Up'],  # Yelp
    ]

    TEXT_REPLACE = {
        '%': 'percent',  # a54-a55-b51, greedy
        '# of': 'number of'#,  # a51-a52-b52, greedy
        # 'tip': 'Percent',
        # 'Tip': 'Percent',
        # 'et': '',
        # 'ET': ''
    }

    CLASS_CATEGORY = {
        "edittext": ["edittext", "textview"],
        "textview": ["edittext", "textview", "button"],
        "button": ["textview", "button"]
    }

    @staticmethod
    def camel_case_split(identifier):
        # https://stackoverflow.com/questions/29916065/how-to-do-camelcase-split-in-python
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
        return [m.group(0) for m in matches]

    @staticmethod
    def sanitize(s):
        s = s.strip()
        s = re.sub(r'\s', ' ', s)  # replace [ \t\n\r\f\v] with space
        # convert float with 0 fraction to int, e.g., 15.0 -> 15 (a54-a52-b51)
        try:
            if float(s) and float(s) == int(float(s)):
                s = str(int(float(s)))
        except:
            pass
        for k, v in StrUtil.TEXT_REPLACE.items():
            s = s.replace(k, v)
        s = re.sub(r'[^\w ]', ' ', s)  # replace non [a-zA-Z0-9_], non-space with space
        # s = re.sub(r'[^a-zA-Z_ ]', ' ', s)
        s = re.sub(r' +', ' ', s)
        return s

    @staticmethod
    def tokenize(s_type, s, use_stopwords=True):
        if not s:
            return []
        if s_type == 'resource-id':
            # e.g., 'acr.browser.lightning:id/search'
            # r_id = s.split('/')[-1]
            r_id = s
            r_id = StrUtil.sanitize(r_id)
            assert r_id
            tokens = r_id.split('_')
            res = []
            for token in tokens:
                res += [t.lower() for t in StrUtil.camel_case_split(token)]
            res = StrUtil.merge_id(res)
            res = StrUtil.rmv_stopwords(res) if use_stopwords else res
            return res
        elif s_type in ['text', 'content-desc', 'parent_text', 'sibling_text']:
            res = StrUtil.sanitize(s).split()
            res = StrUtil.merge_text(res)
            if s_type == 'sibling_text':
                res = StrUtil.merge_sibling_text(res)
            res = StrUtil.rmv_stopwords(res) if use_stopwords else res
            return res
        elif s_type == 'Activity':
            act_id = s.split('.')[-1]
            act_id = StrUtil.sanitize(act_id)
            assert act_id
            tokens = act_id.split('_')
            res = []
            for token in tokens:
                res += [t.lower() for t in StrUtil.camel_case_split(token)]
            res = StrUtil.rmv_stopwords(res) if use_stopwords else res
            return res
        else:  # never happen
            assert False

    @staticmethod
    def merge_id(word_list):
        for left, right, merged in StrUtil.MERGE:
            if left in word_list and right in word_list and word_list.index(left) == word_list.index(right) - 1:
                word_list = word_list[:word_list.index(left)] + [merged] + word_list[word_list.index(right) + 1:]
        return word_list

    @staticmethod
    def merge_text(word_list):
        """Only replace the beginning"""
        for m in StrUtil.TEXT_MERGE:
            if m[:-1] == word_list:
                return m[-1:]
        return word_list

    @staticmethod
    def merge_sibling_text(word_list):
        """Only replace the beginning"""
        for m in StrUtil.SIBLING_TEXT_MERGE:
            phrase_len = len(m) - 1
            if m[:phrase_len] == word_list[:phrase_len]:
                return [m[-1]] + word_list[phrase_len:]
        return word_list

    @staticmethod
    def rmv_stopwords(tokens):
        # global stopwords
        if len(tokens) > 1:  # remove stopwords only if there are multiple words
            return [t for t in tokens if t not in StrUtil.STOPWORDS]
        else:
            return tokens

    @staticmethod
    def expand_text(w_class, w_attr, w_split_text):
        if w_attr != 'resource-id':
            return w_split_text
        else:
            w_class = w_class.split('.')[-1]
            if w_class in StrUtil.EXPAND:
                new_text = []
                for token in w_split_text:
                    if token in StrUtil.EXPAND[w_class]:
                        new_text += StrUtil.EXPAND[w_class][token]
                    else:
                        new_text.append(token)
                return new_text
            else:
                return w_split_text

    @staticmethod
    def w2v_sent_sim(s_new, s_old):
        # run w2v_service.py first to activate the w2v service
        data = {'s_new': s_new, 's_old': s_old}
        if len(s_new) == 0 or len(s_old) == 0:
            return None
        resp = requests.post(url='http://127.0.0.1:5000/w2v', data=data).json()
        if 'sent_sim' in resp and resp['sent_sim']:
            return resp['sent_sim']
        else:
            return None

    @staticmethod
    def get_tid(fname):
        return '_'.join(fname.split('.')[:-1])

    @staticmethod
    def get_method(signature):
        # e.g., 'com.example.anycut.CreateShortcutActivity: void onListItemClick(android.widget.ListView,android.view.View,int,long)'
        #       'something.CreateShortcutActivity: Self Loop()'
        assert signature.split()[-1].split('(')[0]
        return signature.split()[-1].split('(')[0]

    @staticmethod
    def get_activity(signature):
        # e.g., 'com.example.anycut.CreateShortcutActivity: void onListItemClick(android.widget.ListView,android.view.View,int,long)'
        #       'something.CreateShortcutActivity: Self Loop()'
        # assert signature.split(':')[0].split('.')[-1]
        # return signature.split(':')[0].split('.')[-1].split('$')[0]
        assert signature.split(':')[0]
        return signature.split(':')[0].split('$')[0]

    @staticmethod
    def is_contain_email(txt):
        return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', txt)

def get_words_vector_by_tfidf(words):
    tmp_str = words[0]
    new_list = []
    if tmp_str.strip() == '':
        words = ['none']
    else:
        str_list = tmp_str.split(' ')
        for s in str_list:
            res = re.match(r'[^\x00-\xff]', s)
            if len(s) < 2 and res is not None:
                tmp_s = s + s
                new_list.append(tmp_s)
            else:
                new_list.append(s)

        tmp_str = ' '
        tmp_str = tmp_str.join(new_list)
        words = [tmp_str]

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(words))
    word = vectorizer.get_feature_names()
    weight = tfidf.toarray()

    return word, weight[0]

def get_cos_dist(vec1, vec2):
    dist1 = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    return dist1

def get_words_sim(x_words, x_weight, y_words, y_weight):
    map1 = {}
    for i in range(len(x_words)):
        map1[x_words[i]] = x_weight[i]

    map2 = {}
    for i in range(len(y_words)):
        map2[y_words[i]] = y_weight[i]

    key_word = list(set(x_words + y_words))

    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))

    for i in range(len(key_word)):
        for key in map1.keys():
            if key_word[i] == key:
                word_vector1[i] = map1[key]

        for key in map2.keys():
            if key_word[i] == key:
                word_vector2[i] = map2[key]

    return get_cos_dist(word_vector1, word_vector2)