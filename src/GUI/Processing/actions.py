from tkinter import messagebox

class ActionKit:
    def __init__(self, gui, transformer):
        self.gui = gui
        self.transformer = transformer

    def swipe_right(self, i: int) -> None:
        if i is not None and i >= 0:
            self.transformer.add_n_row(i, self.transformer.i_dataframe)
            self.transformer.remove_i_row(i)
            self.update_tables()
            self.window.update_idletasks()
    
    def swipe_left(self, i: int) -> None:
        if i is not None and i >= 0:
            self.transformer.add_i_row(i, self.transformer.n_dataframe)
            self.transformer.remove_n_row(i)
            self.update_tables()
            self.window.update_idletasks()

    def update_tables(self):
        for item in self.gui.df_tree_n.get_children():
            self.gui.df_tree_n.delete(item)
        for idx, row in self.transformer.n_dataframe.iterrows():
            self.gui.df_tree_n.insert("", "end", iid=str(idx), values=list(row))
        
        for item in self.gui.df_tree_i.get_children():
            self.gui.df_tree_i.delete(item)
        for idx, row in self.transformer.i_dataframe.iterrows():
            self.gui.df_tree_i.insert("", "end", iid=str(idx), values=list(row))
        
        self.gui.n_selected_row_index = None
        self.gui.i_selected_row_index = None
        
    def interrupt(self) -> None:
        exit(1)
    
    def finish(self) -> None:
        self.gui.window.destroy()
        