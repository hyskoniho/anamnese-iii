from tkinter import filedialog, messagebox
import os

class ActionKit:
    def __init__(self, gui):
        self.gui = gui

    def get_file_path(self) -> None:
        """Open a file dialog to select a file and return its path."""
        self.selected_file_path = filedialog.askopenfilename()
        self.entry_1.insert(0, self.selected_file_path)
        
    def validate_file_path(self, file_path: str) -> None:
        """Validate the selected file path."""
        if file_path and any([file_path.endswith(term) for term in self.allowed_file_extensions]) and os.path.isfile(file_path):
            if not self.selected_file_path:
                self.selected_file_path = file_path

            self.stop()
        else:
            messagebox.showerror(
                title="Arquivo Inválido",
                message="Por favor, selecione um arquivo válido Excel."
            )
            self.entry_1.delete(0, 'end')
    