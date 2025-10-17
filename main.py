import requests
import random
import time
from collections import Counter
import threading

# URL del servidor Flask que expone los endpoints GET/POST /nums
SERVER_URL = "http://server:5000/nums"
NUM_AGENTS = 3

# Un objeto 'Event' para comunicar entre hilos.
# El hilo principal lo usará para indicar a los agentes que deben detenerse.
consensus_reached_event = threading.Event()

def getCurrentNums():
    """Obtiene los números actuales de todos los agentes desde el servidor."""
    try:
        response = requests.get(SERVER_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener números: {e}")
        return None

def updateAgentNum(agent_id, new_num):
    """Actualiza el número de un agente en el servidor."""
    payload = {"agent": agent_id, "num": new_num}
    try:
        response = requests.post(SERVER_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar agente {agent_id}: {e}")

def checkConsensus(nums_data):
    """Verifica si se ha alcanzado un consenso por mayoría."""
    numbers = [item["num"] for item in nums_data]
    counts = Counter(numbers)
    majority_threshold = (NUM_AGENTS // 2) + 1
    
    for num, count in counts.items():
        if count >= majority_threshold:
            print(f"✅ ¡CONSENSO ALCANZADO! Número de mayoría: {num} (con {count} votos).")
            return True
            
    return False

def agentTask(agent_id):
    """
    Esta es la función que ejecutará cada hilo de agente.
    El agente se ejecuta en un bucle, generando números hasta que el evento de consenso se active.
    """
    print(f"Agente {agent_id} iniciado.")
    while not consensus_reached_event.is_set():
        # Generar un número aleatorio
        new_num = random.randint(1, 10)
        
        # Comunicar el nuevo número al servidor
        updateAgentNum(agent_id, new_num)
        
        # Simular un tiempo de trabajo o espera variable para cada agente
        time.sleep(random.uniform(0.5, 2.0))
        
    print(f"Agente {agent_id} detenido.")

def simularConsenso():
    """
    Orquesta la simulación: inicia los hilos de los agentes y luego
    actúa como un observador que verifica periódicamente si se ha alcanzado un consenso.
    """
    threads = []
    check_count = 0

    print("--- Iniciando Simulación de Consenso con Hilos ---")

    # 1. Crear e iniciar un hilo para cada agente
    for agent_id in range(NUM_AGENTS):
        thread = threading.Thread(target=agentTask, args=(agent_id,))
        threads.append(thread)
        thread.start()

    # 2. El hilo principal ahora comprueba el consenso periódicamente
    while not consensus_reached_event.is_set():
        check_count += 1
        print(f"\n--- Verificación de Consenso #{check_count} ---")
        
        current_nums = getCurrentNums()
        
        if current_nums:
            print(f"Números actuales: {current_nums}")
            
            # Si se encuentra consenso, se activa el evento para detener los hilos
            if checkConsensus(current_nums):
                consensus_reached_event.set()
            else:
                print("No se alcanzó el consenso. El observador volverá a comprobar en breve...")
        
        if check_count > 100: # Límite de seguridad
            print("Límite de verificaciones excedido. Forzando terminación.")
            consensus_reached_event.set()
            break
            
        # El observador espera antes de volver a comprobar
        time.sleep(1)

    # 3. Esperar a que todos los hilos de los agentes terminen su ejecución
    print("\nSeñal de consenso enviada. Esperando a que los hilos de los agentes finalicen...")
    for thread in threads:
        thread.join()

    print(f"\nProceso finalizado. Número total de verificaciones: {check_count}.")


if __name__ == "__main__":
    # Asegúrate de que el servidor (app.py) se esté ejecutando antes de correr este script
    simularConsenso()