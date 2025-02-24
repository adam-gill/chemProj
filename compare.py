import cv2

import numpy as np

from skimage.metrics import structural_similarity as ssim



def load_and_preprocess_image(image_path):

    """Load an image, convert to grayscale, and apply edge detection."""

    try:

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:

            raise FileNotFoundError(f"Error loading image: {image_path}")



        # Apply Gaussian blur to reduce noise

        blurred = cv2.GaussianBlur(image, (5, 5), 0)



        # Apply Canny edge detection

        edges = cv2.Canny(blurred, 50, 150)

        return edges

    except Exception as e:

        raise RuntimeError(f"Error processing image {image_path}: {e}")



def calculate_mse(image1, image2):

    """Compute Mean Squared Error (MSE) between two images."""

    if image1.shape != image2.shape:

        raise ValueError("Images must have the same dimensions for comparison.")



    err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)

    err /= float(image1.shape[0] * image1.shape[1])

    return err



def compare_images(image_path1, image_path2):

    """Compare two images using SSIM and MSE."""

    img1 = load_and_preprocess_image(image_path1)

    img2 = load_and_preprocess_image(image_path2)



    # Compute SSIM

    ssim_score = ssim(img1, img2, data_range=img2.max() - img2.min())



    # Compute MSE

    mse_score = calculate_mse(img1, img2)



    return ssim_score, mse_score


if __name__ == "__main__":

    image_path1 = "IMG_9332.JPG"  # Change to your image path

    image_path2 = "IMG_9335.JPG"  # Change to your image path



    try:

        ssim_score, mse_score = compare_images(image_path1, image_path2)

        print(f"SSIM Score: {ssim_score:.4f}")

        print(f"MSE Score: {mse_score:.4f}")

    except (ValueError, FileNotFoundError, RuntimeError) as e:

        print(f"Error: {e}")