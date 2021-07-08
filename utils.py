import os

docstring = """
Master Password Generator for FSI laptops (hexadecimal digits version)
Copyright (C) 2009 dogbert <dogber1@gmail.com>

After entering the wrong password for the third time, you will receive a
hexadecimal code from which the master password can be calculated,
e.g. 0A1B2D3E or AAAA-BBBB-CCCC-DEAD-BEEF
"""


# d'oh
def generate_crc_16_table():
    table = []
    for i in range(0, 256):
        crc = (i << 8)
        for j in range(0, 8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = (crc << 1)
        table.append(crc & 0xFFFF)
    return table


# D'OH
def calculate_hash(word, table_in):
    hash = 0
    for c in word:
        d = table_in[(ord(c) ^ (hash >> 8)) % 256]
        hash = ((hash << 8) ^ d) & 0xFFFF
    return hash


def hash_to_string(hash_in):
    return (chr(ord('0') + ((hash_in >> 12) % 16) % 10) + chr(
        ord('0') + ((hash_in >> 8) % 16) % 10) + chr(
        ord('0') + ((hash_in >> 4) % 16) % 10) + chr(ord('0') + ((hash_in >> 0) % 16) % 10))


def decrypt_code(code, table_in):
    return hash_to_string(calculate_hash(code[0:4], table_in)) + hash_to_string(
        calculate_hash(code[4:8], table_in))


def get_password(code):
    code = code.replace('-', '')
    if len(code) == 20:
        code = code[12:20]
    return decrypt_code(code, table_static)


table_static = generate_crc_16_table()


if __name__ == '__main__':
    print(docstring)
    print("Please enter the code: ")
    in_code = input().replace('-', '')
    if len(in_code) == 20:
        in_code = in_code[12:20]
    table = generate_crc_16_table()
    password = decrypt_code(in_code.upper(), table)
    print("")
    print("The master password is: " + password)
    if os.name == 'nt':
        print("Press a key to exit...")
        input()
