import codecs

def rot_encode(text, s):
    result = ""
    exception_list = [' ', '!', '?', '.', ',', ':', ';', "'", '"', '(', ')', '[', ']', '{', '}', '\\', '/', '|', '_', '-', '=', '+', '*', '&', '^', '%', '$', '#', '@', '~', '`', '<', '>', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for ch in text:
        if ch.isascii() and ch not in exception_list:
            if ch.isupper():
                result += chr((ord(ch) + s - 65) % 26 + 65)
            else:
                result += chr((ord(ch) + s - 97) % 26 + 97)
        else:
            result += ch
    return result


def utf8_to_hex(s):
    return codecs.encode(s.encode('utf-8'), 'hex').decode('utf-8')


def hex_to_utf8(s):
    return codecs.decode(s, 'hex').decode('utf-8')


def hex_to_base64(s):
    return codecs.encode(codecs.decode(s, 'hex'), 'base64').decode('utf-8')


def base64_to_hex(s):
    return codecs.encode(codecs.decode(s, 'base64'), 'hex').decode('utf-8')


def base64_to_utf8(s):
    return codecs.decode(s, 'base64').decode('utf-8')


def utf8_to_base64(s):
    return codecs.encode(s.encode('utf-8'), 'base64').decode('utf-8')


def rot13(s):
    return rot_encode(s, 13)
