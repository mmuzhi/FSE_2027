import os
import sys
import zipfile
from dataclasses import dataclass


@dataclass
class ZipFileInfo:
    filename: str = ""
    mode: str = ""


class ZipFileProcessor:
    def __init__(self, zip_file_path):
        self._zip_file_path = zip_file_path

    def read_zip_file(self):
        archive = self._open_zip_file("r")
        info = ZipFileInfo()
        if archive is not None:
            info.filename = self._zip_file_path
            info.mode = "r"
            archive.close()
        return info

    def extract_all(self, output_directory):
        if not output_directory:
            return False

        if not self._create_directory_if_not_exists(output_directory):
            return False

        archive = self._open_zip_file("r")
        if archive is None:
            return False

        success = True
        names = archive.namelist()
        num_entries = len(names)
        for i in range(num_entries):
            output_file_path = output_directory + "/" + names[i]
            if not self._extract_file_from_zip(archive, i, output_file_path):
                success = False

        archive.close()
        return success

    def extract_file(self, file_name, output_directory):
        if not output_directory:
            return False

        if not self._create_directory_if_not_exists(output_directory):
            print(f"Failed to create output directory: {output_directory}",
                  file=sys.stderr)
            return False

        archive = self._open_zip_file("r")
        if archive is None:
            return False

        try:
            index = archive.namelist().index(file_name)
        except ValueError:
            print(f"File not found in zip: {file_name}", file=sys.stderr)
            archive.close()
            return False

        output_file_path = output_directory + "/" + file_name
        success = self._extract_file_from_zip(archive, index, output_file_path)

        archive.close()
        return success

    def create_zip_file(self, files, output_zip_file):
        try:
            archive = zipfile.ZipFile(output_zip_file, "w",
                                      compression=zipfile.ZIP_DEFLATED)
        except Exception:
            print(f"Error opening zip file: {output_zip_file}", file=sys.stderr)
            return False

        for file_path in files:
            try:
                # entry name is the full file path, matching zip_file_add
                archive.write(file_path, arcname=file_path)
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

    def _extract_file_from_zip(self, archive, index, output_file_path):
        name = archive.namelist()[index]
        try:
            zfile = archive.open(name)
        except Exception:
            print(f"Failed to open file in zip: {name}", file=sys.stderr)
            return False

        try:
            out_file = open(output_file_path, "wb")
        except OSError:
            print(f"Failed to open output file: {output_file_path}",
                  file=sys.stderr)
            zfile.close()
            return False

        success = True
        try:
            while True:
                try:
                    buffer = zfile.read(4096)
                except Exception:
                    # read error: C++ loop exits and still returns true
                    break
                if not buffer:
                    break
                try:
                    out_file.write(buffer)
                except OSError:
                    print(f"Failed to write to file: {output_file_path}",
                          file=sys.stderr)
                    success = False
                    break
        finally:
            zfile.close()
            out_file.close()

        return success

    def _create_directory_if_not_exists(self, dir_path):
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
                return True
            except OSError:
                return False
        return True

    def _open_zip_file(self, mode="r"):
        try:
            return zipfile.ZipFile(self._zip_file_path, mode)
        except Exception:
            print(f"Failed to open zip file: {self._zip_file_path}",
                  file=sys.stderr)
            return None