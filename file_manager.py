import os

def copy_file_into_file(path_from, path_where):
    with open(path_from, 'r') as file_from:
        with open(path_where, 'w') as file_where:
            for line in file_from:
                file_where.write (line)


def copy_directory_into_directory(path_from, path_where):
    list_of_directory = os.listdir(path_from)
    for element in list_of_directory:
        if os.path.isfile(os.path.join(path_from, element)):
            copy_file_into_directory(os.path.join(path_from, element), path_where)
        elif os.path.isdir(os.path.join(path_from, element)):
            if not os.path.isdir(os.path.join(path_where, element)):
                os.mkdir(os.path.join(path_where, element))
            copy_directory_into_directory(os.path.join(path_from, element), os.path.join(path_where, element))

def copy_file_into_directory(path_from, path_where):
    (dirname, filename) = os.path.split(path_from)
    with open(path_from, 'r') as file_from:
        with open(os.path.join(path_where, filename), 'w') as file_where:
            for line in file_from:
                file_where.write (line)

def delete_file(path):
    os.remove(path)

def delete_directory(path):
    list_of_directory = os.listdir(path)
    for element in list_of_directory:
        if os.path.isfile(os.path.join(path, element)):
            delete_file(os.path.join(path, element))
        elif os.path.isdir(os.path.join(path, element)):
            delete_directory(os.path.join(path, element))
    os.rmdir(path)

def create_file(path):
    with open(os.path.join(path), 'w') as file:
        pass

def create_directory(path):
    os.mkdir(path)
    
def move_file_into_directory(path_from, path_where):
    copy_file_into_directory(path_from, path_where)
    delete_file(path_from)
    
def move_directory_into_directory(path_from, path_where):
    copy_directory_into_directory(path_from, path_where)
    delete_directory(path_from)

command = input()
com_spl = command.split()
if com_spl[0]=='copy':
    if not os.path.exists(com_spl[1]):
        print('Error: nothing to copy')    
    elif os.path.isfile(com_spl[1]):
        if os.path.isdir(com_spl[2]):
            copy_file_into_directory(com_spl[1], com_spl[2])
        else:
            copy_file_into_file(com_spl[1], com_spl[2])
    elif os.path.isdir(com_spl[2]):
        copy_directory_into_directory(com_spl[1], com_spl[2])
    else:
        print('Error: cant copy directory into file')
if com_spl[0]=='delete':
    if not os.path.exists(com_spl[1]):
        print('Error: nothing to delete')    
    elif os.path.isfile(com_spl[1]):
        delete_file(com_spl[1])
    else:
        delete_directory(com_spl[1])
if com_spl[0]=='create':
    if os.path.exists(com_spl[1]):
        print('Error: exists')
    elif com_spl[2]=='F':
        create_file(com_spl[1])
    else:
        create_directory(com_spl[1])
if com_spl[0]=='move':
    if not os.path.exists(com_spl[1]):
        print('Error: nothing to move')
    elif os.path.isdir(com_spl[1]):
        if os.path.isdir(com_spl[2]):
            move_directory_into_directory(com_spl[1], com_spl[2])
        else:
            print('''Error: can't move''')
    elif os.path.isdir(com_spl[2]):
        move_file_into_directory(com_spl[1], com_spl[2])
    else:
        print('''Error: can't move file into file''')
    
    