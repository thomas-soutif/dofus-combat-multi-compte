import cv2
import pytesseract

# Function to process the image and extract text
def process_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to preprocess the image
    _, binary_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # Perform OCR
    text = pytesseract.image_to_string(binary_img)
    return text

def find_word_and_get_position(image, word):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # Perform OCR
    data = pytesseract.image_to_data(binary_img, output_type=pytesseract.Output.DICT)
    
    # Loop through each detected word
    for i in range(len(data['text'])):
        if word.lower() in data['text'][i].lower():
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]
            return (x + w//2, y + h//2)  # Return the center of the word
    return None