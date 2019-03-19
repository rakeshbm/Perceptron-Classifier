import json
import time
from math import log
start_time = time.time()
with open(sys.argv[1], 'r', encoding="utf-8") as f:
    content = f.read()

total_tag_dict = {}
first_tag_dict = {}
tag_dict = {}
emission_prob = {}
num_lines = 0

addone=10**-8

for x in content.splitlines():
    
    num_lines += 1
    
    #update total tags dictionary
    for y in x.split(" "):
        if(y.rsplit('/')[-1] in total_tag_dict):
            total_tag_dict[y.rsplit('/')[-1]] += 1
        else:
            total_tag_dict[y.rsplit('/')[-1]] = 1
    
    #find first tags
    if x.split(' ')[0]:
        if(x.split(' ')[0].rsplit('/',1)[-1] in first_tag_dict):
            first_tag_dict[x.split(' ',1)[0].rsplit('/')[-1]] += 1
        else:
            first_tag_dict[x.split(' ',1)[0].rsplit('/')[-1]] = 1
    
    #find "following" tags
    temp = []
    for y in x.split(" "):
        temp.append(y.rsplit("/",1)[-1])
    for v, w in zip(temp[:-1], temp[1:]):
        if v in tag_dict:
            if w in tag_dict[v]:
                tag_dict[v][w]+=1
            else:
                tag_dict[v][w]=1
        else:
            tag_dict[v]=dict()
            tag_dict[v][w]=1
            
    #find emission probabilities
    temp = []
    for y in x.split(" "):
        temp.append(''.join(map(str, y.rsplit("/",1)[0:-1])))
        temp.append(y.rsplit("/",1)[-1])
    for v, w in zip(temp[::2], temp[1::2]):
        if v in emission_prob:
            if w in emission_prob[v]:
                emission_prob[v][w]+=1
            else:
                emission_prob[v][w]=1
        else:
            emission_prob[v]=dict()
            emission_prob[v][w]=1
        
for major_key in emission_prob:
    for minor_key in emission_prob[major_key]:
        emission_prob[major_key][minor_key] /= total_tag_dict[minor_key]

for major_key in tag_dict:
    for minor_key in tag_dict[major_key]:
        tag_dict[major_key][minor_key] /= total_tag_dict[major_key]

for x in first_tag_dict:
    first_tag_dict[x] /= num_lines

store_data = dict()
with open('hmmmodel.txt', 'w') as outfile:
    #utfile.write("Probabilities of tags appearning at the beginning of sentence:\n\n")
    store_data['beginning_tag'] = dict()
    store_data['beginning_tag'] = first_tag_dict
    store_data['transition_probabilities'] = dict()
    store_data['transition_probabilities'] = tag_dict
    store_data['emission_probabilities'] = dict()
    store_data['emission_probabilities'] = emission_prob
    outfile.write(json.dumps(store_data))
    #outfile.write("\n\nTransition probabilities:\n\n")
    #outfile.write(json.dumps(tag_dict))
    #outfile.write("\n\nEmission probabilities:\n\n")
    #outfile.write(json.dumps(emission_prob))
    
result = []
op = open("results.txt","w", encoding="utf-8")
with open("C:/Users/Rakesh/Documents/data/en_dev_raw.txt", 'r', encoding="utf-8") as f:
    for line in f:
        s = line.split()
        curr = []
        traverse = {}
        for i,word in enumerate(s):
            curr.append(dict())
            traverse[i] = dict()
            if word not in emission_prob:
                emission_prob[word] = dict()
                for tag in total_tag_dict:
                    emission_prob[word][tag]=addone
                    
            if i == 0:
                for tag in emission_prob[word]:
                    if tag not in first_tag_dict:
                        first_tag_dict[tag] =addone 
                    curr[i][tag] = log(emission_prob[word][tag])+log(first_tag_dict[tag])
    
            else:
                for current_tag in emission_prob[word]:
                    temp = -float('inf')
                    for prev_tag in curr[i-1]:
        
                        if prev_tag not in tag_dict:
                            tag_dict[prev_tag] = dict()
                            tag_dict[prev_tag][current_tag] = addone
                        if current_tag not in tag_dict[prev_tag]:
                            tag_dict[prev_tag][current_tag] = addone

                        temp2=(curr[i-1][prev_tag])
                        temp2+=log(tag_dict[prev_tag][current_tag])
                        temp2+=log(emission_prob[word][current_tag])
                        if temp2 > temp:
                            temp = temp2
                            curr[i][current_tag] = temp
                            traverse[i][current_tag] = prev_tag
        
        p = max(curr[-1], key=curr[-1].get)
        mid = []
        s_len = len(s)-1
        mid.append(p)
        rec = p
        
        while s_len > 0:
            mid.append(traverse[s_len][rec])
            rec = traverse[s_len][rec]
            s_len -= 1
        mid = mid[::-1]
        result.append(mid)


tags = ' '.join(str(r) for v in result for r in v)
next = 0
with open("C:/Users/Rakesh/Documents/data/en_dev_raw.txt", 'r', encoding="utf-8") as f:
    tags = tags.split()
    for line in f:
        for word in line.split():
            op.write(word+"/"+tags[next]+" ")
            next += 1
        op.write("\n")
        
op.close()

print("--- %s seconds ---" % (time.time() - start_time))