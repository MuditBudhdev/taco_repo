import cv2

cam = cv2.VideoCapture(0)
temp, frame = cam.read()

cv2.imwrite("pic.jpg", frame)

cam.release()
cv2.destroyAllWindows()