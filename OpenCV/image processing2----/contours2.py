# lets draw on image based on contour---
import cv2 as cv
pic=input("Enter the path of the image:")
image=cv.imread(pic)
gray=cv.cvtColor(image,cv.COLOR_RGB2GRAY)
_,threshold=cv.threshold(gray,130,255,cv.THRESH_BINARY)


contours, hierarchy=cv.findContours(threshold,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

for cont in contours:
    approx=cv.approxPolyDP(cont,0.03*cv.arcLength(cont,True),True)
    corner=len(approx)
    if corner==3:
        shape_name="Triangle"
    elif corner==2:
        shape_name="Line"
    elif corner==4:
        shape_name="Rectangle"
    elif corner==5:
        shape_name="Pentagone"
    elif corner > 5:
        shape_name="Circle"
    else:
        shape_name="unknow"
cv.drawContours(image,[approx],0,(0,0,255),2) 
x=approx.ravel()[0]   
y=approx.ravel()[1] -10
cv.putText(image,shape_name,(x,y),cv.FONT_HERSHEY_COMPLEX,0.8,(0,0,255),1)
cv.imshow("contours",image)
cv.waitKey(0)
cv.destroyAllWindows()