import pytesseract
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import re

# Configure the path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path

def preprocess_image(image_path):
    img = Image.open(image_path)
    # Convert to grayscale
    img = img.convert('L')
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    # Apply a slight blur to smooth out noise
    img = img.filter(ImageFilter.MedianFilter())
    return img

def extract_text(image_path):
    img = preprocess_image(image_path)
    text = pytesseract.image_to_string(img)
    return text

def parse_invoice(text):
    billing_address = shipping_address = invoice_number = total = None

    # Use regular expressions to find fields
    billing_address_match = re.search(r'Bill To[:\s]*(.*)', text, re.IGNORECASE)
    shipping_address_match = re.search(r'Ship To[:\s]*(.*)', text, re.IGNORECASE)
    invoice_number_match = re.search(r'Invoice [:\s]*(.*)', text, re.IGNORECASE)
    total_match = re.search(r'TOTAL[:\s]*\$?(\d+\.\d{2})', text, re.IGNORECASE)

    if billing_address_match:
        billing_address = billing_address_match.group(1).strip()
    if shipping_address_match:
        shipping_address = shipping_address_match.group(1).strip()
    if invoice_number_match:
        invoice_number = invoice_number_match.group(1).strip()
    if total_match:
        total = total_match.group(1).strip()

    return billing_address, shipping_address, invoice_number, total

def save_to_csv(data, output_path='output.csv'):
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Billing Address', 'Shipping Address', 'Invoice Number', 'Total'])
        writer.writerow(data)

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((400, 400))  # Resize for display purposes
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
        
        text = extract_text(file_path)
        billing_address, shipping_address, invoice_number, total = parse_invoice(text)
        
        missing_fields = []
        if not billing_address:
            missing_fields.append("Billing Address")
        if not shipping_address:
            missing_fields.append("Shipping Address")
        if not invoice_number:
            missing_fields.append("Invoice Number")
        if not total:
            missing_fields.append("Total")

        if not missing_fields:
            result_text = (
                f"Billing Address: {billing_address}\n"
                f"Shipping Address: {shipping_address}\n"
                f"Invoice Number: {invoice_number}\n"
                f"Total: {total}"
            )
            result_label.config(text=result_text)
            save_button.config(state=tk.NORMAL)
            global extracted_data
            extracted_data = [billing_address, shipping_address, invoice_number, total]
        else:
            missing_text = "Some fields were not found in the image:\n" + "\n".join(missing_fields)
            messagebox.showwarning("Incomplete Data", missing_text)
            result_label.config(text="")
            save_button.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "No file selected.")

def save_data():
    save_to_csv(extracted_data)
    messagebox.showinfo("Success", "Data extracted and saved to output.csv")
    save_button.config(state=tk.DISABLED)

# Set up the GUI
root = tk.Tk()
root.title("Invoice Data Extractor")

frame = tk.Frame(root)
frame.pack(pady=20)

select_button = tk.Button(frame, text="Select Invoice Image", command=select_image)
select_button.grid(row=0, column=0, padx=10)

image_label = tk.Label(frame)
image_label.grid(row=1, column=0, padx=10, pady=10)

result_label = tk.Label(frame, text="", justify=tk.LEFT, wraplength=400)
result_label.grid(row=2, column=0, padx=10, pady=10)

save_button = tk.Button(frame, text="Save to CSV", command=save_data, state=tk.DISABLED)
save_button.grid(row=3, column=0, padx=10, pady=10)

root.mainloop()
