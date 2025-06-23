import os


def is_valid_dna(sequence):
    """Check if the sequence contains only valid DNA bases."""
    return all(base in "ACGT" for base in sequence.upper())

def count_bases(sequence):
    """Return a dictionary with counts of each base."""
    sequence = sequence.upper()
    return {
        "A": sequence.count("A"),
        "C": sequence.count("C"),
        "G": sequence.count("G"),
        "T": sequence.count("T")
    }

def gc_content(sequence):
    """Calculate GC content percentage of the DNA sequence."""
    sequence = sequence.upper()
    gc = sequence.count("G") + sequence.count("C")
    return (gc / len(sequence)) * 100 if sequence else 0

def parse_dna(file_path):
    """Parse DNA sequence from a file (FASTA or plain text)."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # Skip header lines starting with '>'
    sequence = ''.join(line.strip() for line in lines if not line.startswith('>'))
    return sequence

def print_welcome():
    print("Welcome to the DNA Parser!")
    print("You will be prompted to enter the path to a DNA file (FASTA or plain text).")
    print("Type 'exit' at any time to quit the program.")
    print("The program will validate the file and display sequence statistics.\n")

def main():
    print_welcome()
    while True:
        file_path = input("Enter the path to the DNA file (or type 'exit' to quit): ").strip()
        if file_path.lower() == 'exit':
            print("Exiting the DNA Parser. Goodbye!")
            return
        if not os.path.isfile(file_path):
            print(f"File '{file_path}' does not exist. Please try again.")
            continue

        try:
            sequence = parse_dna(file_path)
        except Exception as e:
            print(f"Error reading file: {e}. Please try again.")
            continue

        if not is_valid_dna(sequence):
            print("Invalid DNA sequence. Only A, C, G, and T are allowed. Please try again.")
            continue

        break  # Valid file and sequence found

    base_counts = count_bases(sequence)
    gc = gc_content(sequence)

    print(f"Length of sequence: {len(sequence)}")
    print(f"Base counts: {base_counts}")
    print(f"GC Content: {gc:.2f}%")

if __name__ == "__main__":
    main()
