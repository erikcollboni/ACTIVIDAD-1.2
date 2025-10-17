import requests
import time
from collections import Counter

SERVER_URL = "http://server:5000"
NUM_AGENTS = 3

def get_current_nums():
    try:
        response = requests.get(f"{SERVER_URL}/nums")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def check_consensus(nums_data):
    if not nums_data or len(nums_data) < NUM_AGENTS:
        return False
    numbers = [item["num"] for item in nums_data]
    # No considerar el consenso si algún agente no ha votado (valor 0)
    if 0 in numbers:
        return False
    counts = Counter(numbers)
    for num, count in counts.items():
        if count >= (NUM_AGENTS // 2) + 1:
            print(f"✅ ¡CONSENSO ALCANZADO! Número de mayoría: {num} (con {count} votos).")
            return True
    return False

def signal_agents(status, round_num=0):
    """Envía la nueva señal (estado y ronda) al servidor."""
    payload = {"status": status, "round": round_num}
    try:
        requests.post(f"{SERVER_URL}/status", json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Observador: Error al enviar señal: {e}") 

if __name__ == "__main__":
    print("Observador iniciado. Esperando a los agentes...")
    # time.sleep(5) # Dar tiempo a los agentes para que envíen su primer número
    
    current_round = 0
    
    while True:
        print(f"\n--- Observador: Verificando Ronda {current_round} ---")
        nums = get_current_nums()
        print(f"Números actuales de los agentes: {nums}")
        
        if check_consensus(nums):
            # Si hay consenso, enviar señal de parada y terminar
            signal_agents("STOP", current_round)
            print("Consenso encontrado. Terminando simulación.")
            break
        else:
            # Si no hay consenso, pasar a la siguiente ronda
            print("No se alcanzó el consenso. Iniciando siguiente ronda...")
            current_round += 1
            signal_agents("CONTINUE", current_round)

        time.sleep(1) # Esperar antes de la siguiente verificación
