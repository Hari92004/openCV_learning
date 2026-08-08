import os
import cv2

image_path = input("Enter image path: ")

if not os.path.exists(image_path):
    print("File path does not exist!")
    exit()

image = cv2.imread(image_path)

if image is not None:
    print("Image is found!")
    print("Enter your choice to do with it:")
    print("1) Open image")
    print("2) Draw circle")
    print("3) Draw rectangle")
    print("4) Draw line")
    print("5) write anythings")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        cv2.imshow("Image", image)

    elif choice == "2":
        cv2.circle(image, (200, 200), 50, (0, 255, 0), 2)
        cv2.imshow("Circle", image)

    elif choice == "3":
        cv2.rectangle(image, (100, 100), (300, 300), (255, 0, 0), 2)
        cv2.imshow("Rectangle", image)

    elif choice == "4":
        cv2.line(image, (50, 50), (400, 400), (0, 0, 255), 2)
        cv2.imshow("Line", image)
    elif choice == "5":
        txt=input("enter tour text:")
        org=(640,275)
        thickness=2
        draw=cv2.putText(image,txt,org,cv2.FONT_HERSHEY_COMPLEX,2.0,(0,0,255),thickness)
        cv2.imshow("write text on image--->",draw)
    else:
        print("Invalid choice!")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Image not found or unsupported format!")
