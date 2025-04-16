import os
import cv2
import numpy as np

name = input("What is your full name?\n")
name = name.split(" ")

lowerFirstName = name[0][0].lower() + name[0][1:]
regularLastName = name[1]
prefix = lowerFirstName + regularLastName
fileName = prefix + "-images.py"

if not os.path.exists(fileName):
    print("FILE NOT FOUND: Make sure the formatting on your file\'s title is correct.")
    print("The format should be : " + prefix + "-images.py")
    raise SystemExit

file = open(fileName,"r")
text = file.read()
lines = text.split("\n")
file.close()

issue = False
functionList = ["invertGrayscale","invertBGR","thresholdGrayscale","thresholdBGR","getMoreNeighbors","neighborAverage","blurGrayscale","blurBGR"]
for item in functionList:
    if not item in text:
        print("MISSING FUNCTION:  You must include a " + item + " function as per the lab manual.")
        issue = True

if issue:
    raise SystemExit

if os.path.exists("testLog.txt"):
    os.remove("testLog.txt")

file = open("testLog.txt","w")

def inBounds(point,height,width):
    x,y = point
    if x > height - 1 or y > width - 1 or x < 0 or y < 0:
        return False
    else:
        return True

def realgetMoreNeighbors(point,shape):
    h,w = shape
    x,y = point
    possibleNeighbors = (x,y-2),(x,y-1),(x,y+1),(x,y+2),(x-1,y-2),(x-1,y-1),(x-1,y+1),(x-1,y+2),(x-1,y),(x-2,y-2),(x-2,y-1),(x-2,y+1),(x-2,y+2),(x-2,y),(x+1,y-2),(x+1,y-1),(x+1,y+1),(x+1,y+2),(x+1,y),(x+2,y-2),(x+2,y-1),(x+2,y+1),(x+2,y+2),(x+2,y)
    actualNeighbors = []
    for p in possibleNeighbors:
        if inBounds(p,h,w):
            actualNeighbors.append(p)

    return actualNeighbors


def realneighborAverage(point,image):
    height,width = image.shape
    neighbors = realgetMoreNeighbors(point,(height,width))

    sum = 0
    for n in neighbors:
        sum += float(image[n[0],n[1]])
    average = sum/len(neighbors)

    return average

def realinvertGrayscale(image):
    slate = np.zeros(image.shape, dtype=np.uint8) + 255
    img = slate - image
    return img

def realinvertBGR(image):
    image[:,:,0] = realinvertGrayscale(image[:,:,0])
    image[:,:,1] = realinvertGrayscale(image[:,:,1])
    image[:,:,2] = realinvertGrayscale(image[:,:,2])
    return image

def realthresholdGrayscale(image,threshold):
    height, width = image.shape
    for x in range(height):
        for y in range(width):
            if image[x,y] < threshold:
                image[x,y] = 0
            else:
                image[x,y] = 255
    
    return image

def realthresholdBGR(image,threshold):
    image[:,:,0] = realthresholdGrayscale(image[:,:,0],threshold)
    image[:,:,1] = realthresholdGrayscale(image[:,:,1],threshold)
    image[:,:,2] = realthresholdGrayscale(image[:,:,2],threshold)
    return image

def realblurGrayscale(image):
    copy = np.copy(image)
    height, width = image.shape
    for x in range(height):
        for y in range(width):
            copy[x,y] = realneighborAverage((x,y),image)
    return copy

def realblurBGR(image):
    image[:,:,0] = realblurGrayscale(image[:,:,0])
    image[:,:,1] = realblurGrayscale(image[:,:,1])
    image[:,:,2] = realblurGrayscale(image[:,:,2])
    return image

def listEquals(l1,l2):
    for elem in l1:
        if not elem in l2:
            return False
    return True

from importlib.machinery import SourceFileLoader
exec(prefix+"=SourceFileLoader(\"stc\",\""+fileName+"\").load_module()")
score = 0

file.write("TEST OF  :  invertGrayscale\n")
negBuildIG = cv2.imread("negativeBuilding.png",0)
exec("test1="+prefix+".invertGrayscale(negBuildIG)")
real1 = realinvertGrayscale(negBuildIG)
if real1[100,100] == test1[100,100]:
    file.write("TEST PASSED\n\n")
else:
    file.write("TEST FAILED\n\n")


file.write("TEST OF  :  invertBGR\n")
negGWEIBGR = cv2.imread("girlWithEarringNegative.png")
exec("test2="+prefix+".invertBGR(negGWEIBGR)")
real2 = realinvertBGR(negGWEIBGR)
if real2[100,100,1] == test2[100,100,1]:
    file.write("TEST PASSED\n\n")
else:
    file.write("TEST FAILED\n\n")


file.write("TEST OF  :  thresholdGrayscale\n")
exec("test3="+prefix+".thresholdGrayscale(real1,140)")
real3 = realthresholdGrayscale(real1,140)
if real3[100,100] == test3[100,100]:
    file.write("TEST PASSED\n\n")
else:
    file.write("TEST FAILED\n\n")


file.write("TEST OF  :  thresholdBGR\n")
exec("test4="+prefix+".thresholdBGR(real2,140)")
real4 = realthresholdBGR(real2,140)
if real4[100,100,1] == test4[100,100,1]:
    file.write("TEST PASSED\n\n")
else:
    file.write("TEST FAILED\n\n")


file.write("TEST OF  :  getMoreNeighbors\n")
in50 = (1,1)
in51 = (20,20)
exec("test5="+prefix+".getMoreNeighbors(in50,in51)")
real5 = realgetMoreNeighbors(in50,in51)
if listEquals(real5,test5):
    file.write("TEST PASSED\n\n")
else:
    file.write("TEST FAILED\n\n")


file.write("TEST OF  :  neighborAverage\n")
exec("test6="+prefix+".neighborAverage((100,100),real1)")
real6 = realneighborAverage((100,100),real1)
if real6 == test6:
    file.write("TEST PASSED\n\n")
else:
    file.write("TEST FAILED\n\n")


file.write("TEST OF  :  blurGrayscale\n")
exec("test7="+prefix+".blurGrayscale(real1)")
real7 = realblurGrayscale(real1)
if real7[100,100] == test7[100,100]:
    file.write("TEST PASSED\n\n")
else:
    file.write("TEST FAILED\n\n")


file.write("TEST OF  :  blurBGR\n")
exec("test8="+prefix+".blurBGR(real2)")
real8 = realblurBGR(real2)
if real8[100,100,1] == test8[100,100,1]:
    file.write("TEST PASSED")
else:
    file.write("TEST FAILED")