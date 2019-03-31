import jieba.analyse
import os
jieba.set_dictionary('jieba_dict/dict.txt.big')

fileList = os.listdir('text')
featureList = []
for filename in fileList:
    with open('text/' + filename, 'r') as f:
        text = f.read().strip().replace('\n', '')
        tags = jieba.analyse.extract_tags(text, 10)
        featureList.append(','.join(tags))
for x in featureList:
    print(x)
