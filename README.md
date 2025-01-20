# Straw-hat - Secure File Transfer

This project implements a secure file transfer system using encryption and basic device discovery.

## Features

* **Encryption:** Encrypts files before sending them to the receiver using AES-256 encryption.
* **Device Discovery:** Discovers devices on the same network using ping sweeps.
* **Cross-Platform:** Designed to work on Linux, macOS, and Android (with Termux).

## Requirements

* **Linux/macOS:**
    * Python 3
    * `pycryptodome` library (install using `pip install pycryptodome`)
* **Android (Termux):**
    * Termux app
    * Python and `pip` installed in Termux (use `pkg install python python-pip` in Termux)
    * `pycryptodome` library (install using `pip install pycryptodome`)

## Usage

**1. Set up a virtual environment (Linux/macOS only):**

   ```bash
   cd ~/Desktop/Straw-hat  # Go to project directory
   python3 -m venv .venv      # Create virtual environment
   source .venv/bin/activate # Activate the virtual environment

# 1 more file for easy to use

## Setup (Linux/macOS)

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd Straw-hat
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install pycryptodome tqdm
    ```

4.  **Run the scripts:**
    ```bash
    # In one terminal (receiver):
    python3 receiver.py

    # In another terminal (sender):
    python3 sender.py
    ```

**Important:** You *must* activate the virtual environment (`source .venv/bin/activate`) in every new terminal you open before running the scripts.