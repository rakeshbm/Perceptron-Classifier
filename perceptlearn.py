import sys
import random
import re
from math import log

with open("C:/Users/Rakesh/Documents/coding-2-data-corpus/train-labeled.txt", 'r', encoding="utf-8") as f:
    content = f.read().lower()
  
eps = sys.float_info.epsilon
reviews = []
weights = {}

for line in content.splitlines():
    temp = []
    if line.split(' ')[1] == "true":
        temp.append(1)
    elif line.split(' ')[1] == "fake":
        temp.append(-1)
    """if line.split(' ')[2] == "pos":
        num_pos += 1
    elif line.split(' ')[2] == "neg":
        num_neg += 1"""
    for word in line.split()[3:]:
        word = re.sub("^[\[\]!\"#$%&'()*+,\-./:;<=>?@\\_\^`{|}~]+", ' ', str(word))
        word = re.sub("[\[\]!\"#$%&'()*+,\-./:;<=>?@\\_\^`{|}~]+$", ' ', str(word))
        word = re.sub('[ \t]+','',word)
        temp.append(word)
    reviews.append(temp)

for review in reviews:
    for y in review[1:]:
        if y not in weights:
            weights[y] = 0

b = 0
for _ in range(20):
    for review in reviews:
        features = {}
        for word in review[1:]:
            if word not in features:
                features[word] = 1
            else:
                features[word] += 1
        for d in weights:
            if d in features:
                a = features[d] * weights[d] + b
            else:
                a = 0 * weights[d] + b
        if review[0]*a <= 0:
            for d in weights:
                if d in features:
                    weights[d] = features[d] * review[0] + weights[d]
                else:
                    weights[d] = 0 * review[0] + weights[d]
            b = b + review[0]

with open("C:/Users/Rakesh/Documents/coding-2-data-corpus/dev-text.txt", 'r', encoding="utf-8") as f:
    content = f.read().lower()

reviews = []
for line in content.splitlines():
    temp = []
    for word in line.split()[1:]:
        word = re.sub("^[\[\]!\"#$%&'()*+,\-./:;<=>?@\\_\^`{|}~]+", ' ', str(word))
        word = re.sub("[\[\]!\"#$%&'()*+,\-./:;<=>?@\\_\^`{|}~]+$", ' ', str(word))
        word = re.sub('[ \t]+','',word)
        temp.append(word)
    reviews.append(temp)

fake = 0
true = 0
for review in reviews:
    features = {}
    a = 0
    for word in review[1:]:
        if word not in features:
            features[word] = 1
        else:
            features[word] += 1
    for d in weights:
        if d not in features:
            a += weights[d] * 0 + b
        else:
            a += ( weights[d] * features[d] ) + b
    if a<=0:
        print("fake")
        fake += 1
    else:
        print("true")
        true += 1
        
print("true")
print("fake")