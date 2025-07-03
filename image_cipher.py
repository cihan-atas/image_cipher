import cv2
import numpy as np
from Crypto.Cipher import AES
import os

def pad_image(image):
    h, w = image.shape
    pad_h = (16 - (h % 16)) % 16
    pad_w = (16 - (w % 16)) % 16
    padded_image = np.pad(image, ((0, pad_h), (0, pad_w)), mode='constant', constant_values=0)
    return padded_image

def encrypt_ecb(image, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_image = pad_image(image)
    encrypted_bytes = cipher.encrypt(padded_image.tobytes())
    encrypted_image = np.frombuffer(encrypted_bytes, dtype=np.uint8).reshape(padded_image.shape)
    return encrypted_image

def decrypt_ecb_with_validation(encrypted_image, key):
    if len(key) not in [16, 24, 32]:
        raise ValueError("Invalid key for ECB decryption!")
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_bytes = cipher.decrypt(encrypted_image.tobytes())
    decrypted_image = np.frombuffer(decrypted_bytes, dtype=np.uint8).reshape(encrypted_image.shape)
    return decrypted_image

def encrypt_cbc(image, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_image = pad_image(image)
    encrypted_bytes = cipher.encrypt(padded_image.tobytes())
    encrypted_image = np.frombuffer(encrypted_bytes, dtype=np.uint8).reshape(padded_image.shape)
    return encrypted_image

def decrypt_cbc_with_validation(encrypted_image, key, iv):
    if len(key) not in [16, 24, 32] or len(iv) != 16:
        raise ValueError("Invalid key or IV for CBC decryption!")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = cipher.decrypt(encrypted_image.tobytes())
    decrypted_image = np.frombuffer(decrypted_bytes, dtype=np.uint8).reshape(encrypted_image.shape)
    return decrypted_image

def get_valid_choice():
    while True:
        try:
            choice = int(input("Enter your choice: "))
            return choice
        except ValueError:
            print("Please enter a valid number!")

def generate_key():
    while True:
        try:
            key_size = int(input("Select key size (128, 192, 256 bits): "))
            if key_size in [128, 192, 256]:
                key = os.urandom(key_size // 8)
                return key, key_size
            else:
                print("Invalid key size! Please select 128, 192, or 256 bits.")
        except ValueError:
            print("Please enter a valid number!")

def list_keys(prefix):
    keys = [f for f in os.listdir() if f.startswith(prefix) and f.endswith(".bin")]
    if not keys:
        print(f"No {prefix} keys found!")
        return None
    print(f"Available {prefix} keys:")
    for i, key in enumerate(keys):
        print(f"{i + 1}. {key}")
    while True:
        try:
            choice = int(input("Select a key: "))
            if 1 <= choice <= len(keys):
                return keys[choice - 1]
            else:
                print("Invalid selection!")
        except ValueError:
            print("Please enter a valid number!")

def main():
    while True:
        print("\nMenu:")
        print("1. Generate ECB key")
        print("2. Generate CBC key")
        print("3. Save in grayscale")
        print("4. Encrypt with ECB")
        print("5. Encrypt with CBC")
        print("6. Decrypt ECB encrypted image")
        print("7. Decrypt CBC encrypted image")
        print("8. Exit")

        choice = get_valid_choice()

        if choice == 8:
            print("Exiting the program...")
            break

        if choice == 1:
            key_ecb, key_size = generate_key()
            key_name = f"ecb_key_{key_size}.bin"
            with open(key_name, "wb") as f:
                f.write(key_ecb)
            print(f"ECB key saved as {key_name}!")

        elif choice == 2:
            key_cbc, key_size = generate_key()
            iv_cbc = os.urandom(16)
            key_name = f"cbc_key_{key_size}.bin"
            iv_name = f"cbc_iv_{key_size}.bin"
            with open(key_name, "wb") as f:
                f.write(key_cbc)
            with open(iv_name, "wb") as f:
                f.write(iv_cbc)
            print(f"CBC key saved as {key_name} and IV saved as {iv_name}!")

        else:
            file_path = input("Enter the image path: ")
            if not os.path.exists(file_path):
                print("File not found!")
                continue

            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                print("Error loading the image!")
                continue

            base_name = os.path.splitext(os.path.basename(file_path))[0]

            if choice == 3:
                output_name = f"{base_name}.png"
                cv2.imwrite(output_name, image)
                print(f"Saved in grayscale {output_name}!")

            elif choice == 4:
                key_name = list_keys("ecb_key")
                if not key_name:
                    continue
                with open(key_name, "rb") as f:
                    key_ecb = f.read()
                encrypted_ecb = encrypt_ecb(image, key_ecb)
                key_size = key_name.split("_")[2].split(".")[0]
                output_name = f"{base_name}_ecb_{key_size}_encrypted.png"
                cv2.imwrite(output_name, encrypted_ecb)
                print(f"Image encrypted with ECB and saved as {output_name}!")

            elif choice == 5:
                key_name = list_keys("cbc_key")
                if not key_name:
                    continue
                iv_name = key_name.replace("key", "iv")
                if not os.path.exists(iv_name):
                    print(f"IV file {iv_name} not found!")
                    continue
                with open(key_name, "rb") as f:
                    key_cbc = f.read()
                with open(iv_name, "rb") as f:
                    iv_cbc = f.read()
                encrypted_cbc = encrypt_cbc(image, key_cbc, iv_cbc)
                key_size = key_name.split("_")[2].split(".")[0]
                output_name = f"{base_name}_cbc_{key_size}_encrypted.png"
                cv2.imwrite(output_name, encrypted_cbc)
                print(f"Image encrypted with CBC and saved as {output_name}!")

            elif choice == 6:
                key_name = list_keys("ecb_key")
                if not key_name:
                    continue
                with open(key_name, "rb") as f:
                    key_ecb = f.read()
                encrypted_ecb = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                if encrypted_ecb is None:
                    print("Error loading the encrypted image!")
                    continue
                try:
                    decrypted_ecb = decrypt_ecb_with_validation(encrypted_ecb, key_ecb)
                    key_size = key_name.split("_")[2].split(".")[0]
                    output_name = f"{base_name}_ecb_{key_size}_decrypted.png"
                    cv2.imwrite(output_name, decrypted_ecb)
                    print(f"Image decrypted with ECB and saved as {output_name}!")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == 7:
                key_name = list_keys("cbc_key")
                if not key_name:
                    continue
                iv_name = key_name.replace("key", "iv")
                if not os.path.exists(iv_name):
                    print(f"IV file {iv_name} not found!")
                    continue
                with open(key_name, "rb") as f:
                    key_cbc = f.read()
                with open(iv_name, "rb") as f:
                    iv_cbc = f.read()
                encrypted_cbc = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                if encrypted_cbc is None:
                    print("Error loading the encrypted image!")
                    continue
                try:
                    decrypted_cbc = decrypt_cbc_with_validation(encrypted_cbc, key_cbc, iv_cbc)
                    key_size = key_name.split("_")[2].split(".")[0]
                    output_name = f"{base_name}_cbc_{key_size}_decrypted.png"
                    cv2.imwrite(output_name, decrypted_cbc)
                    print(f"Image decrypted with CBC and saved as {output_name}!")
                except ValueError as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    main()
