from PIL import Image
import pytesseract
import csv

# Path to the tesseract executable (if not in PATH, specify the full path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  
# Change this to the path where Tesseract-OCR is installed

# Load an image from file
image_path = 'image3.png'  # Replace with the path to your image
image = Image.open(image_path)

# Use Tesseract to do OCR on the image
extracted_text = pytesseract.image_to_string(image)

# Print the extracted text
print(extracted_text)

# Save the extracted text to a CSV file
csv_file_path = 'extracted_text.csv'
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Extracted Text'])
    writer.writerow([extracted_text])

print(f'The extracted text has been saved to {csv_file_path}')