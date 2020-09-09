from password_safe.settings import PASSWORD_KEY

def encrypt(password):
    encrypted = []
    for i, c in enumerate(password):
        key_c = ord(PASSWORD_KEY[i % len(PASSWORD_KEY)])
        msg_c = ord(c)
        encrypted.append(chr((msg_c + key_c) % 127))
    return ''.join(encrypted)

def decrypt(encrypted_password):
    msg = []
    for i, c in enumerate(encrypted_password):
        key_c = ord(PASSWORD_KEY[i % len(PASSWORD_KEY)])
        enc_c = ord(c)
        msg.append(chr((enc_c - key_c) % 127))
    return ''.join(msg)