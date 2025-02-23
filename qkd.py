import binascii
import secrets
import logging
from datetime import datetime
from typing import List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Convert string to binary (UTF-8 encoding)
def string_to_utf8_binary(message: str) -> str:
    """Convert a UTF-8 encoded string to a binary string."""
    utf8_bytes = message.encode('utf-8')
    return ''.join(format(byte, '08b') for byte in utf8_bytes)

# Convert binary string back to UTF-8 string
def binary_to_utf8_string(binary_string: str) -> str:
    """Convert a binary string back to a UTF-8 encoded string."""
    byte_list = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
    byte_array = bytearray(int(byte, 2) for byte in byte_list)
    return byte_array.decode('utf-8')

# XOR two binary strings (bitwise XOR)
def xor_binaries(bin_str1: str, bin_str2: str) -> str:
    """Perform a bitwise XOR operation on two binary strings."""
    return ''.join(str(int(b1) ^ int(b2)) for b1, b2 in zip(bin_str1, bin_str2))

# Generate a random key in binary format with the same length as the message
def generate_random_key(message: str) -> str:
    """Generate a random binary key of the same length as the given message."""
    binary_message = string_to_utf8_binary(message)
    num_bits = len(binary_message)
    random_bytes = secrets.token_bytes((num_bits + 7) // 8)
    return ''.join(format(byte, '08b') for byte in random_bytes)[:num_bits]

# Generate a random basis string (for Alice) with 'x' and '+' bases
def generate_basis_string(length: int) -> str:
    """Generate a random basis string of given length using 'x' and '+'."""
    return ''.join(secrets.choice(['x', '+']) for _ in range(length))

# Eve's attempt to intercept and measure the qubits
def eve_interception(alice_key: str, alice_basis: str) -> Tuple[str, str]:
    """Simulate Eve's interception of the qubits."""
    eve_key = []
    eve_basis_string = ''

    for i in range(len(alice_key)):
        eve_basis_choice = secrets.choice(['x', '+'])
        eve_key.append(alice_key[i] if eve_basis_choice == alice_basis[i] else secrets.choice(['0', '1']))
        eve_basis_string += eve_basis_choice

    return ''.join(eve_key), eve_basis_string

# Bob measures the qubits after Eve's interception
def generate_bob_key(eve_key: str, alice_basis: str) -> Tuple[str, str]:
    """Generate Bob's key based on Eve's intercepted key and Alice's basis."""
    bob_key = []
    bob_basis_string = ''

    for i in range(len(eve_key)):
        bob_basis_choice = secrets.choice(['x', '+'])
        bob_key.append(eve_key[i] if bob_basis_choice == alice_basis[i] else secrets.choice(['0', '1']))
        bob_basis_string += bob_basis_choice

    return ''.join(bob_key), bob_basis_string

# Find correct bits where Alice's, Eve's, and Bob's bases match
def find_matching_bases(alice_basis: str, eve_basis: str, bob_basis: str) -> List[int]:
    """Find indices where Alice's, Eve's, and Bob's bases match."""
    return [i for i in range(len(alice_basis)) if alice_basis[i] == bob_basis[i] == eve_basis[i]]

def key_changer(correct_indices: List[int], alice_key: str, bob_key: str) -> Tuple[str, str]:
    """Create new keys for Alice and Bob based on matching bases."""
    new_alice_key = ''.join(alice_key[i] for i in correct_indices)
    new_bob_key = ''.join(bob_key[i] for i in correct_indices)
    return new_alice_key, new_bob_key

def percentage_correct(correct_indices: List[int], total_length: int) -> float:
    """Calculate the percentage of correct bits."""
    return (len(correct_indices) / total_length * 100) if total_length > 0 else 0.0

# Function to calculate the percentage of matching bits without Eve's interception
def percentage_correct_no_eve(alice_key: str, bob_key: str, correct_indices: List[int]) -> float:
    """Calculate the percentage of correct bits without Eve's interception."""
    return percentage_correct(correct_indices, len(alice_key))

# Log the results to a text file
def log_results(data: str, log_file: str = "qkd_log.txt") -> None:
    """Log the data to a specified file."""
    try:
        with open(log_file, 'a') as file:
            file.write(data)
    except IOError as e:
        logging.error(f"Error writing to log file: {e}")

# Main function to run the protocol and log data
def main() -> None:
    """Main function to execute the QKD protocol."""
    # Input message from the user
    message = input('Enter a message (UTF-8 supported): ')
    
    # Get timestamp for the current iteration
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Convert message to binary
    message_binary = string_to_utf8_binary(message)
    
    # Generate Alice's random key and basis
    alice_key = generate_random_key(message)
    alice_basis = generate_basis_string(len(message_binary))

    # Eve intercepts the key exchange
    eve_key, eve_basis_string = eve_interception(alice_key, alice_basis)

    # Bob generates his key after Eve's interception
    bob_key, bob_basis_string = generate_bob_key(eve_key, alice_basis)

    # Find the indices where Alice's, Eve's, and Bob's bases match
    correct_indices = find_matching_bases(alice_basis, eve_basis_string, bob_basis_string)

    # Adjust Alice's and Bob's keys to only use matching bases
    new_alice_key, new_bob_key = key_changer(correct_indices, alice_key, bob_key)

    # Calculate the percentage of correct bits
    per_correct = percentage_correct(correct_indices, len(alice_key))

    # Encrypt the full message with Alice's original key
    encrypted_message = xor_binaries(message_binary, alice_key)
    
    # Convert encrypted binary to hexadecimal for easier display
    encrypted_hex = binascii.hexlify(bytearray(int(encrypted_message[i:i + 8], 2) for i in range(0, len(encrypted_message), 8))).decode('utf-8')

    # Decrypt the message by XORing the encrypted message with the original key
    decrypted_message_binary = xor_binaries(encrypted_message, alice_key)
    decrypted_message = binary_to_utf8_string(decrypted_message_binary)

    # Calculate percentage of correct bits without Eve
    correct_indices_no_eve = find_matching_bases(alice_basis, alice_basis, bob_basis_string)
    percentage_correct_without_eve = percentage_correct_no_eve(alice_key, bob_key, correct_indices_no_eve)

    # Create a log entry
    log_data = f"""
============================
ITERATION: {timestamp}
============================

1. Input Message:
   - Message: {message}

2. Message in Binary:
   - Binary: {message_binary}

3. Alice's Data:
   - Alice's Key (Binary): {alice_key}
   - Alice's Basis String: {alice_basis}

4. Eve's Data:
   - Eve's Key (Binary): {eve_key}
   - Eve's Basis String: {eve_basis_string}

5. Bob's Data:
   - Bob's Key (Binary): {bob_key}
   - Bob's Basis String: {bob_basis_string}

6. Basis Matching:
   - Correct Bit Locations: {correct_indices}
   - New Alice Key (Binary): {new_alice_key}
   - New Bob Key (Binary): {new_bob_key}
   - Percentage Correct: {per_correct:.2f}%

7. Without Eve:
   - Percentage Correct Without Eve: {percentage_correct_without_eve:.2f}%

8. Encryption:
   - Encrypted Message (Hexadecimal): {encrypted_hex}

9. Decryption:
   - Decrypted Message: {decrypted_message}

--------------------------------------
"""

    # Log the results to the file
    log_results(log_data)

    # Print results to console (optional)
    logging.info("QKD protocol completed successfully.")
    print(log_data)

# Run the main function
if __name__ == "__main__":
    main()

