# dna_parser/main.py

import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from dna_parser.parser import is_valid_dna, count_bases, gc_content, parse_dna

def analyze_sequence(sequence, result_text, colors):
    if not is_valid_dna(sequence):
        messagebox.showerror("Error", "Invalid DNA sequence. Only A, C, G, and T are allowed.")
        return

    base_counts = count_bases(sequence)
    gc = gc_content(sequence)

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    result_text.tag_configure("header", font=("Segoe UI", 12, "bold"), foreground="#0078D7")
    result_text.insert(tk.END, "ANALYSIS RESULTS\n\n", "header")

    result_text.tag_configure("subheader", font=("Segoe UI", 10, "bold"))
    result_text.insert(tk.END, "Length of sequence: ", "subheader")
    result_text.insert(tk.END, f"{len(sequence)}\n\n")

    result_text.insert(tk.END, "Base counts:\n", "subheader")

    base_colors = {"A": "#FF5733", "C": "#33FF57", "G": "#3357FF", "T": "#F033FF"}
    for base, count in base_counts.items():
        result_text.tag_configure(f"base_{base}", foreground=base_colors[base], font=("Consolas", 10, "bold"))
        result_text.insert(tk.END, f"  {base}: ", "normal")
        result_text.insert(tk.END, f"{count}\n", f"base_{base}")

    result_text.insert(tk.END, "\nGC Content: ", "subheader")
    result_text.tag_configure("gc_value", foreground="#0078D7", font=("Consolas", 10, "bold"))
    result_text.insert(tk.END, f"{gc:.2f}%\n", "gc_value")

    result_text.config(state=tk.DISABLED)

def create_rounded_button(parent, text, command, colors, is_primary=False, width=20):
    height = 32
    button_width = width * 8

    button_colors = {
        "bg": colors.get("bg", "#1F1F1F"),
        "button_bg": colors.get("button_bg", "#2D2D2D"),
        "button_fg": colors.get("button_fg", "#FFFFFF"),
        "highlight": colors.get("highlight", "#3D3D3D")
    }

    frame = tk.Frame(parent, bg=button_colors["bg"])
    canvas = tk.Canvas(frame, height=height, width=button_width,
                      bg=button_colors["bg"], bd=0, highlightthickness=0)
    canvas.pack()

    if is_primary:
        btn_bg = "#0078D7"
        btn_fg = "#FFFFFF"
        hover_bg = "#106EBE"
    else:
        btn_bg = button_colors["button_bg"]
        btn_fg = button_colors["button_fg"]
        hover_bg = button_colors["highlight"]

    radius = 15
    def _create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)
    tk.Canvas.create_rounded_rect = _create_rounded_rect

    button_id = canvas.create_rounded_rect(
        0, 0, button_width, height, radius,
        fill=btn_bg, outline=btn_bg
    )
    text_id = canvas.create_text(
        button_width//2, height//2,
        text=text,
        fill=btn_fg,
        font=("Segoe UI", 10)
    )

    def on_enter(e):
        canvas.itemconfig(button_id, fill=hover_bg, outline=hover_bg)
    def on_leave(e):
        canvas.itemconfig(button_id, fill=btn_bg, outline=btn_bg)
    def on_click(e):
        command()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)
    canvas.tag_bind(text_id, "<Button-1>", on_click)
    canvas.rounded_rect_ids = [button_id, text_id]
    return frame

