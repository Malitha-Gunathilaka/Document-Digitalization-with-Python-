import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog, Text
import pandas as pd
from PIL import Image, ImageTk

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path, oem):
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(gray, lang='eng', config=f'--oem {oem}')
    return text

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        text_box.delete("1.0", tk.END)
        extracted_text = extract_text_from_image(file_path, engine_var.get())
        text_box.insert(tk.END, extracted_text)
        # Display the image
        image = Image.open(file_path)
        image.thumbnail((200, 200))
        img = ImageTk.PhotoImage(image)
        panel.config(image=img)
        panel.image = img

def save_to_csv():
    text = text_box.get("1.0", tk.END).strip()
    if text:
        lines = text.split('\n')
        df = pd.DataFrame(lines, columns=["Extracted Text"])
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if save_path:
            df.to_csv(save_path, index=False)

# Set up the main application window
root = tk.Tk()
root.title("OCR with Tesseract and Tkinter")

# Create and place a text box to display the extracted text
text_box = Text(root, wrap='word', height=15, width=50)
text_box.pack(pady=10)

# Create buttons to open image and save text to CSV
open_button = tk.Button(root, text="Select Image", command=open_image)
open_button.pack(side='left', padx=10)

save_button = tk.Button(root, text="Save to CSV", command=save_to_csv)
save_button.pack(side='right', padx=10)

# Option to select OCR engine
engine_var = tk.IntVar(value=3)
tk.Label(root, text="Select OCR Engine:").pack()
tk.Radiobutton(root, text="Legacy (0)", variable=engine_var, value=0).pack(anchor='w')
tk.Radiobutton(root, text="Neural nets LSTM (1)", variable=engine_var, value=1).pack(anchor='w')
tk.Radiobutton(root, text="Legacy + LSTM (2)", variable=engine_var, value=2).pack(anchor='w')
tk.Radiobutton(root, text="Default (3)", variable=engine_var, value=3).pack(anchor='w')

# Panel to display the selected image
panel = tk.Label(root)
panel.pack(pady=10)

root.mainloop()
