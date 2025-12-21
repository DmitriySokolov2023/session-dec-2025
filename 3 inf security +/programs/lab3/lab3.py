import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import secrets
import math


# алгорим Евклида (расширенный)
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = egcd(b, a % b)
        return g, y1, x1 - (a // b) * y1

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception("Обратного элемента не существует")
    return x % m

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def generate_prime(start, end):
    while True:
        num = secrets.randbelow(end-start)+start
        if is_prime(num):
            return num

def generate_rsa_keys():
    p = generate_prime(100, 200)
    q = generate_prime(200, 300)
    
    while p == q:
        q = generate_prime(200, 300)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while math.gcd(e, phi) != 1:
        e += 2
    d = modinv(e, phi)
    return (e, n), (d, n)

def rsa_encrypt_int(m, e, n):
    return pow(m, e, n)

def rsa_decrypt_int(c, d, n):
    return pow(c, d, n)


def encrypt_file(filepath, public_key):
    with open(filepath, "rb") as f:
        data = f.read()
    m = int.from_bytes(data[:50], "big")
    e, n = public_key
    c = rsa_encrypt_int(m, e, n)
    enc_bytes = c.to_bytes((c.bit_length()+7)//8, "big")
    enc_path = filepath + ".enc"
    with open(enc_path, "wb") as f:
        f.write(enc_bytes)
    return enc_path

def decrypt_file(filepath, private_key):
    with open(filepath, "rb") as f:
        enc_bytes = f.read()
    d, n = private_key
    c = int.from_bytes(enc_bytes, "big")
    m = rsa_decrypt_int(c, d, n)
    dec_bytes = m.to_bytes((m.bit_length()+7)//8, "big")
    dec_path = filepath.replace(".enc","_decrypted.jpg")
    with open(dec_path, "wb") as f:
        f.write(dec_bytes)
    return dec_path



class RSAImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA (часть изображения)")
        self.root.geometry("500x450")
        self.public_key = None
        self.private_key = None
        self.image_path = None
        self.image_label = None

        tk.Button(root, text="Сгенерировать ключи", command=self.create_keys, width=25).pack(pady=10)
        tk.Button(root, text="Открыть изображение", command=self.open_image, width=25).pack(pady=10)
        tk.Button(root, text="Зашифровать", command=self.encrypt_image, width=25).pack(pady=5)
        tk.Button(root, text="Расшифровать", command=self.decrypt_image, width=25).pack(pady=5)

    def create_keys(self):
        self.public_key, self.private_key = generate_rsa_keys()
        messagebox.showinfo("Ключи", f"Ключи сгенерированы!\nПубличный e,n: {self.public_key}\nПриватный d,n: {self.private_key}")

    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.bmp *.jpeg")])
        if not path:
            return
        self.image_path = path
        img = Image.open(path)
        img.thumbnail((300,300))
        photo = ImageTk.PhotoImage(img)
        if self.image_label:
            self.image_label.destroy()
        self.image_label = tk.Label(self.root, image=photo)
        self.image_label.image = photo
        self.image_label.pack(pady=10)

    def encrypt_image(self):
        if not self.image_path or not self.public_key:
            messagebox.showwarning("Ошибка", "Выберите изображение и сгенерируйте ключи")
            return
        enc_path = encrypt_file(self.image_path, self.public_key)
        messagebox.showinfo("Готово", f"Файл зашифрован: {enc_path}")

    def decrypt_image(self):
        path = filedialog.askopenfilename(filetypes=[("Зашифрованные файлы", "*.enc")])
        if not path or not self.private_key:
            messagebox.showwarning("Ошибка", "Выберите файл и сгенерируйте ключи")
            return
        dec_path = decrypt_file(path, self.private_key)
        messagebox.showinfo("Готово", f"Файл расшифрован: {dec_path}")



if __name__ == "__main__":
    root = tk.Tk()
    app = RSAImageApp(root)
    root.mainloop()
