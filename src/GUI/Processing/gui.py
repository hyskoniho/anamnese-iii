from .actions import ActionKit

class ProcessingGUI(ActionKit):
    def __init__(self, transformer, step: str = "Processamento"):
        assert step in ["Pacientes", "Anamneses", "Retornos"], "Invalid step provided. Must be one of: 'Pacientes', 'Anamneses', 'Retornos'."
        self.step = step
        
        super().__init__(self, transformer=transformer)
        
        from pathlib import Path
        from tkinter import Tk, Canvas, Entry, Button, PhotoImage
        from tkinter import ttk

        self.Path = Path
        self.Tk = Tk
        self.Canvas = Canvas
        self.Entry = Entry
        self.Button = Button
        self.PhotoImage = PhotoImage
        self.ttk = ttk

        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"C:\Users\Arklok\Documents\Projetos\FACULDADE\anamnese\repository\src\GUI\Processing\assets\frame0")

        self.window = Tk()
        self.window.geometry("960x540")
        self.window.configure(bg="#FAFDFF")

        self.canvas = Canvas(
            self.window,
            bg="#FAFDFF",
            height=540,
            width=960,
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
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_1.place(
            x=713.0,
            y=477.0,
            width=100.0,
            height=41.88607406616211
        )

        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(
            x=835.5,
            y=477.0,
            width=100.0,
            height=41.772151947021484
        )

        self.button_image_3 = PhotoImage(
            file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.button_3.place(
            x=458.0,
            y=320.0,
            width=42.5,
            height=42.5
        )

        self.button_image_4 = PhotoImage(
            file=self.relative_to_assets("button_4.png"))
        self.button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        self.button_4.place(
            x=458.5,
            y=177.5,
            width=42.5,
            height=42.5
        )

        self.image_image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            723.0,
            254.5,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            723.0,
            270.0,
            image=self.image_image_2
        )

        img2_width = self.image_image_2.width()
        img2_height = self.image_image_2.height()
        img2_x = 723.0 - img2_width // 2
        img2_y = 270.0 - img2_height // 2

        self.image_image_3 = PhotoImage(
            file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(
            236.0,
            254.5,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=self.relative_to_assets("image_4.png"))
        self.image_4 = self.canvas.create_image(
            236.0,
            270.0,
            image=self.image_image_4
        )

        img4_width = self.image_image_4.width()
        img4_height = self.image_image_4.height()
        img4_x = 236.0 - img4_width // 2
        img4_y = 270.0 - img4_height // 2

        # --- DataFrame display over image_2 (n_dataframe) ---
        self.df_frame_n = self.ttk.Frame(self.window)
        self.df_frame_n.place(x=img2_x, y=img2_y, width=img2_width, height=img2_height)
        self.df_tree_n = self.ttk.Treeview(self.df_frame_n, show='headings')
        df_n = self.transformer.n_dataframe
        self.df_tree_n["columns"] = list(df_n.columns)
        for col in df_n.columns:
            self.df_tree_n.heading(col, text=col)
            self.df_tree_n.column(col, width=100, anchor='center')
        for _, row in df_n.iterrows():
            self.df_tree_n.insert("", "end", values=list(row))
        vsb_n = self.ttk.Scrollbar(self.df_frame_n, orient="vertical", command=self.df_tree_n.yview)
        hsb_n = self.ttk.Scrollbar(self.df_frame_n, orient="horizontal", command=self.df_tree_n.xview)
        self.df_tree_n.configure(yscrollcommand=vsb_n.set, xscrollcommand=hsb_n.set)
        vsb_n.pack(side='right', fill='y')
        hsb_n.pack(side='bottom', fill='x')
        self.df_tree_n.pack(side='left', fill='both', expand=True)

        # --- DataFrame display over image_4 (i_dataframe) ---
        self.df_frame_i = self.ttk.Frame(self.window)
        self.df_frame_i.place(x=img4_x, y=img4_y, width=img4_width, height=img4_height)
        self.df_tree_i = self.ttk.Treeview(self.df_frame_i, show='headings')
        df_i = self.transformer.i_dataframe
        self.df_tree_i["columns"] = list(df_i.columns)
        for col in df_i.columns:
            self.df_tree_i.heading(col, text=col)
            self.df_tree_i.column(col, width=100, anchor='center')
        for _, row in df_i.iterrows():
            self.df_tree_i.insert("", "end", values=list(row))
        vsb_i = self.ttk.Scrollbar(self.df_frame_i, orient="vertical", command=self.df_tree_i.yview)
        hsb_i = self.ttk.Scrollbar(self.df_frame_i, orient="horizontal", command=self.df_tree_i.xview)
        self.df_tree_i.configure(yscrollcommand=vsb_i.set, xscrollcommand=hsb_i.set)
        vsb_i.pack(side='right', fill='y')
        hsb_i.pack(side='bottom', fill='x')
        self.df_tree_i.pack(side='left', fill='both', expand=True)

        self.canvas.create_text(
            23.0,
            27.5,
            anchor="nw",
            text=f"[{step}]",
            fill="#032157",
            font=("Inter", 20 * -1)
        )

        self.canvas.create_text(
            23.0,
            491.0,
            anchor="nw",
            text="Ao clicar em processar, você concorda em inserir os dados da tabela à esquerda no banco de dados",
            fill="#032157",
            font=("Inter", 12 * -1)
        )

        self.canvas.create_text(
            23.0,
            504.0,
            anchor="nw",
            text="de produção do sistema do ambulatório. ",
            fill="#032157",
            font=("Inter", 12 * -1)
        )
        self.window.resizable(False, False)

    def relative_to_assets(self, path: str):
        return self.ASSETS_PATH / self.Path(path)

    def run(self):
        self.window.mainloop()

# To use from another package:
# from src.GUI.Processing.gui import ProcessingGUI
# gui = ProcessingGUI()
# gui.run()
