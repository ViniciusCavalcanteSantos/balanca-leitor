import serial
import threading
import time
import re
import json, os
import argparse
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

peso_atual = None
lock = threading.Lock()

# Configurações da porta serial
PORTA_SERIAL = 'COM6'
BAUDRATE = 9600
TIMEOUT = 1


CONFIG_FILE = "config.json"

parser = argparse.ArgumentParser()
parser.add_argument("--settings", action="store_true", help="Abrir tela de configurações")
args = parser.parse_args()
mostrar_tela_manual = args.settings

def carregar_config():
    if not os.path.isfile(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def salvar_config(porta, baud):
    cfg = {"PORTA_SERIAL": porta, "BAUDRATE": baud}
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)

def desbloquear_balança(porta):
    try:
        ser = serial.Serial(porta, 1200, timeout=1)
        ser.close()
    except Exception as e:
        print(f"Aviso ao desbloquear balança: {e}")
    time.sleep(1)

def extrair_peso(linha):
    match = re.search(r'([\d.,]+)', linha)
    if match:
        valor = match.group(1).replace(',', '.')
        try:
            return float(valor)
        except ValueError:
            return None
    return None

def ler_balança():
    global peso_atual
    try:
        desbloquear_balança(PORTA_SERIAL)
        ser = serial.Serial(PORTA_SERIAL, BAUDRATE, timeout=TIMEOUT)
        print(f"[INFO] Conectado na balança ({PORTA_SERIAL})")
        
        while True:
            try:
                ser.write(b'\r\n')
                time.sleep(0.3)
                linha = ser.readline().decode('utf-8', errors='ignore').strip()
                peso_float = extrair_peso(linha)

                if linha and peso_float:
                    with lock:
                        peso_atual = peso_float
                        print(f"[PESO] {peso_atual}")
                time.sleep(1)  # espera entre as leituras
            except Exception as e:
                with lock:
                    peso_atual = None
                print(f"[Erro leitura] {e}")
                time.sleep(2)
    except serial.SerialException as e:
        with lock:
            peso_atual = None
        print(f"[Erro serial] {e}")

@app.route('/peso')
def get_peso():
    with lock:
        if peso_atual is None:
            return jsonify({"peso": None, "mensagem": "Sem peso disponível"})
        return jsonify({"peso": peso_atual})

if __name__ == "__main__":
    cfg = carregar_config()
    if cfg is None or mostrar_tela_manual:     # ver passo 2 para a flag
        from settings_gui import abrir_tela_config
        porta, baud = abrir_tela_config()
        if porta is None:
            exit(0)  # usuário fechou sem salvar
        salvar_config(porta, baud)
        cfg = {"PORTA_SERIAL": porta, "BAUDRATE": baud}

    PORTA_SERIAL = cfg["PORTA_SERIAL"]
    BAUDRATE     = cfg["BAUDRATE"]

    thread_leitura = threading.Thread(target=ler_balança, daemon=True)
    thread_leitura.start()
    
    app.run(host='0.0.0.0', port=5000)
