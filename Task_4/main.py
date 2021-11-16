alph = 'с е н о в а л б г д ж з и й к м п р т у ф х ц ч ш щ ъ ы ь э ю я . /'.split()
code = '1 2 3 4 5 6 7 81 82 83 84 85 86 87 88 89 80 91 92 93 94 95 96 97 98 99 90 01 02 03 04 05 06 07'.split()

def markEncrypt(text):
    new_text = ''
    for character in text:


        if character.isdigit() or character.isspace():
            new_text += character
        elif character.isalpha() or character == '.' or character == '/':
            if character == 'ё':
                character = 'е'
            i = alph.index(character.lower())
            new_text += code[i]
    return new_text

def markDecrypt(text):
    new_text = ''
    sym = ''
    for character in text:
        if character.isspace():
            new_text += ' '
        else:
            if (character in code and len(sym) == 0):
                new_text += alph[code.index(character)]
            else:
                sym += character
                if sym in code:
                    new_text += alph[code.index(sym)]
                    sym = ''
    return new_text

def atbash(text):
    rus = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    eng = 'abcdefghijklmnopqrstuvwxyz'
    new_text = ''
    sym = ''
    for character in text:
        irus = rus.find(character.lower())
        ieng = eng.find(character.lower())
        if irus > -1:
            sym = rus[32 - irus] if character.islower() else rus[32 - irus].upper()
        elif ieng > -1:
            sym = eng[25 - ieng] if character.islower() else eng[25 - ieng].upper()
        else:
            sym = character
        new_text += sym
    return new_text


print('Шифрование методом марк')
mark_code = markEncrypt('Этот текст должен быть зашифрован методом Марк.')
print(mark_code + '\n')

print('Расшифровка методом марк')
print(markDecrypt(mark_code) + '\n')

print('Шифрование методом атбаш')
atbash_code = atbash('Этот текст должен быть зашифрован методом Атбаш.')
print(atbash_code + '\n')

print('Расшифровка методом атбаш')
print(atbash(atbash_code))


