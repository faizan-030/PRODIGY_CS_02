import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import random

class ImageEncryptor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryptor/Decryptor")

        self.image = None
        self.encrypted_image = None
        self.decrypted_image = None

        # GUI Elements
        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.encrypt_button = tk.Button(root, text="Encrypt Image", command=self.encrypt_image, state=tk.DISABLED)
        self.encrypt_button.pack()

        self.decrypt_button = tk.Button(root, text="Decrypt Image", command=self.decrypt_image, state=tk.DISABLED)
        self.decrypt_button.pack()

        self.save_button = tk.Button(root, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack()

        self.image_label = tk.Label(root)
        self.image_label.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image = Image.open(file_path)
            self.show_image(self.image)
            self.encrypt_button.config(state=tk.NORMAL)
            self.decrypt_button.config(state=tk.NORMAL if self.encrypted_image else tk.DISABLED)
            self.save_button.config(state=tk.NORMAL if self.encrypted_image or self.decrypted_image else tk.DISABLED)

    def show_image(self, img):
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def encrypt_image(self):
        if not self.image:
            messagebox.showerror("Error", "No image loaded.")
            return

        pixels = np.array(self.image).astype(np.uint32)  # Use a larger data type for calculations
        height, width, _ = pixels.shape

        # Basic encryption: swap random pixels and add a constant
        for _ in range(1000):  # Perform 1000 swaps
            x1, y1 = random.randint(0, height-1), random.randint(0, width-1)
            x2, y2 = random.randint(0, height-1), random.randint(0, width-1)
            pixels[x1, y1], pixels[x2, y2] = pixels[x2, y2], pixels[x1, y1]

        pixels = (pixels + 50) % 256  # Add a constant and wrap around
        self.encrypted_image = Image.fromarray(pixels.astype(np.uint8))
        self.show_image(self.encrypted_image)
        self.save_button.config(state=tk.NORMAL)

    def decrypt_image(self):
        if not self.encrypted_image:
            messagebox.showerror("Error", "No encrypted image to decrypt.")
            return

        pixels = np.array(self.encrypted_image).astype(np.uint32)  # Use a larger data type for calculations
        height, width, _ = pixels.shape

        # Reverse the encryption: swap back the random pixels and subtract the constant
        for _ in range(1000):  # Perform 1000 swaps
            x1, y1 = random.randint(0, height-1), random.randint(0, width-1)
            x2, y2 = random.randint(0, height-1), random.randint(0, width-1)
            pixels[x1, y1], pixels[x2, y2] = pixels[x2, y2], pixels[x1, y1]

        pixels = (pixels - 50) % 256  # Subtract the constant and wrap around
        self.decrypted_image = Image.fromarray(pixels.astype(np.uint8))
        self.show_image(self.decrypted_image)
        self.save_button.config(state=tk.NORMAL)

    def save_image(self):
        if not (self.encrypted_image or self.decrypted_image):
            messagebox.showerror("Error", "No image to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            if self.encrypted_image:
                self.encrypted_image.save(file_path)
            elif self.decrypted_image:
                self.decrypted_image.save(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptor(root)
    root.mainloop()
