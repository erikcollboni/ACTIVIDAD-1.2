import requests
import random
import time
import os

AGENT_ID = int(os.environ.get("AGENT_ID", 0))
SERVER_URL = "http://server:5000"

def update_my_num(new_num):
    payload = {"agent": AGENT_ID, "num": new_num}
    try:
        requests.post(f"{SERVER_URL}/nums", json=payload)
        # print(f"Agente {AGENT_ID} envió el número: {new_num}")
        return True
    except requests.exceptions.RequestException:
        print(f"Agente {AGENT_ID}: El servidor no responde.")
        return False

def get_current_status():
    """Consulta el estado actual de la simulación (ronda y estado)."""
    try:
        response = requests.get(f"{SERVER_URL}/status")
        return response.json()
    except requests.exceptions.RequestException:
        return None

if __name__ == "__main__":
    # random.seed(os.urandom(16))
    # print(f"Agente {AGENT_ID} iniciado.")
    current_round = -1

    while True:
        # 1. Generar y enviar un número
        num = random.randint(1, 10)
        if not update_my_num(num):
            # time.sleep(2) # Esperar si el servidor no está listo
            continue

        # 2. Esperar la señal del observador para la siguiente ronda
        # print(f"Agente {AGENT_ID} esperando la siguiente ronda...")
        while True:
            status = get_current_status()
            if not status:
                # time.sleep(1)
                continue

            # Si el servidor está en estado 'STOP', el agente termina.
            if status.get("status") == "STOP":
                # print(f"Agente {AGENT_ID} ha recibido la señal de parada. Terminando.")
                exit(0) # Termina el proceso del contenedor

            # Si el observador ha incrementado la ronda, es hora de generar un nuevo número.
            if status.get("round") > current_round:
                current_round = status.get("round")
                # print(f"Agente {AGENT_ID} iniciando ronda {current_round}.")
                break
            
            # time.sleep(1) # Esperar antes de volver a consultar
           