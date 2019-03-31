import pytesseract
import re
import os

books = os.listdir('pic')
for book in books:
    print('Processing', book)
    imgs = os.listdir('/'.join(['pic', book]))
    with open('text/' + book, 'w') as of:
        for img in imgs:
            text = pytesseract.image_to_string('/'.join(['pic', book, img]), lang='chi_tra+eng+jpn')
            #text = pytesseract.image_to_string('/'.join(['pic', book, img]), lang='chi_tra')
            text = re.sub(r'[ \n　]', '', text)
            of.write(text)
