from skimage.metrics import structural_similarity as compare_ssim
import cv2

def image_comparison(image_1, image_2):
    def resize_images(image1, image2):
        height1, width1 = image1.shape[:2]
        height2, width2 = image2.shape[:2]

        if height1 != height2 or width1 != width2:
            new_height = min(height1, height2)
            new_width = min(width1, width2)

            image1 = cv2.resize(image1, (new_width, new_height))
            image2 = cv2.resize(image2, (new_width, new_height))

        return image1, image2


    def resize_for_display(image, target_width=500):
        aspect_ratio = image.shape[1] / image.shape[0]
        target_height = int(target_width / aspect_ratio)
        return cv2.resize(image, (target_width, target_height))


    # baca gambar
    imageA = image_1
    imageB = image_2
    # print(imageA)

    imageA, imageB = resize_images(imageA, imageB)

    # konversi warna gambar
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # lihat kemiripan gambar pake lib skit image
    (score, diff) = compare_ssim(grayA, grayB, full=True, gaussian_weights=True)

    diff = (diff * 255).astype("uint8")

    thresh_value, thresh = cv2.threshold(
        diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    cnts, _ = cv2.findContours(
        thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        if cv2.contourArea(c) < 100:
            continue

        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # print("SSIM: {:.2f}".format(score))

    imageA_resized = resize_for_display(imageA)
    imageB_resized = resize_for_display(imageB)
    diff_resized = resize_for_display(diff)
    thresh_resized = resize_for_display(thresh)

    return imageB_resized, imageA_resized, diff_resized, thresh_resized