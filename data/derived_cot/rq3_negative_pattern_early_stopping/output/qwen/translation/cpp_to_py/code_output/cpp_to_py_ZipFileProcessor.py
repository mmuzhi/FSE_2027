import os
import zipfile
from pathlib import Path

class ZipFileInfo:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

class ZipFileProcessor:
    def __init__(self, zip_file_path):
        self.zip_file_path = zip_file_path

    def read_zip_file(self):
        return ZipFileInfo(self.zip_file_path, "r")

    def extract_all(self, output_directory):
        if not output_directory:
            return False

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            try:
                os.makedirs(output_directory)
            except OSError as e:
                print(f"Failed to create output directory: {output_directory}")
                print(e)
                return False

        try:
            with zipfile.ZipFile(self.zip_file_path, 'r') as zipf:
                # Extract all files into the output directory
                zipf.extractall(output_directory)
                return True
        except zipfile.BadZipFile:
            print(f"Error: {self.zip_file_path} is not a valid ZIP file.")
            return False
        except Exception as e:
            print(f"An error occurred while extracting the zip file: {e}")
            return False

    def extract_file(self, file_name, output_directory):
        if not output_directory:
            return False

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            try:
                os.makedirs(output_directory)
            except OSError as e:
                print(f"Failed to create output directory: {output_directory}")
                print(e)
                return False

        try:
            with zipfile.ZipFile(self.zip_file_path, 'r') as zipf:
                # Check if the file exists in the zip
                if file_name not in zipf.namelist():
                    print(f"File not found in zip: {file_name}")
                    return False

                # Extract the specific file
                zipf.extract(file_name, output_directory)
                return True
        except zipfile.BadZipFile:
            print(f"Error: {self.zip_file_path} is not a valid ZIP file.")
            return False
        except Exception as e:
            print(f"An error occurred while extracting the file {file_name}: {e}")
            return False

    def create_zip_file(self, files, output_zip_file):
        try:
            with zipfile.ZipFile(output_zip_file, 'w') as zipf:
                for file_path in files:
                    # Check if the file exists
                    if not os.path.exists(file_path):
                        print(f"Error: File not found: {file_path}")
                        return False

                    # Add the file to the zip
                    zipf.write(file_path, os.path.basename(file_path), zipfile.ZIP_STORED)
            return True
        except Exception as e:
            print(f"An error occurred while creating the zip file: {e}")
            return False

# Example usage:
if __name__ == "__main__":
    processor = ZipFileProcessor("example.zip")
    
    # Test read_zip_file
    info = processor.read_zip_file()
    print(f"Zip File Info: {info.filename}, Mode: {info.mode}")

    # Test extract_all
    if processor.extract_all("output_dir"):
        print("All files extracted successfully.")
    else:
        print("Failed to extract all files.")

    # Test extract_file
    if processor.extract_file("file.txt", "output_dir/file.txt"):
        print("File extracted successfully.")
    else:
        print("Failed to extract file.")

    # Test create_zip_file
    if processor.create_zip_file(["file1.txt", "file2.txt"], "new_archive.zip"):
        print("Zip file created successfully.")
    else:
        print("Failed to create zip file.")