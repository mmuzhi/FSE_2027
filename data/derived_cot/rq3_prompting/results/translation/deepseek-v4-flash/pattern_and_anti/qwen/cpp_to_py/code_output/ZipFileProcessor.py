import os
import sys
import zipfile
import shutil


class ZipFileInfo:
    def __init__(self, filename="", mode=""):
        self.filename = filename
        self.mode = mode


class ZipFileProcessor:
    def __init__(self, zip_file_path):
        self.zip_file_path_ = zip_file_path

    def read_zip_file(self):
        archive = self.open_zip_file(0)
        info = ZipFileInfo()
        if archive is not None:
            info.filename = self.zip_file_path_
            info.mode = "r"
            try:
                archive.close()
            except OSError:
                pass
        return info

    def extract_all(self, output_directory):
        if not output_directory:
            return False

        if not self.create_directory_if_not_exists(output_directory):
            return False

        archive = self.open_zip_file(0)
        if archive is None:
            return False

        success = True
        try:
            for info in archive.infolist():
                output_file_path = output_directory + "/" + info.filename
                if not self.extract_file_from_zip(archive, info.filename, output_file_path):
                    success = False
        finally:
            try:
                archive.close()
            except OSError:
                pass

        return success

    def extract_file(self, file_name, output_directory):
        if not output_directory:
            return False

        if not self.create_directory_if_not_exists(output_directory):
            print("Failed to create output directory: " + output_directory, file=sys.stderr)
            return False

        archive = self.open_zip_file(0)
        if archive is None:
            return False

        try:
            if file_name not in archive.namelist():
                print("File not found in zip: " + file_name, file=sys.stderr)
                return False

            output_file_path = output_directory + "/" + file_name
            return self.extract_file_from_zip(archive, file_name, output_file_path)
        finally:
            try:
                archive.close()
            except OSError:
                pass

    def create_zip_file(self, files, output_zip_file):
        try:
            archive = zipfile.ZipFile(output_zip_file, "w", zipfile.ZIP_DEFLATED)
        except OSError:
            print("Error opening zip file: " + output_zip_file, file=sys.stderr)
            return False

        try:
            for file_path in files:
                if not os.path.exists(file_path):
                    print("Error adding file to zip: " + file_path, file=sys.stderr)
                    try:
                        archive.close()
                    except OSError:
                        pass
                    return False

                if os.path.isdir(file_path):
                    arcname = file_path
                    if not arcname.endswith("/"):
                        arcname += "/"
                    archive.writestr(arcname, b"")
                else:
                    try:
                        zinfo = zipfile.ZipInfo.from_file(file_path, arcname=file_path)
                        with archive.open(zinfo, "w") as dest:
                            with open(file_path, "rb") as src:
                                shutil.copyfileobj(src, dest, 4096)
                    except OSError:
                        print("Error closing zip file: " + output_zip_file, file=sys.stderr)
                        try:
                            archive.close()
                        except OSError:
                            pass
                        return False

            try:
                archive.close()
            except OSError:
                print("Error closing zip file: " + output_zip_file, file=sys.stderr)
                return False

            return True
        except OSError:
            print("Error closing zip file: " + output_zip_file, file=sys.stderr)
            try:
                archive.close()
            except OSError:
                pass
            return False

    def extract_file_from_zip(self, archive, name, output_file_path):
        try:
            file = archive.open(name, "r")
        except Exception:
            print("Failed to open file in zip: " + name, file=sys.stderr)
            return False

        try:
            try:
                out_file = open(output_file_path, "wb")
            except OSError:
                print("Failed to open output file: " + output_file_path, file=sys.stderr)
                return False

            try:
                while True:
                    try:
                        data = file.read(4096)
                    except Exception:
                        break
                    if not data:
                        break
                    try:
                        out_file.write(data)
                    except OSError:
                        print("Failed to write to file: " + output_file_path, file=sys.stderr)
                        return False
            finally:
                out_file.close()
        finally:
            file.close()

        return True

    def create_directory_if_not_exists(self, dir_path):
        if os.path.exists(dir_path):
            return True
        try:
            os.makedirs(dir_path)
            return True
        except OSError:
            return False

    def open_zip_file(self, flags):
        try:
            return zipfile.ZipFile(self.zip_file_path_, "r")
        except (OSError, zipfile.BadZipFile):
            print("Failed to open zip file: " + self.zip_file_path_, file=sys.stderr)
            return None