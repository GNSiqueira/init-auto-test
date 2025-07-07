import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import sys

def get_folder_path():
    root = tk.Tk()
    root.withdraw() # Esconde a janela principal do Tkinter
    initial_path = str(Path.home() / "Downloads")
    folder_path = filedialog.askdirectory(initialdir=initial_path)
    print(folder_path) # Imprime o caminho selecionado para a saída padrão
    root.destroy() # Garante que a janela do Tkinter seja fechada

def get_file_path():
    root = tk.Tk()
    root.withdraw() # Esconde a janela principal do Tkinter
    initial_path = str(Path.home() / "Downloads")
    file_path = filedialog.askopenfilename(initialdir=initial_path)
    print(file_path) # Imprime o caminho selecionado para a saída padrão
    root.destroy() # Garante que a janela do Tkinter seja fechada

if __name__ == "__main__":
    # Verifica qual função deve ser chamada com base nos argumentos da linha de comando
    if len(sys.argv) > 1:
        if sys.argv[1] == "folder":
            get_folder_path()
        elif sys.argv[1] == "file":
            get_file_path()