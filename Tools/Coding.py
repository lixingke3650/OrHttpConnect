# !usr/bin/python
# -*-coding: utf-8-*-
# Filename: Coding.py

# std
import base64


class Base64():
    '''BASE64编解码'''

    # base64.b64encode 参数必须是byte型，返回值是byte型
    # base64.b64decode 参数可以是byte或string型，返回值是byte型

    def enBase64_s2b(str, coding = 'utf8'):
        '''Encode a string using Base64'''
        return base64.b64encode(str.encode(coding))

    def deBase64_s2b(str, coding = 'utf8'):
        '''Decode a Base64 encoded string'''
        return base64.b64decode(str)

    def enBase64_b2s(byte, coding = 'utf8'):
        '''Encode a string using Base64'''
        return base64.b64encode(byte).decode(coding)

    def deBase64_b2s(byte, coding = 'utf8'):
        '''Decode a Base64 encoded string'''
        return base64.b64decode(byte).decode(coding)

    def enBase64_s2s(str, coding = 'utf8'):
        '''Encode a string using Base64'''
        return base64.b64encode(str.encode(coding)).decode(coding)

    def deBase64_s2s(str, coding = 'utf8'):
        '''Decode a Base64 encoded string'''
        return base64.b64decode(str).decode(coding)

    def enBase64_b2b(byte, coding = 'utf8'):
        '''Encode a string using Base64'''
        return base64.b64encode(byte)

    def deBase64_b2b(byte, coding = 'utf8'):
        '''Decode a Base64 encoded string'''
        return base64.b64decode(byte)

# 以下为测试代码
if (__name__ == '__main__') :
    strstr = 'lixingke3650'
    strstr_b = b'lixingke3650' # strstr.encode('utf8')

    print ('======= string to string =======')
    en = Base64.enBase64_s2s(strstr)
    print (en)
    de = Base64.deBase64_s2s(en)
    print (de)

    print ('\n======= byte to byte =======')
    en = Base64.enBase64_b2b(strstr_b)
    print (en)
    de = Base64.deBase64_b2b(en)
    print (de)

    print ('\n======= string to byte to string =======')
    en = Base64.enBase64_s2b(strstr)
    print (en)
    de = Base64.deBase64_b2s(en)
    print (de)

    print ('\n======= byte to string to byte =======')
    en = Base64.enBase64_b2s(strstr_b)
    print (en)
    de = Base64.deBase64_s2b(en)
    print (de)
