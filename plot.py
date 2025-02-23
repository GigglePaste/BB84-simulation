import matplotlib.pyplot as plt
import numpy as np
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_log_file(file_path: str) -> tuple[List[float], List[float], List[str]]:
    """Read data from the log file and extract relevant information.

    Args:
        file_path (str): The path to the log file.

    Returns:
        tuple: A tuple containing three lists - percentages with Eve, without Eve, and encrypted messages.
    """
    percentages_correct_with_eve = []
    percentages_correct_without_eve = []
    encrypted_messages = []

    try:
        with open(file_path, 'r') as log_file:
            for line in log_file:
                logging.debug(f"Reading line: {line.strip()}")  # Debug: log each line read
                if "Percentage Correct:" in line:  # Capture percentage correct with Eve
                    value = line.split(':')[-1].strip().replace('%', '')  # Remove '%' sign
                    percentages_correct_with_eve.append(float(value))  # Convert to float
                elif "Percentage Correct Without Eve" in line:
                    value = line.split(':')[-1].strip().replace('%', '')  # Remove '%' sign
                    percentages_correct_without_eve.append(float(value))  # Convert to float
                elif "Encrypted Message" in line:
                    value = line.split(':')[-1].strip()
                    encrypted_messages.append(value)
    except FileNotFoundError:
        logging.error(f"The log file at {file_path} was not found.")
        raise
    except Exception as e:
        logging.error(f"An error occurred while reading the log file: {e}")
        raise

    return (percentages_correct_with_eve, percentages_correct_without_eve, encrypted_messages)

def plot_data(percentages_correct_with_eve: List[float], percentages_correct_without_eve: List[float], encrypted_messages: List[str]) -> None:
    """Plot the data extracted from the log file.

    Args:
        percentages_correct_with_eve (List[float]): List of percentages with Eve.
        percentages_correct_without_eve (List[float]): List of percentages without Eve.
        encrypted_messages (List[str]): List of encrypted messages.
    """
    # Check if we have at least one list populated
    if len(percentages_correct_with_eve) == 0 and len(percentages_correct_without_eve) == 0:
        logging.warning("No data found for percentages.")
        return

    # Use the length of the longest populated list for x_values
    max_length = max(len(percentages_correct_with_eve), len(percentages_correct_without_eve))
    x_values = np.arange(1, max_length + 1)

    # Create a figure and axis for multiple plots
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Plot Percentage Correct with Eve
    axs[0].plot(x_values[:len(percentages_correct_with_eve)], percentages_correct_with_eve,
                marker='o', color='blue', label='Correct % with Eve')
    axs[0].set_title('Percentage Correct with Eve')
    axs[0].set_xlabel('Iteration')
    axs[0].set_ylabel('Percentage Correct (%)')
    axs[0].grid()
    axs[0].legend()

    # Plot Percentage Correct Without Eve
    axs[1].plot(x_values[:len(percentages_correct_without_eve)], percentages_correct_without_eve,
                marker='o', color='green', label='Correct % without Eve')
    axs[1].set_title('Percentage Correct without Eve')
    axs[1].set_xlabel('Iteration')
    axs[1].set_ylabel('Percentage Correct (%)')
    axs[1].grid()
    axs[1].legend()

    # Plot the length of encrypted messages
    encrypted_lengths = [len(msg) for msg in encrypted_messages]
    axs[2].bar(x_values[:len(encrypted_lengths)], encrypted_lengths,
               color='orange', label='Encrypted Message Lengths')
    axs[2].set_title('Lengths of Encrypted Messages')
    axs[2].set_xlabel('Iteration')
    axs[2].set_ylabel('Length of Encrypted Message (characters)')
    axs[2].grid()
    axs[2].legend()

    # Show plots
    plt.tight_layout()
    plt.show()

def main() -> None:
    """Main function to execute the log reading and plotting."""
    log_file_path = 'qkd_log.txt'
    percentages_correct_with_eve, percentages_correct_without_eve, encrypted_messages = read_log_file(log_file_path)
    
    logging.info(f"Data extracted: {len(percentages_correct_with_eve)} with Eve, {len(percentages_correct_without_eve)} without Eve, {len(encrypted_messages)} encrypted messages.")
    
    plot_data(percentages_correct_with_eve, percentages_correct_without_eve, encrypted_messages)

if __name__ == "__main__":
    main()

