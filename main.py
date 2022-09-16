import os
import shutil
import glob
import typing

"""
I have several propositions regarding this code
(preface - search code by notations like @EX1 to see what I adhere to)

------------------------

First of all, path management is all over the place. os.getcwd() depends on the directory you run in from,
 whilst os.curdir IS A CONSTANT! Extracted from current python release /usr/lib/python3.10/os.py: 
 
   " - os.curdir is a string representing the current directory (always '.') "
   
My proposition is to use the basic trick of settings the dir as an absolute path build from this very file being run.
(example @EX1 below)
if you put main.py in /home/rikkt0r/aaa/main.py from wherever you run this script 
    it will always point to /home/rikkt0r/aaa


------------------------

Other thing, supported formats are constant so how about hoisting them up (global variable simulating application settings) @EX2 below

besides that, I noticed you using the same constants later in the code like:
if file_format in ['cdi', 'iso'] and other use cases

It's kinda error prone. How about creating constants for each type and then use these?


------------------------

@EX3, this fragment of code

glob.glob(os.getcwd() + f'/I*/**/*.{supported_format}', [...]

besides concatenating string instead of using os.path.join( *path ),
using @EX1 I propose something like,

glob.glob(os.path.join(BASE_PATH, 'INPUT', f'/**/*.{supported_format}'), [...]


And then summing up the topic of paths - just do the same everywher else

------------------------

@EX4 - the whole segment from the beginning of the function until line
        output_folders = os.listdir(os.path.join(os.curdir, 'OUTPUT'))
could be a separate function returning a list of input dirs


------------------------

Before reading the remainder of this subsection see all the @EX5 markings in the code.

Now, @EX5 

instead of:
    for i in range(len(input_files)):
        whatever (..., input_files[i])

how about:
    for input_file in input_files):
            whatever (..., input_file)
            
a lot cleaner!


------------------------
@EX6 - just rename variable to whatever meaningful. Or not. Your choice. Because right now, without a comment I can
hardly understand what is happening here and for examle why n>10 matters

Bonus: use if/else instead of fulfilling the whole set theory here with double if check :)

------------------------
If I'm not mistaken whether run on windows or linux python ALWAYS uses slashes instead of backslashes in paths
C:/Users/someone/something.py & /home/someone/something
@EX7 - while path[-1] not in ('/', '\\'):  ===> while not path.endswith('/'):


or the whole crawling through string could be "pythonically" written as:

>>> path = '/a/b/c'
>>> path = '/'.join(path.split('/')[:-1])
>>> path
'/a/b'
>>> path = '/'.join(path.split('/')[:-1])
>>> path
'/a'
>>> path = '/'.join(path.split('/')[:-1])
>>> path
''
>>> path = '/'.join(path.split('/')[:-1])
>>> path
''
>>> path = '/'.join(path.split('/')[:-1])
>>> path
''

------------------------

if os.path.isfile(os.path.join(path, file)) and not any(x in file for x in ('cdi', 'iso')): -- @EX8

"file" variable is a string. so...

I'd propose something in the likes of:

... and not file.endswith(CDI) and not file.endswith(ISO)


You could create an utility function for checking whether string ends with given string

def has_any_suffix(string: str, suffixes: typing.List[str]) -> bool:
    for suffix in suffixes:
        if string.endswith(suffix):
            return True

    return False

and then

... and not has_any_suffix(file, [CDI, ISO]))


If you don't wanna use this function NO PROBLEM! Just format this if statement neatly and you are good. Like so:

    if os.path.isfile(os.path.join(path, file)) \
            and not file.endswith(CDI) \
            and not file.endswith(ISO):  # TODO @EX8
            
            
            
Another option here is to use different approach like so:



if os.path.isfile(os.path.join(path, file)) and not any(x in file for x in ('cdi', 'iso')):  # TODO @EX8
    
    path_args = (output_files[0], folder_name, )
    
    if file.endswith(CDI) or file.endswith(ISO):
        continue  # skip this file in loop
    
    elif file.endswith(GDI):
        path_args += ('disc.gdi',)
        
    # IN ANY OTHER CASE, it will be copied without 'disc.gdi' ending - not sure that was the intention?
        
    shutil.copy(
        os.path.join(path, file),
        os.path.join(*path_args)
    )

    print('Moving GDI file {} from {} to {}'  # em... if its not GDI, then it's not GDI! Misleading print
          .format(file, path, os.path.join(output_files[0], folder_name)))



------------------------

@EX9 - add newlines at the end of code blocks. it adds a lot to readability

"""



# TODO @EX1
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# TODO @EX2
CDI = 'cdi'
ISO = 'iso'
GDI = 'gdi'

# Or even create constant like FORMAT_CDI for better readability

SUPPORTED_FORMATS = (CDI, ISO, GDI)


def gdi_file_formatter():
    # TODO @EX4 - cut here
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
        input_files += (glob.glob(os.getcwd() + f'/I*/**/*.{supported_format}', recursive=True))  # TODO @EX3

    # TODO @EX4 - end here
    output_folders = os.listdir(os.path.join(os.curdir, 'OUTPUT'))
    output_files = glob.glob(os.path.join(os.getcwd(), 'OUTPUT'), recursive=True)

    n = 2  # folder 01 is reserved for GDEMU settings file  # TODO @EX6 - rename "n" to something more meaningful
    for i in range(len(input_files)):  # TODO @EX5 - Should loop through files instead
        if n < 10:
            if '0' + str(n) in output_folders:
                while '0' + str(n) in output_folders:
                    n += 1
            folder_name = '0{}'.format(str(n))
        # TODO @EX9 - newline
        if n >= 10:  # TODO @EX6 - just else ? instead of checking
            if str(n) in output_folders:
                while str(n) in output_folders:
                    n += 1
            folder_name = '{}'.format(str(n))

        os.mkdir(os.path.join(output_files[0], folder_name))
        output_folders = os.listdir(os.path.join(os.curdir, 'OUTPUT'))
        file_format = input_files[i][-3:]  # TODO @EX5 - i used only as list/array index

        if file_format in ['cdi', 'iso']:
            shutil.copy(input_files[i], os.path.join(output_files[0], folder_name, f"disc.{file_format}"))  # TODO @EX5 - same here
            print('Moved {} to {}'
                  .format(input_files[i], os.path.join(output_files[0], folder_name, f'disc.{file_format}')))  # TODO @EX5 - same here
            # TODO @EX9 - newline
        elif file_format in ['gdi']:
            path = input_files[i]  # TODO @EX5 - same here
            while path[-1] not in ('/', '\\'):  # TODO @EX7 - while not path.endswith('/')
                path = path[:-1]  # TODO @EX7 or do it another way... (comment above)
            for file in os.listdir(path):
                if os.path.isfile(os.path.join(path, file)) and not any(x in file for x in ('cdi', 'iso')):  # TODO @EX8
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
