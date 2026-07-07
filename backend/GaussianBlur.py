import cv2

#we set a variable named "res" which means the result after 
#applying Gaussian blur to the image, which is the input from the camera
#only a function for filtering
def apply_gaussian_blur (input):
    res=cv2.GaussianBlur(input,(5,5),0)
    blurred_grey=cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    return blurred_grey