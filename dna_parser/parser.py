# dna_parser/parser.py

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
    sequence = ''.join(line.strip() for line in lines if not line.startswith('>'))
    return sequence