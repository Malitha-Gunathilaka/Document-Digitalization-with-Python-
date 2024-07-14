import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract
import csv
import os

# Path to the tesseract executable (if not in PATH, specify the full path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Change this to the path where Tesseract-OCR is installed

class ImageTextExtractorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Text Extractor")
        self.geometry("400x200")
        self.configure(bg="#f0f0f0")

        self.image_paths = []

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Image Text Extractor", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        self.select_button = tk.Button(self, text="Select Images", command=self.select_images, width=20, height=2, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.select_button.pack(pady=10)

        self.extract_button = tk.Button(self, text="Extract Text and Save to CSVs", command=self.extract_text, width=25, height=2, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"))
        self.extract_button.pack(pady=10)

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
        if self.image_paths:
            messagebox.showinfo("Selected Images", f"{len(self.image_paths)} images selected.")

    def extract_text(self):
        if not self.image_paths:
            messagebox.showwarning("No Images Selected", "Please select images first.")
            return

        save_directory = filedialog.askdirectory()
        if not save_directory:
            messagebox.showwarning("No Directory Selected", "Please select a directory to save the CSV files.")
            return

        for image_path in self.image_paths:
            try:
                image = Image.open(image_path)
                extracted_text = pytesseract.image_to_string(image)
                base_name = os.path.basename(image_path)
                csv_file_name = os.path.splitext(base_name)[0] + '.csv'
                csv_file_path = os.path.join(save_directory, csv_file_name)
                with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Extracted Text'])
                    writer.writerow([extracted_text])
                messagebox.showinfo("Success", f"The extracted text from {base_name} has been saved to {csv_file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {image_path}: {e}")

if __name__ == "__main__":
    app = ImageTextExtractorApp()
    app.mainloop()
