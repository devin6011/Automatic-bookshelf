import re
import cv2 as cv
import os
import jieba
from subprocess import Popen, PIPE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


jieba.set_dictionary('jieba_dict/dict.txt.big')

def OCR(img, scaling_factor=1.0, lang='chi_tra'):
    #text = pytesseract.image_to_string(img, lang=lang)
    if scaling_factor != 1.0:
        img = cv.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv.INTER_CUBIC)
    tempFileName = 'ocr_temp_image_794535.jpg'
    cv.imwrite(tempFileName, img)
    process = Popen(['tesseract', tempFileName, 'stdout', '-l', lang], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    text = stdout.decode('utf-8').strip()
    os.remove(tempFileName)
    text = re.sub(r'[ \n　]', '', text)
    return text

def textSegment(text):
    seg_list = jieba.cut(text)
    return ' '.join(seg_list)

def extractFeature(text, num_features=10):
    tags = jieba.analyse.extract_tags(text, num_features)
    return tags

def topicClustering(imgs, num_clusters=3):
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1,3), max_features=200000)
    corpora = []
    for img in imgs:
        corpora.append(textSegment(OCR(img)))
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpora)
    km = KMeans(n_clusters=num_clusters, n_init=50)
    km.fit(tfidf_matrix)
    return km.labels_.tolist()

def featureMatching(img1, img2):
    img1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    sift = cv.xfeatures2d.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    cnt = sum([m.distance < 0.7 * n.distance for m, n in matches])
    return cnt


#img1 = cv.imread('pic/1/1.jpg')
#img2 = cv.imread('pic/2/1.jpg')
#img3 = cv.imread('pic/4/1.jpg')
#imgs = [img1, img2, img3]
#
#print(textSegment(OCR(img1)))
#print(topicClustering(imgs))
#print(featureMatching(img1, img2))
from picamera.array import PiRGBArray
from picamera import PiCamera
cam=PiCamera(resolution=(640,480))
rawCapture=PiRGBArray(cam)
while True:
    #ret,frame=cam.read()
    cam.capture(rawCapture, format="bgr")
    image = rawCapture.array   
    #cv.imshow('frame',frame)
    print(textSegment(OCR(image)))
    rawCapture.truncate(0)
cv.release()
cv.destoryAllWindows()

