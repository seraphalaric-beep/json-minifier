import json
import tkinter as tk
from tkinter import filedialog, ttk
from typing import Optional


class JsonMinifierApp:
    """Simple Tkinter desktop app for minifying JSON text or files."""

    STATUS_COLORS = {
        "info": "#2d3748",
        "success": "#2f855a",
        "error": "#c53030",
    }

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("JSON Minifier")
        self.root.minsize(800, 640)
        self.root.geometry("900x680")
        self._build_ui()
        self._configure_shortcuts()
        self.show_status("Ready to minify.")

    def _build_ui(self) -> None:
        main_frame = ttk.Frame(self.root, padding=16)
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(
            main_frame,
            text="Paste JSON, click Minify, then copy or save the compact output.",
            font=("Segoe UI", 12, "bold"),
        )
        title_label.pack(anchor="w", pady=(0, 12))

        paned = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
        paned.pack(fill="both", expand=True)

        input_frame = ttk.Labelframe(paned, text="Input JSON", padding=8)
        output_frame = ttk.Labelframe(paned, text="Minified JSON", padding=8)
        paned.add(input_frame, weight=1)
        paned.add(output_frame, weight=1)

        self.input_text = tk.Text(
            input_frame,
            wrap="none",
            font=("Cascadia Code", 11),
            undo=True,
        )
        self.input_text.pack(side="left", fill="both", expand=True)

        input_scroll_y = ttk.Scrollbar(
            input_frame, orient="vertical", command=self.input_text.yview
        )
        input_scroll_y.pack(side="right", fill="y")
        input_scroll_x = ttk.Scrollbar(
            input_frame, orient="horizontal", command=self.input_text.xview
        )
        input_scroll_x.pack(side="bottom", fill="x")
        self.input_text.configure(
            yscrollcommand=input_scroll_y.set, xscrollcommand=input_scroll_x.set
        )

        self.output_text = tk.Text(
            output_frame,
            wrap="none",
            font=("Cascadia Code", 11),
            state="disabled",
        )
        self.output_text.pack(side="left", fill="both", expand=True)

        output_scroll_y = ttk.Scrollbar(
            output_frame, orient="vertical", command=self.output_text.yview
        )
        output_scroll_y.pack(side="right", fill="y")
        output_scroll_x = ttk.Scrollbar(
            output_frame, orient="horizontal", command=self.output_text.xview
        )
        output_scroll_x.pack(side="bottom", fill="x")
        self.output_text.configure(
            yscrollcommand=output_scroll_y.set, xscrollcommand=output_scroll_x.set
        )

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(12, 4))

        minify_button = ttk.Button(button_frame, text="Minify JSON", command=self.minify_json)
        minify_button.pack(side="left")

        copy_button = ttk.Button(button_frame, text="Copy Output", command=self.copy_output)
        copy_button.pack(side="left", padx=(8, 0))

        save_button = ttk.Button(button_frame, text="Save Output", command=self.save_output)
        save_button.pack(side="left", padx=(8, 0))

        open_button = ttk.Button(button_frame, text="Open File", command=self.load_file)
        open_button.pack(side="left", padx=(8, 0))

        self.status_label = ttk.Label(main_frame, text="", font=("Segoe UI", 10))
        self.status_label.pack(anchor="w", pady=(4, 0))

    def _configure_shortcuts(self) -> None:
        self.root.bind("<Control-m>", lambda _: self.minify_json())
        self.root.bind("<Control-M>", lambda _: self.minify_json())
        self.root.bind("<Control-c>", lambda _: self.copy_output())
        self.root.bind("<Control-C>", lambda _: self.copy_output())
        self.root.bind("<Control-s>", lambda _: self.save_output())
        self.root.bind("<Control-S>", lambda _: self.save_output())
        self.root.bind("<Control-o>", lambda _: self.load_file())
        self.root.bind("<Control-O>", lambda _: self.load_file())

    def show_status(self, message: str, kind: str = "info") -> None:
        """
        Update the status label with a message and style.

        Args:
            message: The text to display.
            kind: One of "info", "success", or "error".
        """
        color = self.STATUS_COLORS.get(kind, self.STATUS_COLORS["info"])
        self.status_label.configure(text=message, foreground=color)

    def clear_output(self) -> None:
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.configure(state="disabled")

    def minify_json(self) -> None:
        """Minify the JSON from the input box and show it in the output box."""
        raw_text = self.input_text.get("1.0", tk.END).strip()

        if not raw_text:
            self.clear_output()
            self.show_status("Please paste JSON to minify.")
            return

        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError as error:
            self.clear_output()
            self.show_status(f"Invalid JSON: {error}", kind="error")
            return

        minified = json.dumps(parsed, separators=(",", ":"), ensure_ascii=False)
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", minified)
        self.output_text.configure(state="disabled")
        self.show_status("JSON minified successfully.", kind="success")

    def copy_output(self) -> None:
        """Copy the minified JSON to the clipboard."""
        content = self.output_text.get("1.0", tk.END).strip()
        if not content:
            self.show_status("Nothing to copy yet.", kind="info")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.show_status("Minified JSON copied to clipboard.", kind="success")

    def save_output(self) -> None:
        """Save the minified JSON to a file."""
        content = self.output_text.get("1.0", tk.END).strip()
        if not content:
            self.show_status("Nothing to save yet.", kind="info")
            return

        path: Optional[str] = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Minified JSON",
        )
        if not path:
            self.show_status("Save canceled.", kind="info")
            return

        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
        self.show_status(f"Minified JSON saved to {path}.", kind="success")

    def load_file(self) -> None:
        """Load a JSON file into the input area."""
        path: Optional[str] = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Open JSON File",
        )
        if not path:
            self.show_status("File open canceled.", kind="info")
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
        except OSError as error:
            self.show_status(f"Unable to read file: {error}", kind="error")
            return

        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", content)
        self.show_status(f"Loaded file: {path}")


def main() -> None:
    root = tk.Tk()
    app = JsonMinifierApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
