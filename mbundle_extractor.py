import os
import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
import threading

def extract_files_from_mbundle(plist_path, mbundle_path, output_dir, batch_size=10):
    try:
        tree = ET.parse(plist_path)
        root = tree.getroot()
        
        bundles = root.find('dict').find('array')
        
        mbundle_filename = os.path.basename(mbundle_path)
        
        files_dict = None
        for bundle in bundles.findall('dict'):
            bundle_name = bundle.find("string").text
            if bundle_name == mbundle_filename:
                files_dict = bundle.find("dict")
                break
        
        if not files_dict:
            messagebox.showerror("Error", f"No files found for mbundle file '{mbundle_filename}' in the plist.")
            return
        
        with open(mbundle_path, 'rb') as mbundle_file:
            mbundle_data = mbundle_file.read()
        
            bundle_output_dir = os.path.join(output_dir, os.path.splitext(mbundle_filename)[0])
            if not os.path.exists(bundle_output_dir):
                os.makedirs(bundle_output_dir)
            
            file_keys = files_dict.findall("key")
            file_values = files_dict.findall("dict")
            
            files_to_extract = []
            
            for i in range(len(file_keys)):
                file_name = file_keys[i].text
                offset = int(file_values[i].find("integer").text)
                size = int(file_values[i+1].find("integer").text) - offset
                
                file_data = mbundle_data[offset:offset+size]
                files_to_extract.append((file_name, file_data))
                
                if len(files_to_extract) >= batch_size:
                    thread = threading.Thread(target=process_batch, args=(files_to_extract, bundle_output_dir))
                    thread.start()
                    thread.join()
                    files_to_extract = []
            
            if files_to_extract:
                thread = threading.Thread(target=process_batch, args=(files_to_extract, bundle_output_dir))
                thread.start()
                thread.join()
        
        messagebox.showinfo("Success", "Extraction completed successfully")
    
    except Exception as e:
        messagebox.showerror("Error", f"Extraction failed: {str(e)}")

def process_batch(files_to_extract, bundle_output_dir):
    for file_name, file_data in files_to_extract:
        output_file_path = os.path.join(bundle_output_dir, file_name)
        with open(output_file_path, 'wb') as output_file:
            output_file.write(file_data)
        
        # Check if the file is valid (exists and has non-zero size)
        if not os.path.exists(output_file_path) or os.path.getsize(output_file_path) == 0:
            # Re-extract the file
            print(f"Invalid file: {file_name}. Re-extracting from mbundle.")
            with open(mbundle_path, 'rb') as mbundle_file:
                mbundle_data = mbundle_file.read()
                offset = int(file_values[file_keys.index(file_name) + 1].find("integer").text)
                size = int(file_values[file_keys.index(file_name) + 2].find("integer").text) - offset
                file_data = mbundle_data[offset:offset+size]
            
            # Write the correct file data
            with open(output_file_path, 'wb') as output_file:
                output_file.write(file_data)
        
        print(f'Extracted {file_name} to {output_file_path}')

root = tk.Tk()
root.title("Mbundle Extractor")

plist_path = tk.StringVar()
mbundle_path = tk.StringVar()
output_dir = tk.StringVar()

def select_plist():
    plist_path.set(filedialog.askopenfilename(filetypes=[("Plist files", "*.plist")]))
    
def select_mbundle():
    mbundle_path.set(filedialog.askopenfilename(filetypes=[("Mbundle files", "*.mbundle")]))

def select_output_dir():
    output_dir.set(filedialog.askdirectory())

def run_extraction():
    if not plist_path.get() or not mbundle_path.get() or not output_dir.get():
        messagebox.showerror("Error", "All paths must be provided")
        return
    
    thread = threading.Thread(target=extract_files_from_mbundle, args=(plist_path.get(), mbundle_path.get(), output_dir.get()))
    thread.start()

tk.Label(root, text="Plist File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(root, textvariable=plist_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_plist).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Mbundle File:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
tk.Entry(root, textvariable=mbundle_path, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_mbundle).grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Output Directory:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
tk.Entry(root, textvariable=output_dir, width=50).grid(row=2, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_output_dir).grid(row=2, column=2, padx=10, pady=10)

tk.Button(root, text="Extract", command=run_extraction).grid(row=3, columnspan=3, padx=10, pady=20)

root.mainloop()
