# lets do the assignment ---where i will load the image ,convert into grayscale,show and save it it based on the user input name and save ,show it--and base on the user demand like save and show it will work like that--->
import cv2

# Read image
image = cv2.imread(r"C:\Users\harip\OneDrive\Pictures\Camera Roll\WIN_20251225_19_25_32_Pro.jpg")

# Function to show image
def showImage():
    cv2.imshow("Original Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Function to save image
def saveImage():
    cv2.imwrite("saved.jpg", image)
    print("Image is saved successfully")

# Function to convert to gray
def grayImage():
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Gray Image", gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Main logic
if image is not None:
    print("1) Show Image")
    print("2) Convert to Gray")
    print("3) Convert to Gray and Save")
    print("4) Exit")

    x = input("Enter your choice: ")

    if x == "1":
        showImage()

    elif x == "2":
        grayImage()

    elif x == "3":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("gray_saved.jpg", gray)
        print("Gray image saved")

    elif x == "4":
        print("Exiting program")

    else:
        print("Invalid choice")

else:
    print("Image not found")
