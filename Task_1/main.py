def binary(string):
    s = ''
    for i in range(len(string)):
        n = ord(string[i])
        if n == 0:
            new_b = '0' * 8
        else:
            b = ''
            while n > 0:
                b = str(n % 2) + b
                n = n // 2
            bt = '0' * 8
            new_b = bt[0:8 - len(b)] + b
        s += new_b
    return (s)

def len_file(file):
    with open(file, encoding='utf8') as f:
        size = len(f.readlines())
    return(size)

def code(carrier, result, payload):
    file_in = open(carrier, encoding='utf8')
    file_out = open(result, 'w')
    i = 0
    if len_file(carrier) < len(payload) * 8:
        print('В тексте-контейнере слишком мало строк')
    else:
        new_payload = binary(payload)
        len_new_payload = len(new_payload)
        for line in file_in:
            if (i < len_new_payload):
                sym = ' ' if new_payload[i] == '1' else ''
                i += 1
                str_end = line.find('\n')
                new_line = line[0:str_end] + sym + '\n'
                file_out.write(new_line)
            else:
                file_out.write(line)
    file_out.close()


def decode(file):
    key = ''
    f = open(file)
    for line in f:
        if len(line) != 0:
            key += '1' if line[line.find('\n') - 1] == ' ' else '0'

    string_blocks = (key[i:i + 8] for i in range(0, len(key), 8))
    string = ''.join(chr(int(char, 2)) for char in string_blocks if (char != '0'*8 and len(char) == 8))
    print('Обнаруженный скрытый текст: ' + string)


hidden_text = 'Hello!'
code('text.txt', 'result.txt', hidden_text)
decode('result.txt')
