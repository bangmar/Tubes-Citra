# import the necessary packages
from skimage.metrics import structural_similarity as compare_ssim
import imutils
import cv2


def resize_images(image1, image2):
    # Resize the images to have the same dimensions
    height1, width1 = image1.shape[:2]
    height2, width2 = image2.shape[:2]

    if height1 != height2 or width1 != width2:
        # Choose the smaller dimension and resize both images
        new_height = min(height1, height2)
        new_width = min(width1, width2)

        image1 = cv2.resize(image1, (new_width, new_height))
        image2 = cv2.resize(image2, (new_width, new_height))

    return image1, image2


def resize_for_display(image, target_width=500):
    # Resize the image for better display
    aspect_ratio = image.shape[1] / image.shape[0]
    target_height = int(target_width / aspect_ratio)
    return cv2.resize(image, (target_width, target_height))


# Load images directly from the directory
# Replace "first.png" with the actual path to your first image
imageA = cv2.imread("first.png")
# Replace "second.png" with the actual path to your second image
imageB = cv2.imread("second.png")

# resize the images to have the same dimensions
imageA, imageB = resize_images(imageA, imageB)

# convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned
(score, diff) = compare_ssim(grayA, grayB, full=True, gaussian_weights=True)

# Convert the difference image to 8-bit unsigned integer type
diff = (diff * 255).astype("uint8")

# Threshold the difference image
thresh_value, thresh = cv2.threshold(
    diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# Find contours using a more flexible retrieval mode and contour approximation method
cnts, _ = cv2.findContours(
    thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Loop over the contours
for c in cnts:
    # Ignore small contours (adjust the threshold as needed)
    if cv2.contourArea(c) < 100:
        continue

    # Compute the bounding box of the contour and then draw the
    # bounding box on both input images to represent where the two
    # images differ
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

# Display the SSIM score
print("SSIM: {:.2f}".format(score))

# Resize images for better display
imageA_resized = resize_for_display(imageA)
imageB_resized = resize_for_display(imageB)
diff_resized = resize_for_display(diff)
thresh_resized = resize_for_display(thresh)

# Show the output images
cv2.imshow("Original", imageA_resized)
cv2.imshow("Modified", imageB_resized)
cv2.imshow("Diff", diff_resized)
cv2.imshow("Thresh", thresh_resized)
cv2.waitKey(0)
