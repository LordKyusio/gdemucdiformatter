import os
import shutil
import glob


def gdi_file_formatter():
    folders = os.listdir(os.curdir)
    supported_formats = ['cdi', 'iso']
    input_files = []
    if 'INPUT' not in folders:
        print('INPUT dir not found. Please make sure that INPUT folder exists')
        return
    if 'OUTPUT' not in folders:
        print('OUTPUT dir not found')
        os.mkdir('OUTPUT')
        print('OUTPUT created in current directory')
    for supported_format in supported_formats:
        input_files += (glob.glob(os.getcwd() + f'/I*/**/*.{supported_format}', recursive=True))

    output_folders = os.listdir(os.curdir + '/OUTPUT')
    output_files = glob.glob(os.getcwd() + '/OUTPUT', recursive=True)

    folder_name = None

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

        os.mkdir('{}/{}'.format(output_files[0], folder_name))
        output_folders = os.listdir(os.curdir + '/OUTPUT')
        file_format = input_files[i][-3:]
        shutil.copy(input_files[i], '{}/{}/{}'.format(output_files[0], folder_name, f"disc.{file_format}"))
        print('Moved {} to {}'.format(input_files[i], f"{output_files[0]}/{folder_name}/{f'disc.{file_format}'}"))
        n += 1


if __name__ == '__main__':
    gdi_file_formatter()
