import os
import shutil
import glob


def gdi_file_formatter():
    folders = os.listdir(os.curdir)
    supported_formats = ('cdi', 'iso', 'gdi')
    input_files = []
    folder_name = None

    if 'INPUT' not in folders:
        print('INPUT dir not found. Please make sure that INPUT folder exists')
    if 'OUTPUT' not in folders:
        print('OUTPUT dir not found')
        os.mkdir('OUTPUT')
        print('OUTPUT created in current directory')

    for supported_format in supported_formats:
        input_files += (glob.glob(os.getcwd() + f'/I*/**/*.{supported_format}', recursive=True))

    output_folders = os.listdir(os.path.join(os.curdir, 'OUTPUT'))
    output_files = glob.glob(os.path.join(os.getcwd(), 'OUTPUT'), recursive=True)

    n = 2  # folder 01 is reserved for GDEMU settings file
    for i in range(len(input_files)):
        if n < 10:
            if '0' + str(n) in output_folders:
                while '0' + str(n) in output_folders:
                    n += 1
            folder_name = '0{}'.format(str(n))
        if n >= 10:
            if str(n) in output_folders:
                while str(n) in output_folders:
                    n += 1
            folder_name = '{}'.format(str(n))

        os.mkdir(os.path.join(output_files[0], folder_name))
        output_folders = os.listdir(os.path.join(os.curdir, 'OUTPUT'))
        file_format = input_files[i][-3:]

        if file_format in ['cdi', 'iso']:
            shutil.copy(input_files[i], os.path.join(output_files[0], folder_name, f"disc.{file_format}"))
            print('Moved {} to {}'
                  .format(input_files[i], os.path.join(output_files[0], folder_name, f'disc.{file_format}')))
        elif file_format in ['gdi']:
            path = input_files[i]
            while path[-1] not in ('/', '\\'):
                path = path[:-1]
            for file in os.listdir(path):
                if os.path.isfile(os.path.join(path, file)) and not any(x in file for x in ('cdi', 'iso')):
                    if file[-3:] == 'gdi':
                        shutil.copy(os.path.join(path, file), os.path.join(output_files[0], folder_name, 'disc.gdi'))
                    else:
                        shutil.copy(os.path.join(path, file), os.path.join(output_files[0], folder_name))

                    print('Moving GDI file {} from {} to {}'
                          .format(file, path, os.path.join(output_files[0], folder_name)))
        else:
            n -= 1
        n += 1


if __name__ == '__main__':
    gdi_file_formatter()
