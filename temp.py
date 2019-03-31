import numpy as np
import cv2 as cv
from imageGod import *

img = cv.imread('temp2.jpg')

print(OCR(img, preprocess=False))
