# let make user input for video capturing ---->
import os
import cv2
camera=cv2.VideoCapture(0)

video_frame_width=int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
video_frame_height=int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

codec=cv2.VideoWriter_fourcc(*'XVID')

print("what is your mood today----")
print("1) video recoring !")
print("2) Draw something on your photo !")
user=input("Enter your choice (1/2):")
if user=="1":
    recored=cv2.VideoWriter("recorded_video.avi",codec,30,(video_frame_width,video_frame_height))
   # yaha avi -->audio video interleave
    while True:
     success,image=camera.read()
     if not success:
         break
     recored.write(cv2.flip(image,1)) # yaha pe recording video ko flip kar diya gaya hai
     cv2.imshow("live recording",cv2.flip(image,1))
    
     if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    camera.release()
    recored.release()
elif user=="2":
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
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif choice == "2":
        cv2.circle(image, (200, 200), 50, (0, 255, 0), 2)
        cv2.imshow("Circle", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif choice == "3":
        cv2.rectangle(image, (100, 100), (300, 300), (255, 0, 0), 2)
        cv2.imshow("Rectangle", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif choice == "4":
        cv2.line(image, (50, 50), (400, 400), (0, 0, 255), 2)
        cv2.imshow("Line", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif choice == "5":
        txt=input("enter tour text:")
        org=(640,275)
        thickness=2
        draw=cv2.putText(image,txt,org,cv2.FONT_HERSHEY_COMPLEX,2.0,(0,0,255),thickness)
        cv2.imshow("write text on image--->",draw)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Invalid choice!")

else:
    print("invalid choice!")
