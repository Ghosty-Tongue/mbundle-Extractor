# Mbundle Extractor

Mbundle Extractor is a Python script built with tkinter and threading to extract files from an mbundle file based on information stored in a plist file.

## Features

- Extracts files from an mbundle file using data from a plist file.
- Supports threading to improve extraction performance.
- Allows selection of plist file, mbundle file, and output directory through a GUI.

## Requirements

- Python 3.x
- tkinter (standard library)
- xml.etree.ElementTree (standard library)

## Usage

1. **Installation:**
   - Ensure you have Python installed on your system.

2. **Running the Script:**
   - Clone or download the script `mbundle_extractor.py`.
   - Open a terminal or command prompt.
   - Navigate to the directory containing `mbundle_extractor.py`.
   - Run the script by executing the command:
     ```
     python mbundle_extractor.py
     ```

3. **Using the GUI:**
   - Click the "Browse" buttons to select the plist file, mbundle file, and output directory.
   - Once all paths are selected, click the "Extract" button to start the extraction process.
   - A message box will indicate whether the extraction was successful or if there was an error.

## Notes

- This script assumes the plist file (`*.plist`) contains information about the mbundle file (`*.mbundle`) and the files it contains.
- Ensure you have the necessary permissions to read from and write to the selected output directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
