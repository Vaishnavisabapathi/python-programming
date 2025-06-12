#import section
import cv2
from PIL import Image
import pytesseract

# Set Tesseract command path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(img_path):
    print(f"[INFO] Loading image: {img_path}")
    img = cv2.imread(img_path)

    if img is None:
        print("[ERROR] Image not found!")
        return None

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize to improve accuracy (scale text)
    gray = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)

    # Smooth image using bilateral filter
    blurred = cv2.bilateralFilter(gray, 9, 75, 75)

    # Apply Otsu's thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh

def extract_text(preprocessed_img):
    if preprocessed_img is None:
        return "[ERROR] No image to extract text from."

    pil_img = Image.fromarray(preprocessed_img)

    # Custom OCR config to improve results
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(pil_img, config=custom_config)

    return text

if __name__ == "__main__":
    # Update the image file name here
    image_path = r'C:\Users\nsaba\OneDrive\Pictures\workshop.jpg'

    processed_img = preprocess_image(image_path)
    extracted_text = extract_text(processed_img)

    print("\n----- Extracted Text -----\n")
    print(extracted_text)

    # Save result to file
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(extracted_text)
