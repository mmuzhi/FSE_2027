import os
import sys
import zipfile

class ZipFileInfo:
    def __init__(self, filename="", mode=""):
        self.filename = filename
        self.mode = mode

class ZipFileProcessor:
    def __init__(self, zip_file_path):
        self.zip_file_path_ = zip_file_path

    def read_zip_file(self):
        archive = self.open_zip_file('r')
        info = ZipFileInfo()
        if archive:
            info.filename = self.zip_file_path_
            info.mode = "r"
            archive.close()
        return info

    def extract_all(self, output_directory):
        if not output_directory:
            return False
        if not self.create_directory_if_not_exists(output_directory):
            return False

        archive = self.open_zip_file('r')
        if not archive:
            return False

        success = True
        for info in archive.infolist():
            output_file_path = output_directory + "/" + info.filename
            if not self.extract_file_from_zip(archive, info, output_file_path):
                success = False

        archive.close()
        return success

    def extract_file(self, file_name, output_directory):
        if not output_directory:
            return False
        if not self.create_directory_if_not_exists(output_directory):
            print(f"Failed to create output directory: {output_directory}", file=sys.stderr)
            return False

        archive = self.open_zip_file('r')
        if not archive:
            return False

        try:
            info = archive.getinfo(file_name)
        except KeyError:
            print(f"File not found in zip: {file_name}", file=sys.stderr)
            archive.close()
            return False

        output_file_path = output_directory + "/" + file_name
        success = self.extract_file_from_zip(archive, info, output_file_path)

        archive.close()
        return success

    def create_zip_file(self, files, output_zip_file):
        try:
            archive = zipfile.ZipFile(output_zip_file, 'w')
        except Exception:
            print(f"Error opening zip file: {output_zip_file}", file=sys.stderr)
            return False

        for file_path in files:
            try:
                archive.write(file_path, file_path)
            except Exception:
                print(f"Error adding file to zip: {file_path}", file=sys.stderr)
                archive.close()
                return False

        try:
            archive.close()
        except Exception:
            print(f"Error closing zip file: {output_zip_file}", file=sys.stderr)
            return False

        return True

    def extract_file_from_zip(self, archive, info, output_file_path):
        try:
            zip_file = archive.open(info.filename)
        except Exception:
            print(f"Failed to open file in zip: {info.filename}", file=sys.stderr)
            return False

        out_file = None
        try:
            out_file = open(output_file_path, 'wb')
        except OSError:
            print(f"Failed to open output file: {output_file_path}", file=sys.stderr)
            zip_file.close()
            return False

        try:
            while True:
                buffer = zip_file.read(4096)
                if not buffer:
                    break
                out_file.write(buffer)
        except Exception:
            print(f"Failed to write to file: {output_file_path}", file=sys.stderr)
            zip_file.close()
            out_file.close()
            return False

        out_file.close()
        zip_file.close()
        return True

    def create_directory_if_not_exists(self, dir_path):
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
                return True
            except OSError:
                return False
        return True

    def open_zip_file(self, mode):
        try:
            return zipfile.ZipFile(self.zip_file_path_, mode)
        except Exception:
            print(f"Failed to open zip file: {self.zip_file_path_}", file=sys.stderr)
            return None