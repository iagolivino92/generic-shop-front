import os, rsa

from Crypto.Cipher import AES
from dotenv import load_dotenv
load_dotenv()


def main():
    # eax_test()
    # ofb_test()
    # cfb_test()
    rsa_test()


def eax_test():
    data = bytes('any information', 'utf-8')
    key = bytes(os.getenv('AES_KEY'), 'utf-8')
    encrypted = encrypt_eax(key, data)
    print(encrypted)
    print(decrypt_eax(key, encrypted).decode('utf-8'))


def encrypt_eax(key, data):
    nonce = os.getenv("NONCE").encode('utf-8')
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce, tag, ciphertext


def decrypt_eax(key, data):
    nonce, tag, ciphertext = data
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


def ofb_test():
    data = bytes('any information', 'utf-8')
    key = bytes(os.getenv('AES_KEY'), 'utf-8')
    encrypted = encrypt_ofb(key, data)
    print(encrypted)
    print(decrypt_ofb(key, encrypted[0], encrypted[1]))


def encrypt_ofb(key, data):
    cipher = AES.new(key, AES.MODE_OFB)
    cipher_text = cipher.encrypt(data)
    iv = cipher.iv
    return iv, cipher_text


def decrypt_ofb(key, iv, text):
    decrypt_cipher = AES.new(key, AES.MODE_OFB, iv=iv)
    return decrypt_cipher.decrypt(text)


def cfb_test():
    data = 'any information'.encode('utf-8')
    key = os.getenv('AES_KEY').encode('utf-8')
    iv = 'c}YER+tgx>Zf33*+'.encode('utf-8')
    encrypted = encrypt_cfb(key, iv, data)
    print(encrypted)
    print(decrypt_ofb(key, iv, encrypted))


def encrypt_cfb(key, iv, text):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.encrypt(text)


def decrypt_cfb(key, iv, text):
    decrypt_cipher = AES.new(key, AES.MODE_CFB, iv)
    return decrypt_cipher.decrypt(text)


def rsa_test():
    pbc = os.getenv('PUBLIC').split(',')
    public_key = rsa.PublicKey(int(pbc[0].strip()), int(pbc[1].strip()))
    prv = os.getenv('PRIVATE').split(',')
    private_key = rsa.PrivateKey(int(prv[0].strip()), int(prv[1].strip()), int(prv[2].strip()), int(prv[3].strip()), int(prv[4].strip()))
    print(f'public: {public_key}\nprivate: {private_key}')
    data = 'any information'
    encrypted = encrypt_rsa(public_key, data)
    print(f'encrypted: {encrypted}')
    print(f'decrypted: {decrypt_rsa(private_key, encrypted)}')


def encrypt_rsa(public_key, text):
    return rsa.encrypt(text.encode(), public_key)


def decrypt_rsa(private_key, text):
    return rsa.decrypt(text, private_key).decode()


if __name__ == '__main__':
    main()
