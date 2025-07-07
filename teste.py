import tkinter as tk
from tkinter import filedialog
from pathlib import Path

class PastaUtils:
    @staticmethod
    def getPathFolder():
        root = tk.Tk()
        root.withdraw()
        initial_path = str(Path.home() / "Downloads")
        print("Pasta inicial:", initial_path)
        return filedialog.askdirectory(initialdir=initial_path)

# Exemplo de uso:
pasta = PastaUtils.getPathFolder()
print("Pasta selecionada:", pasta)
