# Jacob Pim
# Images

# Step 0) Importing libraries
import numpy as np
import cv2

def inBounds(point,height,width):
    x,y = point
    if x > height - 1 or y > width - 1 or x < 0 or y < 0:
        return False
    else:
        return True

def getNeighbors(point,shape):
    h,w = shape
    x,y = point
    possibleNeighbors = (x,y-1),(x,y+1),(x-1,y),(x+1,y),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x+1,y+1)
    actualNeighbors = []
    for p in possibleNeighbors:
        if inBounds(p,h,w):
            actualNeighbors.append(p)

    return actualNeighbors


# Step 1) Inverting a grayscale image
def invertGrayscale(img):
    inverted = np.zeros(img.shape, dtype=np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            inverted[i,j] = 255 - img[i,j]
    cv2.imwrite("invertedImage.png", inverted)

# Step 2) Inverting a BGR image
def invertBGR(img):
    inverted = np.zeros(img.shape, dtype=np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            inverted[i,j] = 255 - img[i,j]
    cv2.imwrite("invertedBGRImage.png", inverted)

# Step 3) Thresholding a grayscale image
def thresholdGrayscale(img):
    thresholded = np.zeros(img.shape, dtype=np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] < 128:
                thresholded[i,j] = 0
            else:
                thresholded[i,j] = 255
    cv2.imwrite("thresholdedImage.png", thresholded)
    
# Step 4) Thresholding a color image
def thresholdBGR(img):
    thresholded = np.zeros(img.shape, dtype=np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j][0] < 128:
                thresholded[i,j][0] = 0
            else:
                thresholded[i,j][0] = 255

            if img[i,j][1] < 128:
                thresholded[i,j][1] = 0
            else:
                thresholded[i,j][1] = 255

            if img[i,j][2] < 128:
                thresholded[i,j][2] = 0
            else:
                thresholded[i,j][2] = 255

    cv2.imwrite("thresholedBGRImage.png", thresholded)

# Step 5) Getting even more neighbors than before
def getMoreNeighbors(point,shape):
    h,w = shape
    x,y = point
    possibleNeighbors = (x,y-1),(x,y+1),(x-1,y),(x+1,y),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x+1,y+1), (x-2,y),(x+2,y),(x,y-2),(x,y+2),(x-2,y-2),(x-2,y+2),(x+2,y-2),(x+2,y+2), (x-1,y-2),(x+1,y-2),(x-1,y+2),(x+1,y+2),(x-2,y-1),(x+2,y-1),(x-2,y+1),(x+2,y+1)
    actualNeighbors = []
    for p in possibleNeighbors:
        if inBounds(p,h,w):
            actualNeighbors.append(p)

    return actualNeighbors
# Step 6) Getting the average value of even more neighbors
def neighborAverage(point, img):
    neighbors = getMoreNeighbors(point, img.shape)
    sum = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            sum += img[i,j]
    return sum // len(neighbors)

# Step 7) Blurring a grayscale image
def blurGrayscale(img):
    blurred = np.zeros(img.shape, dtype=np.uint8)
    for i in range(img.shape[0]):
        # print(f"at row {i}")
        for j in range(img.shape[1]):
            avg = neighborAverage((i,j), img)
            blurred[i,j] = avg
    cv2.imwrite("blurredImage.png", blurred)

def blurBGR(img):
    pass

# Step 8) Blurring a BGR image

negativeGirl = cv2.imread("negativeGirlWithEarring.png", 1)
negativeBuilding = cv2.imread("negativeBuilding.png", 0)
negativeHorse = cv2.imread("negativeHorse.png", 0)

girl = cv2.imread("images/girlWithEarring.png", 1)
building = cv2.imread("images/building.png", 0)

thresholdedBuilding = cv2.imread("images/thresholdedBuilding.png", 1)
thresholdedGirl = cv2.imread("images/thresholdedGirl.png", 1)

invertGrayscale(negativeBuilding)

# blurGrayscale(negativeHorse, "blurredHorse")
