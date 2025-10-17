# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Estado inicial de los números de los agentes
nums = [
    {"agent": 0, "num": 0},
    {"agent": 1, "num": 0},
    {"agent": 2, "num": 0}
]

# NUEVO: Estado del "juego" o simulación
# - status: 'CONTINUE' o 'STOP'
# - round: El número de ronda actual. Los agentes lo usan para saber si deben generar un nuevo número.
game_state = {"status": "CONTINUE", "round": 0}

@app.get("/nums")
def get_nums():
    return jsonify(nums)

@app.post("/nums")
def add_num():
    if request.is_json:
        new_num_data = request.get_json()
        agent_id = new_num_data["agent"]
        if 0 <= agent_id < len(nums):
            nums[agent_id]['num'] = new_num_data['num']
            return new_num_data, 201
    return {"error": "Request must be JSON and have a valid agent ID"}, 415

# --- NUEVOS ENDPOINTS PARA CONTROLAR EL FLUJO ---

@app.get("/status")
def get_status():
    """Endpoint para que los agentes consulten el estado actual de la simulación."""
    return jsonify(game_state)

@app.post("/status")
def update_status():
    """Endpoint para que el observador cambie el estado de la simulación."""
    if request.is_json:
        new_state = request.get_json()
        if "status" in new_state:
            game_state["status"] = new_state["status"]
        if "round" in new_state:
            game_state["round"] = new_state["round"]
        print(f"Nuevo estado recibido: {game_state}")
        return jsonify(game_state), 200
    return {"error": "Request must be JSON"}, 415