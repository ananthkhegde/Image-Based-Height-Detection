import cv2
import numpy as np
from operator import itemgetter
from scipy.spatial import distance
from imutils import perspective
from imutils import contours

class DetectHeight:
    def getHeight(self, img_copy):

        self.img_copy = img_copy

        ## Load the Image and resize
        if type(img_copy) == bytes:
            # If a bytes object decoded from base 64 encoded string is received
            img = cv2.imdecode(np.fromstring(img_copy, np.uint8), 1)
        else:
            # If image file is received
            img = cv2.imdecode(np.fromstring(img_copy.read(), np.uint8), 1)

        ## Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ########  Implement Canny Edge Detection  ########
        # Resize the image before performing Canny Edge detection
        rows, cols = img.shape[:2]
        M = np.float32([[1, 0, 0], [0, 1, 20]])

        img_WP = cv2.warpAffine(img, M, (cols, rows))

        gray_wp = cv2.cvtColor(img_WP, cv2.COLOR_BGR2GRAY)
        blurred_wp = cv2.GaussianBlur(gray_wp, (13, 13), 0)

        # Apply Canny Detection
        edged_wp = cv2.Canny(blurred_wp, 50, 100)
        edged_wp = cv2.dilate(edged_wp, None, iterations=1)
        edged_wp = cv2.erode(edged_wp, None, iterations=1)

        # Find the contours in the binarized image
        cnts = cv2.findContours(edged_wp.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[1]

        # Sort the contours from left to right

        cnts_ = contours.sort_contours(cnts)

        # WRITE A FUNCTION TO CHECK FOR EXISTENCE OF ALL POINTS IN BOX (MINAREARECT) In THE LIST OF CONTOURS
        index = 0
        distances = []

        for c in cnts:

            point_distances = []
            dists = []

            box = cv2.minAreaRect(c)
            box = cv2.boxPoints(box)
            box = np.array(box, dtype=float)
            box = perspective.order_points(box)

            epsilon = cv2.arcLength(c, True)
            # print(epsilon)
            approx = cv2.approxPolyDP(c, 0.07 * epsilon, True)
            # print(len(approx))

            if len(approx) >= 4:
                reference_object_contour = c
                break

        # Compute the minimum bounded rectangle
        box = cv2.minAreaRect(reference_object_contour)

        # Initialize the object width and height in pixels
        width_pixels = box[1][0]
        height_pixels = box[1][1]

        # Compute the box points and order them in required format
        box = cv2.boxPoints(box)
        box = np.array(box, dtype=float)
        box = perspective.order_points(box)

        cv2.drawContours(img_WP, [box.astype("int")], -1, (0, 255, 0), 6)

        ######### Implement SIFT Detector ########
        sift = cv2.xfeatures2d.SIFT_create()
        kp, des = sift.detectAndCompute(gray, None)

        # Convert the Key Points into an array of coordinates
        points = []
        for point in kp:
            points.append(point.pt)

        # Determine the Top Most and Bottom Most Points
        points_ordered = sorted(points, key=itemgetter(1), reverse=False)
        first = 0
        last = len(points_ordered) - 1
        head_and_feet = [points_ordered[first], points_ordered[last]]
        head_and_feet[1] = (head_and_feet[0][0], head_and_feet[1][1])

        for point in head_and_feet:
            cv2.circle(img, (int(point[0]), int(point[1])), 2, (0, 0, 255), 5)

        # Determine the Kid Height in Pixels
        kid_height_pixels = distance.euclidean(head_and_feet[0], head_and_feet[1])

        ######## Calculate the Edges of Reference object ########
        reference_points = [box[1], box[2]]

        for point in reference_points:
            cv2.circle(img_WP, (int(point[0]), int(point[1])), 2, (200, 255, 0), 5)

        # Initialize the reference real height
        reference_height_inches = 6.02 * 3.5

        # Calculate the reference pixel height
        reference_height_pixels = distance.euclidean(reference_points[0], reference_points[1])

        # Calculate the conversion factor
        inches_per_pixel = reference_height_inches / reference_height_pixels

        # Calculate the Kid's Height in Inches
        kid_height_inches = kid_height_pixels * inches_per_pixel

        return kid_height_inches