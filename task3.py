import os
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_image(image_path, key, cipher_mode=AES.MODE_CBC):
    # 1. Open image and convert to RGB
    img = Image.open("input.jpg")
    raw_bytes = img.tobytes()
    
    # 2. Initialize Cipher with a random IV
    iv = os.urandom(16) if cipher_mode != AES.MODE_ECB else b''
    cipher = AES.new(key, cipher_mode, iv) if iv else AES.new(key, cipher_mode)
    
    # 3. Encrypt the raw bytes
    padded_data = pad(raw_bytes, AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_data)
    
    return iv, encrypted_bytes, img.size, img.mode

def save_encrypted_image(iv, encrypted_bytes, size, mode, output_path):
    # Save the encrypted data (IV + Ciphertext) to a new file 
    with open(output_path, 'wb') as f:
        f.write(iv)
        f.write(encrypted_bytes)
    print(f"Encrypted image saved to: {output_path}")

# --- Example Usage ---
if __name__ == "__main__":
    # AES keys must be 16, 24, or 32 bytes long
    secret_key = b'SixteenByteKey12' 
    
    iv, cipher_data, size, mode = encrypt_image("input.jpg", secret_key, AES.MODE_CBC)
    save_encrypted_image(iv, cipher_data, size, mode, "encrypted.bin")