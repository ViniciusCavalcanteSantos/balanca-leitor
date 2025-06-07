import tkinter as tk
from tkinter import messagebox
import serial

def testar_conexao(porta, baud):
    try:
        ser = serial.Serial(porta, int(baud), timeout=1)
        ser.close()
        return True, f"Conectado em {porta} @ {baud}bps"
    except Exception as e:
        return False, str(e)

def abrir_tela_config():
    import os, json
    config = {"PORTA_SERIAL": "COM6", "BAUDRATE": "9600"}
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            try:
                config.update(json.load(f))
            except:
                pass

    sel = {"porta": None, "baud": None}

    def on_testar():
        ok, msg = testar_conexao(entry_porta.get(), entry_baud.get())
        messagebox.showinfo("Teste de Conexão", msg if ok else f"Erro: {msg}")

    def on_salvar():
        sel["porta"] = entry_porta.get().strip()
        sel["baud"]  = entry_baud.get().strip()
        root.destroy()

    def on_fechar():
        root.destroy()

    # Título
    root = tk.Tk()
    root.title("Configurar Balança")

    # Input Serial
    tk.Label(root, text="Porta Serial:").grid(row=0, column=0, padx=5, pady=5)
    entry_porta = tk.Entry(root)
    entry_porta.insert(0, config["PORTA_SERIAL"])
    entry_porta.grid(row=0, column=1, padx=5, pady=5)
    
     # Input Baudrate
    tk.Label(root, text="Baudrate:").grid(row=1, column=0, padx=5, pady=5)
    entry_baud = tk.Entry(root)
    entry_baud.insert(0, str(config["BAUDRATE"]))
    entry_baud.grid(row=1, column=1, padx=5, pady=5)

    # Botões
    btn_frame = tk.Frame(root)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
    tk.Button(btn_frame, text="Testar Conexão", command=on_testar).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Salvar",          command=on_salvar).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Fechar",          command=on_fechar).pack(side="left", padx=5)

    # Centralizar janela
    root.update_idletasks()
    w = root.winfo_width(); h = root.winfo_height()
    ws = root.winfo_screenwidth(); hs = root.winfo_screenheight()
    x = (ws//2) - (w//2); y = (hs//2) - (h//2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.mainloop()
    return sel["porta"], sel["baud"]
