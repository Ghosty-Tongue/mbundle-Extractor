import os
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
            print(f"Error: No files found for mbundle file '{mbundle_filename}' in the plist.")
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
            offset = int(file_values[i].findall("integer")[0].text)
            size = int(file_values[i].findall("integer")[1].text)
            
            file_data = mbundle_data[offset:offset+size]
            files_to_extract.append((file_name, file_data))
            
            if len(files_to_extract) >= batch_size:
                process_batch(files_to_extract, bundle_output_dir)
                files_to_extract = []
        
        if files_to_extract:
            process_batch(files_to_extract, bundle_output_dir)
        
        print("Success: Extraction completed successfully")
    
    except Exception as e:
        print(f"Error: Extraction failed: {str(e)}")

def process_batch(files_to_extract, bundle_output_dir):
    for file_name, file_data in files_to_extract:
        output_file_path = os.path.join(bundle_output_dir, file_name)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        attempt = 0
        while attempt < 5:
            with open(output_file_path, 'wb') as output_file:
                output_file.write(file_data)
            
            if os.path.getsize(output_file_path) > 0:
                print(f"Success: Extracted {file_name} successfully")
                break
            else:
                print(f"Warning: {file_name} extracted as zero-byte file, retrying...")
                attempt += 1
        
        if os.path.getsize(output_file_path) == 0:
            print(f"Error: Failed to extract {file_name} correctly after multiple attempts")

def main():
    plist_path = input("Enter the path to the plist file: ")
    mbundle_path = input("Enter the path to the mbundle file: ")
    output_dir = input("Enter the output directory: ")

    if not plist_path or not mbundle_path or not output_dir:
        print("Error: All paths must be provided")
        return
    
    thread = threading.Thread(target=extract_files_from_mbundle, args=(plist_path, mbundle_path, output_dir))
    thread.start()
    thread.join()

if __name__ == "__main__":
    main()
