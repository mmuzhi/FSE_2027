def decimal_to_binary(decimal_num):
    if decimal_num >= 0:
        return bin(decimal_num)[2:]
    else:
        return bin(decimal_num & 0xFFFFFFFF)[2:]

def binary_to_decimal(binary_num):
    return int(binary_num, 2)

def decimal_to_octal(decimal_num):
    if decimal_num >= 0:
        return oct(decimal_num)[2:]
    else:
        return oct(decimal_num & 0xFFFFFFFF)[2:]

def octal_to_decimal(octal_num):
    return int(octal_num, 8)

def decimal_to_hex(decimal_num):
    if decimal_num >= 0:
        return hex(decimal_num)[2:]
    else:
        return hex(decimal_num & 0xFFFFFFFF)[2:]

def hex_to_decimal(hex_num):
    return int(hex_num, 16)