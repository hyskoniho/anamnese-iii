from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from .actions import ActionKit

class HomeGUI(ActionKit):
    def __init__(self):
        super().__init__(self)
        
        self.allowed_file_extensions = ['.xlsx', '.xls', '.xlsb']
        self.selected_file_path = None

        self.Path = Path
        self.Tk = Tk
        self.Canvas = Canvas
        self.Entry = Entry
        self.Button = Button
        self.PhotoImage = PhotoImage

        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"C:\Users\Arklok\Documents\Projetos\FACULDADE\anamnese\repository\src\GUI\Home\assets\frame0")

        self.window = Tk()
        self.window.title("Clínica - Home")
        self.window.geometry("600x500")
        self.window.configure(bg="#FAFDFF")

        self.canvas = Canvas(
            self.window,
            bg="#FAFDFF",
            height=500,
            width=600,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.button_image_1 = PhotoImage(
            file=self.relative_to_assets("button_1.png"))
        
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.validate_file_path(self.entry_1.get()),
            relief="flat"
        )
        self.button_1.place(
            x=142.0,
            y=357.0,
            width=316.0,
            height=100.0
        )

        self.image_image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            276.0,
            244.0,
            image=self.image_image_1
        )

        self.entry_image_1 = PhotoImage(
            file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            276.0,
            244.0,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#9EAEB8",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=61.0,
            y=224.0,
            width=430.0,
            height=38.0
        )

        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.get_file_path(),
            relief="flat"
        )
        self.button_2.place(
            x=521.0,
            y=219.0,
            width=50.0,
            height=50.0
        )

        self.canvas.create_text(
            46.0,
            188.0,
            anchor="nw",
            text="Caminho do Arquivo",
            fill="#032157",
            font=("Inter", 16 * -1)
        )

        self.image_image_2 = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            145.0,
            71.0,
            image=self.image_image_2
        )
        self.window.resizable(False, False)

    def relative_to_assets(self, path: str):
        return self.ASSETS_PATH / self.Path(path)

    def run(self):
        self.window.mainloop()
    
    def stop(self):
        self.window.destroy()

# To use from another package:
# from src.GUI.Home.gui import HomeGUI
# gui = HomeGUI()
# gui.run()
