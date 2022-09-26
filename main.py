import os
import shutil
import glob
import typing

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
OUTPUT_PATH = os.path.join(BASE_PATH, 'OUTPUT')

CDI = 'cdi'
ISO = 'iso'
GDI = 'gdi'


def gdi_file_formatter():
    folders = os.listdir(BASE_PATH)
    supported_formats = (CDI, ISO, GDI)
    input_files = []

    if 'INPUT' not in folders:
        print('INPUT dir not found. Please make sure that INPUT folder exists')
    if 'OUTPUT' not in folders:
        print('OUTPUT dir not found')
        os.mkdir('OUTPUT')
        print('OUTPUT created in current directory')

    for supported_format in supported_formats:
        input_files += glob.glob(os.path.join(BASE_PATH, 'INPUT', f'**/*.{supported_format}'), recursive=True)

    output_folders = os.listdir(OUTPUT_PATH)
    folder_number = 2  # folder 01 is reserved for GDEMU settings file

    for input_file in input_files:
        while str(folder_number).zfill(2) in output_folders:
            folder_number += 1
        folder_name = str(folder_number).zfill(2)
        os.mkdir(os.path.join(OUTPUT_PATH, folder_name))
        output_folders = os.listdir(OUTPUT_PATH)
        file_format = input_file[-3:]

        if file_format in [CDI, ISO]:
            shutil.copy(input_file, os.path.join(OUTPUT_PATH, folder_name, f'disc.{file_format}'))
            print('Moved {} to {}'
                  .format(input_file, os.path.join(OUTPUT_PATH, folder_name, f'disc.{file_format}')))
        elif file_format == GDI:
            path = input_file
            while path[-1] not in ('/', '\\'):
                path = path[:-1]
            for file in os.listdir(path):
                if os.path.isfile(os.path.join(path, file)) and not file.endswith((CDI, ISO)):
                    if file.endswith(GDI):
                        shutil.copy(os.path.join(path, file), os.path.join(OUTPUT_PATH, folder_name, 'disc.gdi'))
                    else:
                        shutil.copy(os.path.join(path, file), os.path.join(OUTPUT_PATH, folder_name))

                    print('Moving GDI file {} from {} to {}'
                          .format(file, path, os.path.join(OUTPUT_PATH, folder_name)))
        else:
            folder_number -= 1
        folder_number += 1


if __name__ == '__main__':
    gdi_file_formatter()
