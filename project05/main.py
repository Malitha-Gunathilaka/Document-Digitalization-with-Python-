import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog, Text
import pandas as pd
from PIL import Image, ImageTk

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_information_from_image(image_path, psm_mode):
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Perform OCR using Tesseract with specified PSM mode
    extracted_text = pytesseract.image_to_string(gray, lang='eng', config=f'--oem 3 --psm {psm_mode}')

    # Extract relevant information based on PSM mode
    lines = extracted_text.split('\n')
    bill_address = ''
    ship_address = ''
    invoice_number = ''
    amount = ''

    for line in lines:
        line = line.strip()
        if 'Bill address' in line or 'Bill Addr' in line or 'Billing Address' in line:
            bill_address = line.replace('Bill address', '').strip()
        elif 'Ship address' in line or 'Ship Addr' in line or 'Shipping Address' in line:
            ship_address = line.replace('Ship address', '').strip()
        elif 'Invoice no' in line or 'Invoice Number' in line:
            invoice_number = line.replace('Invoice no', '').strip()
        elif 'Amount' in line or 'Total' in line:
            amount = line.replace('Amount', '').replace('Total', '').strip()

    return bill_address, ship_address, invoice_number, amount

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        text_box.delete("1.0", tk.END)
        psm_mode = psm_var.get()  # Get selected PSM mode
        bill_address, ship_address, invoice_number, amount = extract_information_from_image(file_path, psm_mode)
        text_box.insert(tk.END, f"Bill address: {bill_address}\n")
        text_box.insert(tk.END, f"Ship address: {ship_address}\n")
        text_box.insert(tk.END, f"Invoice no: {invoice_number}\n")
        text_box.insert(tk.END, f"Amount: {amount}\n")

def save_to_csv():
    bill_address = text_box.get("1.0", tk.END).split("Bill address: ")[1].split("\n")[0].strip()
    ship_address = text_box.get("1.0", tk.END).split("Ship address: ")[1].split("\n")[0].strip()
    invoice_number = text_box.get("1.0", tk.END).split("Invoice no: ")[1].split("\n")[0].strip()
    amount = text_box.get("1.0", tk.END).split("Amount: ")[1].split("\n")[0].strip()

    df = pd.DataFrame({
        "Bill address": [bill_address],
        "Ship address": [ship_address],
        "Invoice no": [invoice_number],
        "Total": [amount]
    })

    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if save_path:
        df.to_csv(save_path, index=False)

# Set up the main application window
root = tk.Tk()
root.title("Extract Information from Image")

# Create and place a text box to display the extracted information
text_box = Text(root, wrap='word', height=15, width=50)
text_box.pack(pady=10)

# Create buttons to open image and save information to CSV
open_button = tk.Button(root, text="Select Image", command=open_image)
open_button.pack(side='left', padx=10)

save_button = tk.Button(root, text="Save to CSV", command=save_to_csv)
save_button.pack(side='right', padx=10)

# Option to select OCR PSM mode
psm_var = tk.IntVar(value=3)  # Default PSM mode
tk.Label(root, text="Select OCR PSM Mode:").pack()
tk.Radiobutton(root, text="Auto (Default)", variable=psm_var, value=3).pack(anchor='w')
tk.Radiobutton(root, text="Single column", variable=psm_var, value=4).pack(anchor='w')
tk.Radiobutton(root, text="Single block (vertical)", variable=psm_var, value=6).pack(anchor='w')
tk.Radiobutton(root, text="Single line", variable=psm_var, value=7).pack(anchor='w')
tk.Radiobutton(root, text="Single word", variable=psm_var, value=8).pack(anchor='w')

root.mainloop()
