OCR-based Heading and Subheading Extraction from Images
Project Structure

- app.py: Main Python script that handles image input, preprocesses the image, and extracts text to output a structured dictionary.
- requirements.txt: A list of Python dependencies required to run the project.
- README.md: This file, providing details about the project.

Requirements

1. Python 3.x
2. Required Python packages (specified in requirements.txt):
    - OpenCV (opencv-python)
    - Tesseract-OCR (pytesseract)
    - collections (for structured data organization)
3. Tesseract-OCR installation:
   - Windows: Download and install from https://github.com/tesseract-ocr/tesseract/wiki.
   - Linux: Install using the following command:
     sudo apt install tesseract-ocr
   - Mac: Install using Homebrew:
     brew install tesseract

Installation

1. Clone the repository:

   git clone <repository-url>
   cd ocr-heading-extraction

2. Install the dependencies:

   pip install -r requirements.txt

3. Install Tesseract-OCR as per your operating system instructions (above).

Usage

1. Running the Script:
   Use app.py to process an image and generate a structured dictionary output.

   Example usage:

   python app.py --image path_to_image.jpg

2. Sample Output:
   After running the script, the processed image will generate an output dictionary where headings are keys and sub-items (list) are values.

   Example output:

   {
       "Hypothalamus": ["TRH", "CRH", "GHRH", "Dopamine", "Somatostatin", "Vasopressin"],
       "Pituitary gland": ["GH", "TSH", "ACTH", "FSH", "MSH", "LH"],
       "Thyroid and Parathyroid": ["T3", "T4", "Calcitonin", "PTH"]
   }

Command-Line Arguments

- --image: Path to the input image file.

How It Works

1. Image Preprocessing:
   The image is preprocessed using OpenCV to enhance text quality for OCR. This involves converting the image to grayscale and applying adaptive thresholding for better readability.

2. Text Extraction:
   Tesseract-OCR is applied to extract the text. A custom configuration (--oem 3 --psm 6) is used to ensure accurate text detection, focusing on structured content.

3. Text Organization:
   The text is parsed and organized into a dictionary where headings act as keys, and sub-items under each heading are stored as lists of strings.

Notes

- Accuracy: The accuracy of text extraction depends on the quality of the input image. It is recommended to use images with clear, readable text and good contrast.
- Headings and Subheadings: The script assumes that larger text sizes or specific keywords indicate headings, while smaller, regular text items are treated as sub-items or lists.

Troubleshooting

1. Tesseract Not Found Error:
   If you encounter an error like "Tesseract not found", make sure that Tesseract-OCR is installed and that its executable is added to your system's environment variables.

2. Poor OCR Output:
   If the extracted text is inaccurate:
   - Try enhancing the image quality (increase contrast, crop unnecessary parts).
   - Adjust preprocessing parameters in the code (e.g., try different thresholding techniques).
