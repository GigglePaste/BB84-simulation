import subprocess
import random
import logging
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SENTENCE_FILE = 'sentences.txt'
QKD_SCRIPT = 'qkd.py'
BATCH_SIZE = 10  # Number of sentences to process in each run
TOTAL_RUNS = 100  # Total number of runs

def read_sentences(file_path: str) -> List[str]:
    """Read sentences from a file and return them as a list."""
    try:
        with open(file_path, 'r') as file:
            sentences = [line.strip() for line in file.readlines() if line.strip()]
        logging.info(f"Read {len(sentences)} sentences from {file_path}.")
        return sentences
    except FileNotFoundError:
        logging.error(f"The file {file_path} was not found.")
        raise

def run_qkd_process(sentences: List[str]) -> None:
    """Run the QKD process with a list of sentences."""
    input_data = "\n".join(sentences)
    try:
        process = subprocess.Popen(
            ['python', QKD_SCRIPT],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input=input_data.encode())
        
        if process.returncode != 0:
            logging.error(f"Error running QKD process: {stderr.decode().strip()}")
        else:
            logging.info(f"QKD process completed successfully for {len(sentences)} sentences.")
    except Exception as e:
        logging.error(f"An exception occurred while running the QKD process: {e}")

def main() -> None:
    """Main function to execute the QKD process."""
    sentences = read_sentences(SENTENCE_FILE)
    total_runs = 0

    while total_runs < TOTAL_RUNS:
        batch_sentences = random.sample(sentences, min(BATCH_SIZE, len(sentences)))
        run_qkd_process(batch_sentences)
        total_runs += BATCH_SIZE

if __name__ == "__main__":
    main()

