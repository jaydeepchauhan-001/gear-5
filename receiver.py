# receiver.py (Cross-Platform)
import socket
import os
from Crypto.Cipher import AES
import tqdm

# Encryption Key and Nonce (MUST MATCH SENDER!)
key = b"CyberGuard1Bytes"
nonce = b"CyberGuard1Bytes"

cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

def main():
    """Listens for file transfers and decrypts received data."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(("0.0.0.0", 5000))
    except OSError as e:
        print(f"Error binding socket: {e}. Port 5000 in use?")
        return
    server.listen(5)
    print("Receiver listening...")

    try:
        client, addr = server.accept()
        print(f"Connection from {addr}")

        metadata = client.recv(1024).decode('utf-8')
        file_name, file_size = metadata.split('|')
        file_size = int(file_size)

        print(f"Receiving {file_name} ({file_size} bytes)")
        client.sendall(b"ACK") # Send ACK back to the sender
        file_bytes = b""
        progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1024, total=file_size)
        while True:
            data = client.recv(1024)
            if b"<END>" in data:
                file_bytes += data.replace(b"<END>", b"")
                break
            file_bytes += data
            progress.update(len(data))

        try:
            decrypted_data = cipher.decrypt(file_bytes)
            with open(f"received_{file_name}", "wb") as f:
                f.write(decrypted_data)
            print(f"File '{file_name}' received and decrypted.")
        except ValueError as e: # Handle decryption errors
            print(f"Decryption error: {e}. Check key/nonce.")
            os.remove(f"received_{file_name}") # Remove corrupted file
        

        client.close()

    except ConnectionResetError:
        print("Connection reset by client.")
    except KeyboardInterrupt:
        print("Receiver stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    main()