import jieba
import os
jieba.set_dictionary('jieba_dict/dict.txt.big')
fileList = os.listdir('text')

for filename in fileList:
    with open('text/' + filename, 'r') as f:
        seg_list = jieba.cut(f.read().strip().replace('\n', ''))
        with open('seg/' + filename, 'w') as of:
            of.write(' '.join(seg_list))
