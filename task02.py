import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os

#function to swap and shuffle the pixels
def generate_swap_pattern(key, length):
    np.random.seed(key)
    pattern = np.arange(length)
    np.random.shuffle(pattern)
    return pattern
    
#function for encryption of image
def pixel_swap_encrypt(image_path, key):
    img = Image.open(image_path)
    img_array = np.array(img)
    flat_img = img_array.flatten()
    length = flat_img.shape[0]
    swap_pattern = generate_swap_pattern(key, length)
    encrypted_flat_img = flat_img[swap_pattern]
    encrypted_img_array = encrypted_flat_img.reshape(img_array.shape)
    encrypted_img = Image.fromarray(encrypted_img_array)
    encrypted_img_path = image_path.replace(".", "_encrypted.")
    encrypted_img.save(encrypted_img_path)
    return encrypted_img, encrypted_img_path

#function for decryption of image
def pixel_swap_decrypt(image_path, key):
    img = Image.open(image_path)
    img_array = np.array(img)
    flat_img = img_array.flatten()
    length = flat_img.shape[0]
    swap_pattern = generate_swap_pattern(key, length)
    decrypted_flat_img = np.zeros_like(flat_img)
    decrypted_flat_img[swap_pattern] = flat_img
    decrypted_img_array = decrypted_flat_img.reshape(img_array.shape)
    decrypted_img = Image.fromarray(decrypted_img_array)
    decrypted_img_path = image_path.replace("_encrypted.", "_decrypted.")
    decrypted_img.save(decrypted_img_path)
    return decrypted_img, decrypted_img_path
    
#function for  load_image button
def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        global original_image_path
        original_image_path = file_path
        original_image = Image.open(file_path)
        display_image(original_image)

#function to display image 
def display_image(image):
    image.thumbnail((300, 300))
    img = ImageTk.PhotoImage(image)
    canvas.create_image(150, 150, image=img)
    canvas.image = img

#function for encryption button of image
def encrypt_image():
    if original_image_path:
        key = get_key()
        if key is not None:
            encrypted_img, encrypted_img_path = pixel_swap_encrypt(original_image_path, key)
            display_image(encrypted_img)
            messagebox.showinfo("Encrypted", f"Encrypted image saved to: {encrypted_img_path}")
            
#function for decryption button of image
def decrypt_image():
    if original_image_path:
        key = get_key()
        if key is not None:
            decrypted_img, decrypted_img_path = pixel_swap_decrypt(original_image_path.replace(".", "_encrypted."), key)
            display_image(decrypted_img)
            messagebox.showinfo("Decrypted", f"Decrypted image saved to: {decrypted_img_path}")

def get_key():
    try:
        key = int(entry_key.get())
        return key
    except ValueError:
        messagebox.showerror("Invalid Key", "Please enter a valid integer key.")
        return None

# Setting up the main window
root = tk.Tk()
root.title("Image Encryption Tool")
root.geometry("400x500")

# Adding a canvas to display images
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack(pady=20)

# Adding a label for the key entry
label_key = tk.Label(root, text="Enter encryption key (integer):")
label_key.pack()

# Adding an entry field for the key
entry_key = tk.Entry(root)
entry_key.pack(pady=5)

# Adding buttons
load_button = tk.Button(root, text="Load Image", command=load_image, width=20)
load_button.pack(pady=5)

encrypt_button = tk.Button(root, text="Encrypt Image", command=encrypt_image, width=20)
encrypt_button.pack(pady=5)

decrypt_button = tk.Button(root, text="Decrypt Image", command=decrypt_image, width=20)
decrypt_button.pack(pady=5)

# Running the GUI application
original_image_path = None
root.mainloop()
