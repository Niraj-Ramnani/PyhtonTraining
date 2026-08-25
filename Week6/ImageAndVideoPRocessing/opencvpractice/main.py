import cv2

image = cv2.imread("image.png")
resized_image = cv2.resize(image, (500, 300))
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray_photo.png", gray_image)
cv2.imshow("My Image", image)
cv2.imshow("Resized Image", resized_image)
cv2.imshow("Gray Image", gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()