from collections import Counter
from math import ceil
import re
import pkuseg


def average_sentence_length(doc):
    n = 0
    length = 0
    for sent in doc.sents:
        l = 0
        for tok in sent.tokens:
            if tok.pos != 'PUNCT':
                l += 1
        n += 1
        length += l
    return length / n


def common_words(doc, n=100):
    counter = Counter([tok.lemma for tok in doc.tokens if tok.pos != 'PUNCT'])
    return counter.most_common(n)


def sttr(doc):
    tokens = [tok.lemma for tok in doc.tokens if tok.pos != 'PUNCT']
    sttr = 0
    for i in range(ceil(len(tokens) / 1000)):
        sttr += len(set(tokens[1000*i:1000*(i+1)]))
    return sttr / len(tokens)


seg = pkuseg.pkuseg(postag=True, user_dict='my_dict.txt')   


def _split_zh(text, limit=1000):
        sent_list = []
        text = re.sub('(?P<quotation_mark>([。？！](?![”’"\'）])))', r'\g<quotation_mark>\n', text)
        text = re.sub('(?P<quotation_mark>([。？！]|…{1,2})[”’"\'）])', r'\g<quotation_mark>\n', text)

        sent_list_ori = text.splitlines()
        for sent in sent_list_ori:
            sent = sent.strip()
            if not sent:
                continue
            else:
                while len(sent) > limit:
                    temp = sent[0:limit]
                    sent_list.append(temp)
                    sent = sent[limit:]
                sent_list.append(sent)

        return sent_list


class Doc_zh:
    def __init__(self, doc):
        sents = _split_zh(doc)
        self.sents = []
        for sent in sents:
            self.sents.append(Sent_zh(sent))
    
    @property
    def tokens(self):
        for sent in self.sents:
            yield from sent.tokens


class Sent_zh:
    def __init__(self, sent):
        self.text = sent
        self.tokens = []
        for tok in seg.cut(sent):
            self.tokens.append(Token_zh(tok[0], tok[1]))


class Token_zh:
    def __init__(self, word, pos):
        self.text = word
        self.lemma = word
        if pos == 'w':
            self.pos = 'PUNCT'
        else:
            self.pos = pos

