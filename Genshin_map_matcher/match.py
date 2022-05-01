import numpy as np
import imutils
import cv2

template = cv2.imread("target2.png")
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]

image = cv2.imread("origin.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
found = None


for scale in np.linspace(0.2, 1.0, 20)[::-1]:
    resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
    r = gray.shape[1] / float(resized.shape[1])
    if resized.shape[0] < tH or resized.shape[1] < tW:
        break
    edged = cv2.Canny(resized, 50, 200)
    result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
    if found is None or maxVal > found[0]:
        found = (maxVal, maxLoc, r)


(_, maxLoc, r) = found
(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))


a = int((startX+endX)/2)
b = int((startY+endY)/2)
cv2.circle(image, (a, b), 2, (0, 0, 255), 2)


cv2.imwrite("test2.png", image)