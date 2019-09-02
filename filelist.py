from os import listdir
import os

files_terminals = listdir(os.path.join(os.getcwd(), 'terminals'))
terminal_file_list = []

for filename in files_terminals:
    if filename.endswith('xml'):
        filelabels = filename.split('.')
        filenumber = filelabels[0]
        filewho = filelabels[1]
        filetype = filelabels[2]
        if filenumber not in terminal_file_list:
            terminal_file_list.append(filenumber)

for swnum in terminal_file_list:
    print swnum

