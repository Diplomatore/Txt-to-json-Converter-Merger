import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_txt_to_json(input_path, output_directory):
    # Dosya uzantısını kontrol et
    if not input_path.endswith('.txt'):
        raise ValueError("Sadece .txt dosyaları desteklenmektedir.")

    # Giriş dosyasını oku
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Belirtilen dosya bulunamadı: {input_path}")

    # İlk anahtar kelimeyi belirle
    main_key = os.path.splitext(os.path.basename(input_path))[0]

    # Veriyi işleyerek JSON formatına dönüştür
    data = {}
    for line in lines:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            data[key.strip()] = value.strip()

    # JSON yapısını oluştur
    json_data = {main_key: data}

    # Çıkış dizinini oluştur (yoksa)
    os.makedirs(output_directory, exist_ok=True)

    # Çıkış dosyası yolunu belirle
    output_file = os.path.join(output_directory, f"{main_key}.json")

    # JSON dosyasına yaz
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False)

    return output_file

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    input_path_entry.delete(0, tk.END)
    input_path_entry.insert(0, file_path)

def browse_directory():
    directory_path = filedialog.askdirectory()
    output_path_entry.delete(0, tk.END)
    output_path_entry.insert(0, directory_path)

def convert_file():
    input_path = input_path_entry.get()
    output_directory = output_path_entry.get()
    try:
        output_file = convert_txt_to_json(input_path, output_directory)
        messagebox.showinfo("Başarılı", f"JSON dosyası oluşturuldu: {output_file}")
    except Exception as e:
        messagebox.showerror("Hata", str(e))

# Tkinter arayüzü
root = tk.Tk()
root.title("TXT to JSON Converter")

# Giriş dosyası seçimi
tk.Label(root, text="TXT Dosyası:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
input_path_entry = tk.Entry(root, width=50)
input_path_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Gözat", command=browse_file).grid(row=0, column=2, padx=10, pady=10)

# Çıkış dizini seçimi
tk.Label(root, text="Çıkış Dizini:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
output_path_entry = tk.Entry(root, width=50)
output_path_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Gözat", command=browse_directory).grid(row=1, column=2, padx=10, pady=10)

# Dönüştürme butonu
tk.Button(root, text="Dönüştür", command=convert_file).grid(row=2, column=0, columnspan=3, pady=20)

# Uygulamayı açık tut
root.mainloop()