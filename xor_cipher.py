def xor_encrypt_decrypt(msg:str,key:str)->str:
    return ''.join(chr(ord(c)^ord(key[i%len(key)]))for i,c in enumerate(msg))
