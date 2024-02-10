# Performant Programming Cipher App

Welcome to the Performant Programming Cipher App repository! This project showcases an efficient implementation of the XOR cipher algorithm in both Python and C++. It includes a graphical user interface (GUI) for ease of use, as well as demonstrations of the algorithm's performance in different programming languages.

## Overview
The XOR cipher is a simple encryption technique that offers basic encryption capabilities. This application demonstrates how to apply the XOR cipher for encrypting and decrypting text messages. Users can interact with the application through a graphical interface or via the command line, making it accessible for both beginners and advanced users interested in cryptography.

## Features
- **XOR Cipher Implementation**: Encrypt and decrypt messages using the XOR cipher algorithm.
- **Performance Comparison**: Compare the execution speed of the algorithm implemented in Python vs. C++.
- **Graphical User Interface**: A user-friendly GUI for easy interaction with the encryption and decryption functionalities.
- **Command-Line Interface**: For advanced users, the application can be operated via the command line, offering more control and automation capabilities.

## Getting Started
### Prerequisites
- Python 3.x
- C++ Compiler (GCC or any compatible compiler that supports C++11 or later)
- CMake (for building the C++ part of the project)

### Installation
1. Clone the repository
```
git clone https://github.com/DenseLink/PerformantProgramming_Cipher_App.git
```
2. Navigate to the project directory
```
cd PerformantProgramming_Cipher_App
```
3. Build the C++ component
```
cmake .
make
```
4. Run the application
   - For Gui:
     ```
     python cipher_app_gui.py
     ```
   - For CLI:
     ```
     python cipher_app_cli.py
     ```
### Usage
## GUI Mode
Launch the application in GUI mode. The interface allows you to:

- Enter the text you wish to encrypt or decrypt.
- Choose to encrypt or decrypt the message.
- View the output directly in the application window.
## CLI Mode
Run the application in CLI mode with the following syntax:
```
python cipher_app_cli.py [encrypt|decrypt] [message]
```
Replace `[encrypt|decrypt]` with your desired operation and `[message]` with the text you wish to process.
