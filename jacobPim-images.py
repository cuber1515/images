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
def invertGrayscale(image):
    slate = np.zeros(image.shape, dtype=np.uint8) + 255
    img = slate - image
    return img

# Step 2) Inverting a BGR image
def invertBGR(image):
    image[:,:,0] = invertGrayscale(image[:,:,0])
    image[:,:,1] = invertGrayscale(image[:,:,1])
    image[:,:,2] = invertGrayscale(image[:,:,2])
    return image

# Step 3) Thresholding a grayscale image
def thresholdGrayscale(image,threshold):
    height, width = image.shape
    for x in range(height):
        for y in range(width):
            if image[x,y] < threshold:
                image[x,y] = 0
            else:
                image[x,y] = 255
    
    return image
    
# Step 4) Thresholding a color image
def thresholdBGR(image,threshold):
    image[:,:,0] = thresholdGrayscale(image[:,:,0],threshold)
    image[:,:,1] = thresholdGrayscale(image[:,:,1],threshold)
    image[:,:,2] = thresholdGrayscale(image[:,:,2],threshold)
    return image

# Step 5) Getting even more neighbors than before
def getMoreNeighbors(point,shape):
    h,w = shape
    x,y = point
    possibleNeighbors = (x,y-2),(x,y-1),(x,y+1),(x,y+2),(x-1,y-2),(x-1,y-1),(x-1,y+1),(x-1,y+2),(x-1,y),(x-2,y-2),(x-2,y-1),(x-2,y+1),(x-2,y+2),(x-2,y),(x+1,y-2),(x+1,y-1),(x+1,y+1),(x+1,y+2),(x+1,y),(x+2,y-2),(x+2,y-1),(x+2,y+1),(x+2,y+2),(x+2,y)
    actualNeighbors = []
    for p in possibleNeighbors:
        if inBounds(p,h,w):
            actualNeighbors.append(p)

    return actualNeighbors

# Step 6) Getting the average value of even more neighbors
def neighborAverage(point,image):
    height,width = image.shape
    neighbors = getMoreNeighbors(point,(height,width))

    sum = 0
    for n in neighbors:
        sum += float(image[n[0],n[1]])
    average = sum/len(neighbors)

    return average

# Step 7) Blurring a grayscale image
def blurGrayscale(image):
    copy = np.copy(image)
    height, width = image.shape
    for x in range(height):
        for y in range(width):
            copy[x,y] = neighborAverage((x,y),image)
    return copy

def blurBGR(image):
    image[:,:,0] = blurGrayscale(image[:,:,0])
    image[:,:,1] = blurGrayscale(image[:,:,1])
    image[:,:,2] = blurGrayscale(image[:,:,2])
    return image

# Step 8) Blurring a BGR image
"""
negativeGirl = cv2.imread("negativeGirlWithEarring.png", 1)
negativeHorse = cv2.imread("negativeHorse.png", 0)

girl = cv2.imread("images/girlWithEarring.png", 1)
building = cv2.imread("images/building.png", 0)

thresholdedBuilding = cv2.imread("images/thresholdedBuilding.png", 1)
thresholdedGirl = cv2.imread("images/thresholdedGirl.png", 1)
"""