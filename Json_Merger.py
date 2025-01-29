import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_txt_to_json(input_path, output_directory):
    # Check file extension
    if not input_path.endswith('.txt'):
        raise ValueError("Only .txt files are supported.")

    # Read the input file
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"The specified file was not found: {input_path}")

    # Determine the main key
    main_key = os.path.splitext(os.path.basename(input_path))[0]

    # Process the data and convert to JSON format
    data = {}
    for line in lines:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            data[key.strip()] = value.strip()

    # Create the JSON structure
    json_data = {main_key: data}

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Define the output file path
    output_file = os.path.join(output_directory, f"{main_key}.json")

    # Write to the JSON file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False)

    return output_file

def merge_json_files(input_directory, output_file):
    # Check if the input directory exists
    if not os.path.isdir(input_directory):
        raise FileNotFoundError(f"The specified directory was not found: {input_directory}")

    merged_data = {}

    # Iterate through all JSON files in the directory
    for file_name in os.listdir(input_directory):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_directory, file_name)
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                merged_data.update(data)

    # Write the merged data to the output file
    with open(output_file, 'w', encoding='utf-8') as json_output:
        json.dump(merged_data, json_output, ensure_ascii=False)

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
        result_file = convert_txt_to_json(input_path, output_directory)
        messagebox.showinfo("Success", f"JSON file created: {result_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_merge_directory():
    directory_path = filedialog.askdirectory()
    merge_input_path_entry.delete(0, tk.END)
    merge_input_path_entry.insert(0, directory_path)

def browse_merge_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    merge_output_path_entry.delete(0, tk.END)
    merge_output_path_entry.insert(0, file_path)

def merge_files():
    input_directory = merge_input_path_entry.get()
    output_file = merge_output_path_entry.get()
    try:
        result_file = merge_json_files(input_directory, output_file)
        messagebox.showinfo("Success", f"Merged JSON file created: {result_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter GUI
root = tk.Tk()
root.title("TXT to JSON Converter")

# Input file selection
tk.Label(root, text="TXT File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
input_path_entry = tk.Entry(root, width=50)
input_path_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=10)

# Output directory selection
tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
output_path_entry = tk.Entry(root, width=50)
output_path_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_directory).grid(row=1, column=2, padx=10, pady=10)

# Convert button
tk.Button(root, text="Convert", command=convert_file).grid(row=2, column=0, columnspan=3, pady=20)

# Merge JSON files section
tk.Label(root, text="Merge JSON Directory:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
merge_input_path_entry = tk.Entry(root, width=50)
merge_input_path_entry.grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_merge_directory).grid(row=3, column=2, padx=10, pady=10)

tk.Label(root, text="Merged Output File:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
merge_output_path_entry = tk.Entry(root, width=50)
merge_output_path_entry.grid(row=4, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_merge_output_file).grid(row=4, column=2, padx=10, pady=10)

tk.Button(root, text="Merge", command=merge_files).grid(row=5, column=0, columnspan=3, pady=20)

# Keep the application running
root.mainloop()