def apply_theme(root, is_dark_mode, frames, text_widgets, canvas_buttons):
    if is_dark_mode:
        colors = {
            "bg": "#1F1F1F",
            "fg": "#FFFFFF",
            "button_bg": "#2D2D2D",
            "button_fg": "#FFFFFF",
            "text_bg": "#2A2A2A",
            "text_fg": "#FFFFFF",
            "highlight": "#3D3D3D",
            "accent": "#0078D7",
            "border": "#3D3D3D"
        }
    else:
        colors = {
            "bg": "#F5F5F5",
            "fg": "#000000",
            "button_bg": "#E1E1E1",
            "button_fg": "#000000",
            "text_bg": "#FFFFFF",
            "text_fg": "#000000",
            "highlight": "#D1D1D1",
            "accent": "#0078D7",
            "border": "#D1D1D1"
        }
    root.config(bg=colors["bg"])
    for frame in frames:
        try:
            frame.config(bg=colors["bg"])
        except:
            pass
    for txt in text_widgets:
        try:
            txt.config(bg=colors["text_bg"], fg=colors["text_fg"])
        except:
            try:
                txt.config(bg=colors["bg"], fg=colors["fg"])
            except:
                pass
    for canvas_btn in canvas_buttons:
        try:
            canvas = canvas_btn.winfo_children()[0]
            canvas.config(bg=colors["bg"])
            if "primary" in str(canvas):
                btn_bg = "#0078D7"
                outline = "#0078D7"
            else:
                btn_bg = colors["button_bg"]
                outline = colors["button_bg"]
            for item_id in canvas.rounded_rect_ids:
                if "text" not in str(canvas.type(item_id)):
                    canvas.itemconfig(item_id, fill=btn_bg, outline=outline)
                else:
                    if "primary" in str(canvas):
                        canvas.itemconfig(item_id, fill="#FFFFFF")
                    else:
                        canvas.itemconfig(item_id, fill=colors["button_fg"])
        except:
            pass
    return colors

