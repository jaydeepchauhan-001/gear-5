# sender.py (Cross-Platform)
import os
import socket
import threading
from queue import Queue
from Crypto.Cipher import AES
import tqdm
import platform

# Encryption Key and Nonce (KEEP THESE SECRET IN REAL APPLICATIONS!)
key = b"CyberGuard1Bytes"  # Must be 16 bytes
nonce = b"CyberGuard1Bytes"  # Must be 16 bytes

cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

def ping_device(ip, results):
    """Ping a device (cross-platform)."""
    print(f"Pinging: {ip}")
    try:
        if platform.system() == "Windows":
            response = os.system(f"ping -n 1 -w 2 {ip} >nul 2>&1")  # Windows
        else:  # Linux/macOS (including Kali)
            response = os.system(f"ping -c 1 -W 2 {ip} > /dev/null 2>&1")  # Linux/macOS
        if response == 0:
            results.put(ip)
    except Exception as e:
        print(f"Ping error: {e}") # Handle potential ping errors

def discover_devices(subnet):
    """Discover devices using threaded ping sweep."""
    print("Discovering devices...")
    devices = []
    results = Queue()
    threads = []

    for i in range(1, 255):
        ip = f"{subnet}{i}"
        thread = threading.Thread(target=ping_device, args=(ip, results,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    while not results.empty():
        devices.append(results.get())

    return devices

def forward_file(file_name, file_data, target_ip):
    """Forward the file."""
    print(f"Forwarding to {target_ip}...")
    file_size = len(file_data)

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, 5000))

        metadata = f"{file_name}|{file_size}".encode('utf-8')
        client.sendall(metadata) # Use sendall to ensure all metadata is sent
        ack = client.recv(1024).decode('utf-8')
        if ack != "ACK":
            raise Exception("Did not receive ACK from receiver.")
        client.sendall(file_data)
        client.sendall(b"<END>") # Use sendall here as well
        client.close()
        print(f"Forwarded to {target_ip}.")
    except ConnectionRefusedError:
        print(f"Connection to {target_ip} refused. Is the receiver running?")
    except Exception as e:
        print(f"Error forwarding: {e}")

def get_subnet():
    """Gets the subnet from the user."""
    while True:
        subnet = input("Enter your network subnet (e.g., 192.168.1.): ").strip()
        if subnet and subnet[-1] == '.':
            return subnet
        print("Invalid subnet format. Use 'xxx.xxx.xxx.'")

def main():
    file_name = input("Enter the file name to send: ").strip()
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"File '{file_name}' not found.")

    with open(file_name, "rb") as f:
        file_data = f.read()
    encrypted_data = cipher.encrypt(file_data)

    subnet = get_subnet()
    devices = discover_devices(subnet)

    if devices:
        print("Devices discovered:")
        for i, ip in enumerate(devices):
            print(f"{i + 1}. {ip}")

        while True:
            try:
                forward_indices = input("Enter device numbers (comma-separated): ").strip()
                forward_indices = [int(x.strip()) - 1 for x in forward_indices.split(',')]
                for idx in forward_indices:
                    if 0 <= idx < len(devices):
                        target_ip = devices[idx]
                        forward_file(file_name, encrypted_data, target_ip)
                    else:
                        print(f"Invalid device number: {idx + 1}")
                break
            except (ValueError, IndexError):
                print("Invalid input. Use comma-separated numbers.")
    else:
        print("No devices found. Check subnet, network, firewalls.")

if __name__ == "__main__":
    main()