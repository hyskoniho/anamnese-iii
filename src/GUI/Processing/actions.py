from tkinter import messagebox

class ActionKit:
    def __init__(self, gui, transformer):
        self.gui = gui
        self.transformer = transformer

    def open_settings(self):
        """Open the settings dialog."""
        self.gui.open_settings()

    def open_about(self):
        """Open the about dialog."""
        self.gui.open_about()

    def open_help(self):
        """Open the help dialog."""
        self.gui.open_help()

    def exit_application(self):
        """Exit the application."""
        self.gui.exit_application()