def main():
    root = tk.Tk()
    root.title("DNA Sequence Analyzer")
    root.geometry("800x700")
    root.minsize(700, 600)
    root.iconbitmap(default=None)

    is_dark_mode = True
    frames = []
    text_widgets = []
    canvas_buttons = []

    welcome_frame = tk.Frame(root, pady=25, padx=25)
    welcome_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
    frames.append(welcome_frame)

    title_frame = tk.Frame(welcome_frame)
    title_frame.pack(fill=tk.X)
    frames.append(title_frame)

    header_frame = tk.Frame(title_frame)
    header_frame.pack(anchor=tk.CENTER, expand=True)
    frames.append(header_frame)

    dna_label = tk.Label(
        header_frame,
        text="DNA",
        font=("Segoe UI", 32, "bold")
    )
    dna_label.pack(anchor=tk.CENTER)
    text_widgets.append(dna_label)

    welcome_label = tk.Label(
        header_frame,
        text="Sequence Analyzer",
        font=("Segoe UI Light", 24)
    )
    welcome_label.pack(anchor=tk.CENTER)
    text_widgets.append(welcome_label)

    desc_frame = tk.Frame(welcome_frame)
    desc_frame.pack(fill=tk.X, pady=(15, 0))
    frames.append(desc_frame)

    desc_label = tk.Label(
        desc_frame,
        text="Analyze DNA sequences with advanced visualization and statistics",
        font=("Segoe UI", 11)
    )
    desc_label.pack(anchor=tk.CENTER)
    text_widgets.append(desc_label)

    content_frame = tk.Frame(root, pady=15, padx=15)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
    frames.append(content_frame)

    content_border = tk.Frame(content_frame)
    content_border.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
    frames.append(content_border)

    content_inner = tk.Frame(content_border, padx=15, pady=15)
    content_inner.pack(fill=tk.BOTH, expand=True)
    frames.append(content_inner)

    viz_frame = tk.Frame(content_inner)
    viz_frame.pack(fill=tk.X, padx=10, pady=10)
    frames.append(viz_frame)

    viz_label = tk.Label(viz_frame, text="DNA VISUALIZATION", font=("Segoe UI", 9, "bold"))
    viz_label.pack(anchor=tk.W, padx=5)
    text_widgets.append(viz_label)

    dna_display = tk.Canvas(viz_frame, width=700, height=40)
    dna_display.pack(fill=tk.X, padx=5, pady=5)

    action_frame = tk.Frame(content_inner)
    action_frame.pack(fill=tk.X, padx=10, pady=(20, 10))
    frames.append(action_frame)

    action_label = tk.Label(action_frame, text="ACTIONS", font=("Segoe UI", 9, "bold"))
    action_label.pack(anchor=tk.W, padx=5)
    text_widgets.append(action_label)

    buttons_frame = tk.Frame(action_frame)
    buttons_frame.pack(fill=tk.X, padx=5, pady=10)
    frames.append(buttons_frame)

    results_frame = tk.Frame(content_inner)
    results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(15, 0))
    frames.append(results_frame)

    results_label = tk.Label(results_frame, text="RESULTS", font=("Segoe UI", 9, "bold"))
    results_label.pack(anchor=tk.W, padx=5)
    text_widgets.append(results_label)

    result_text = scrolledtext.ScrolledText(results_frame, height=15, font=("Consolas", 10), wrap=tk.WORD)
    result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
    result_text.config(state=tk.DISABLED)
    text_widgets.append(result_text)

    status_frame = tk.Frame(root, height=30)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    frames.append(status_frame)

    status_label = tk.Label(status_frame, text="Ready", anchor=tk.W, font=("Segoe UI", 9))
    status_label.pack(side=tk.LEFT, padx=10)
    text_widgets.append(status_label)

    def draw_dna(canvas, colors):
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width < 10:
            return
        canvas.config(bg=colors["text_bg"])
        base_colors = {
            "A": "#FF5733",
            "C": "#33FF57",
            "G": "#3357FF",
            "T": "#F033FF"
        }
        bases = ["A", "T", "G", "C", "A", "T", "G", "C", "A", "T", "G", "C", "A", "T", "G", "C"]
        spacing = width / (len(bases) + 1)
        canvas.create_line(
            10, height / 2, width - 10, height / 2,
            fill=colors["accent"], width=2, dash=(8, 4)
        )
        for i, base in enumerate(bases):
            x = (i + 1) * spacing
            color = base_colors[base]
            canvas.create_oval(
                x - 8, height / 2 - 8, x + 8, height / 2 + 8,
                fill=color, outline=colors["text_bg"]
            )
            canvas.create_text(
                x, height / 2,
                text=base,
                fill="#FFFFFF" if is_dark_mode else "#000000",
                font=("Consolas", 10, "bold")
            )
            if i % 2 == 0:
                canvas.create_line(
                    x, height / 2 - 8, x, height / 2 - 18,
                    fill=color, width=2
                )
                canvas.create_oval(
                    x - 4, height / 2 - 22, x + 4, height / 2 - 14,
                    fill=color, outline=colors["text_bg"]
                )
            else:
                canvas.create_line(
                    x, height / 2 + 8, x, height / 2 + 18,
                    fill=color, width=2
                )
                canvas.create_oval(
                    x - 4, height / 2 + 14, x + 4, height / 2 + 22,
                    fill=color, outline=colors["text_bg"]
                )

    def open_text_input():
        status_label.config(text="Entering DNA sequence...")
        input_window = tk.Toplevel(root)
        input_window.title("Enter DNA Sequence")
        input_window.geometry("500x400")
        input_window.transient(root)
        input_window.grab_set()
        input_frame = tk.Frame(input_window, padx=20, pady=20)
        input_frame.pack(fill=tk.BOTH, expand=True)
        header_label = tk.Label(
            input_frame,
            text="Enter DNA Sequence",
            font=("Segoe UI", 14, "bold")
        )
        header_label.pack(anchor=tk.CENTER, pady=(0, 10))
        instruction = tk.Label(
            input_frame,
            text="Enter a sequence containing only A, C, G, and T bases:",
            font=("Segoe UI", 10)
        )
        instruction.pack(pady=(10, 5), anchor=tk.W)
        text_input = scrolledtext.ScrolledText(
            input_frame,
            height=12,
            font=("Consolas", 11),
            wrap=tk.WORD
        )
        text_input.pack(fill=tk.BOTH, expand=True, pady=10)
        input_window.config(bg=colors["bg"])
        input_frame.config(bg=colors["bg"])
        header_label.config(bg=colors["bg"], fg=colors["fg"])
        instruction.config(bg=colors["bg"], fg=colors["fg"])
        text_input.config(bg=colors["text_bg"], fg=colors["text_fg"])
        buttons_bar = tk.Frame(input_frame, bg=colors["bg"])
        buttons_bar.pack(fill=tk.X, pady=(15, 0))
        def submit_sequence():
            sequence = text_input.get(1.0, tk.END).strip()
            if sequence:
                analyze_sequence(sequence, result_text, colors)
                status_label.config(text=f"Analyzed sequence of length {len(sequence)}")
                input_window.destroy()
        cancel_btn_frame = create_rounded_button(
            buttons_bar, "Cancel", input_window.destroy, colors, width=10
        )
        cancel_btn_frame.pack(side=tk.RIGHT, padx=5)
        submit_btn_frame = create_rounded_button(
            buttons_bar, "Analyze", submit_sequence, colors, is_primary=True, width=10
        )
        submit_btn_frame.pack(side=tk.RIGHT, padx=5)
        text_input.focus_set()

    def browse_file():
        status_label.config(text="Browsing for DNA files...")
        file_path = filedialog.askopenfilename(
            title="Select DNA File",
            filetypes=[("Text files", "*.txt"), ("FASTA files", "*.fasta"), ("All files", "*.*")]
        )
        if file_path:
            try:
                sequence = parse_dna(file_path)
                analyze_sequence(sequence, result_text, colors)
                filename = os.path.basename(file_path)
                status_label.config(text=f"Analyzed file: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {e}")
                status_label.config(text="Error reading file")

    def toggle_theme():
        nonlocal is_dark_mode, colors
        is_dark_mode = not is_dark_mode
        colors = apply_theme(root, is_dark_mode, frames, text_widgets, canvas_buttons)
        draw_dna(dna_display, colors)
        status_label.config(text=f"Switched to {'Dark' if is_dark_mode else 'Light'} mode")

    text_btn = create_rounded_button(
        buttons_frame, "Enter DNA Sequence", open_text_input,
        {"bg": "#FFFFFF"}, is_primary=True
    )
    text_btn.pack(side=tk.LEFT, padx=5, pady=5)
    canvas_buttons.append(text_btn)

    browse_btn = create_rounded_button(
        buttons_frame, "Browse for DNA File", browse_file,
        {"bg": "#FFFFFF"}, is_primary=False
    )
    browse_btn.pack(side=tk.LEFT, padx=5, pady=5)
    canvas_buttons.append(browse_btn)

    controls_frame = tk.Frame(status_frame)
    controls_frame.pack(side=tk.RIGHT, padx=10)
    frames.append(controls_frame)

    theme_btn = create_rounded_button(
        controls_frame,
        "Light Mode",
        toggle_theme,
        {"bg": "#FFFFFF"},
        is_primary=False,
        width=10
    )
    theme_btn.pack(side=tk.RIGHT, padx=5)
    canvas_buttons.append(theme_btn)

    exit_btn = create_rounded_button(
        controls_frame,
        "Exit",
        root.destroy,
        {"bg": "#FFFFFF"},
        is_primary=False,
        width=8
    )
    exit_btn.pack(side=tk.RIGHT, padx=5)
    canvas_buttons.append(exit_btn)

    colors = apply_theme(root, is_dark_mode, frames, text_widgets, canvas_buttons)

    def on_resize(event):
        if event.widget == root:
            root.after(100, lambda: draw_dna(dna_display, colors))
    root.bind("<Configure>", on_resize)

    result_text.config(state=tk.NORMAL)
    result_text.tag_configure("welcome_title", font=("Segoe UI", 14, "bold"), foreground="#0078D7", justify="center")
    result_text.tag_configure("welcome_text", font=("Segoe UI", 11), justify="center")
    result_text.insert(tk.END, "\n\n\n", "welcome_text")
    result_text.insert(tk.END, "Welcome to DNA Sequence Analyzer\n\n", "welcome_title")
    result_text.insert(tk.END, "This tool helps you analyze DNA sequences.\n", "welcome_text")
    result_text.insert(tk.END, "Enter a sequence manually or load from a file to begin.\n\n", "welcome_text")
    result_text.insert(tk.END, "You'll get information about:\n", "welcome_text")
    result_text.insert(tk.END, "• Sequence length\n", "welcome_text")
    result_text.insert(tk.END, "• Base counts (A, C, G, T)\n", "welcome_text")
    result_text.insert(tk.END, "• GC content percentage\n", "welcome_text")
    result_text.config(state=tk.DISABLED)

    root.update()
    draw_dna(dna_display, colors)
    root.mainloop()

if __name__ == "__main__":
    main()