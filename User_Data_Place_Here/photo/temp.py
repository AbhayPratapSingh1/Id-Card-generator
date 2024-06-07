import cv2
image = cv2.imread("1.png")
for i in range(55,70):
    cv2.imwrite(f"{i}.png", image)