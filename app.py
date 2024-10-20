import cv2
import pytesseract
from pytesseract import Output
import re

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to get a binary image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Perform dilation and erosion to remove noise and make the text clearer
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return morph

def extract_text(image_path):
    # Preprocess the image
    processed_img = preprocess_image(image_path)

    # Use pytesseract to extract text data with bounding box information
    data = pytesseract.image_to_data(processed_img, output_type=Output.DICT)

    # Collecting text lines and confidences
    n_boxes = len(data['text'])
    extracted_text = []
    
    for i in range(n_boxes):
        if int(data['conf'][i]) > 60:  # Only consider boxes with a confidence > 60
            extracted_text.append(data['text'][i])

    return ' '.join(extracted_text)

def organize_text(text):
    # Clean up the text
    text = re.sub(r'\s+', ' ', text).strip()

    # Dynamically create a dictionary to organize the data
    organized_data = {}
    current_heading = None

    # Regular expression to identify headings (gland names followed by "gland" or colon)
    heading_pattern = re.compile(r'([A-Z][a-zA-Z\s]+(?:gland|):)')

    # Split the text into words/tokens
    tokens = text.split()

    # Handle common multi-word gland names
    multi_word_glands = ["Pineal gland", "Pituitary gland", "Thyroid and Parathyroid", "Ovary, Placenta"]

    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Handle multi-word gland names
        if i < len(tokens) - 1 and f"{token} {tokens[i+1]}" in multi_word_glands:
            current_heading = f"{token} {tokens[i+1]}"
            organized_data[current_heading] = []
            i += 2  # Skip the next token (as it's part of the gland name)
            continue

        # If token matches the heading pattern, it's a new heading (gland or organ)
        if heading_pattern.match(token):
            current_heading = token.strip(':')  # Remove any trailing colon or space
            organized_data[current_heading] = []  # Create a list for its subheadings
        elif current_heading:  # If we are under a heading, treat this as a subheading (hormone)
            organized_data[current_heading].append(token)

        i += 1

    # Optional: Clean up subheading lists (remove any accidental punctuation or empty items)
    for key, hormones in organized_data.items():
        organized_data[key] = [hormone.strip(',') for hormone in hormones if hormone.strip(',')]

    return organized_data

def main(image_path):
    # Extract text from the image
    extracted_text = extract_text(image_path)

    # Organize the text into a structured format
    organized_text = organize_text(extracted_text)

    return organized_text

# Set your image path
image_path = 'sample.jpeg'

# Get the organized data
organized_data = main(image_path)

# Output the organized data
print(organized_data)
