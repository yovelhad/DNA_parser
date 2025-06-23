import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


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


def analyze_sequence(sequence, result_text):
    """Analyze DNA sequence and display results"""
    if not is_valid_dna(sequence):
        messagebox.showerror("Error", "Invalid DNA sequence. Only A, C, G, and T are allowed.")
        return

    base_counts = count_bases(sequence)
    gc = gc_content(sequence)

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Length of sequence: {len(sequence)}\n")
    result_text.insert(tk.END, f"Base counts: {base_counts}\n")
    result_text.insert(tk.END, f"GC Content: {gc:.2f}%\n")


def main():
    # Create the main window
    root = tk.Tk()
    root.title("DNA Parser")
    root.geometry("600x500")

    # Welcome message
    welcome_frame = tk.Frame(root, pady=20)
    welcome_frame.pack(fill=tk.X)

    welcome_label = tk.Label(welcome_frame,
                             text="Welcome to the DNA Parser!\n"
                                  "Choose one of the options below to analyze a DNA sequence.\n",
                             font=("Arial", 12))
    welcome_label.pack()

    # Options frame
    options_frame = tk.Frame(root, pady=10)
    options_frame.pack(fill=tk.X)

    # Results area
    result_frame = tk.Frame(root, pady=10)
    result_frame.pack(fill=tk.BOTH, expand=True)

    result_text = scrolledtext.ScrolledText(result_frame, height=15)
    result_text.pack(fill=tk.BOTH, expand=True, padx=20)

    # Text input for manual DNA entry
    def open_text_input():
        input_window = tk.Toplevel(root)
        input_window.title("Enter DNA Sequence")
        input_window.geometry("500x300")

        tk.Label(input_window, text="Enter DNA sequence (only A, C, G, T):").pack(pady=10)

        text_input = scrolledtext.ScrolledText(input_window, height=10)
        text_input.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        def submit_sequence():
            sequence = text_input.get(1.0, tk.END).strip()
            if sequence:
                analyze_sequence(sequence, result_text)
                input_window.destroy()

        submit_btn = tk.Button(input_window, text="Analyze", command=submit_sequence)
        submit_btn.pack(pady=10)

    # Browse file function
    def browse_file():
        file_path = filedialog.askopenfilename(
            title="Select DNA File",
            filetypes=[("Text files", "*.txt"), ("FASTA files", "*.fasta"), ("All files", "*.*")]
        )

        if file_path:
            try:
                sequence = parse_dna(file_path)
                analyze_sequence(sequence, result_text)
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {e}")

    # Option buttons
    btn_exit = tk.Button(options_frame, text="1: Exit", command=root.destroy, width=20)
    btn_exit.pack(pady=5)

    btn_text = tk.Button(options_frame, text="2: Enter DNA sequence", command=open_text_input, width=20)
    btn_text.pack(pady=5)

    btn_browse = tk.Button(options_frame, text="3: Browse for DNA file", command=browse_file, width=20)
    btn_browse.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()