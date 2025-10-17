# Simulación de Consenso con Agentes RESTful y Docker
Este proyecto simula un sistema distribuido donde múltiples agentes intentan alcanzar un consenso sobre un número aleatorio. La comunicación se gestiona a través de una API RESTful centralizada, y todo el entorno está orquestado con Docker Compose para garantizar la portabilidad y facilidad de ejecución.

## Arquitectura y Flujo de Comunicación
El sistema utiliza una arquitectura de **Coordinador Centralizado**, donde los componentes no se comunican directamente entre sí, sino a través de un servidor central que actúa como intermediario y única fuente de información.

La comunicación es **indirecta y asíncrona**. Los agentes y el observador son clientes desacoplados que interactúan con el estado compartido que mantiene el servidor.

El flujo de comunicación para alcanzar el consenso es el siguiente:

1.  **Primera Ronda**: Cada `Agente` genera un número aleatorio y lo publica en el endpoint `/nums` del servidor.
2.  **Estado de Espera**: Tras enviar su número, cada `Agente` entra en un bucle de espera, donde consulta periódicamente el endpoint `/status` para recibir instrucciones.
3.  **Verificación del Observador**: El `Observador` consulta el endpoint `/nums` para obtener los números de todos los agentes.Aplica la lógica de consenso para verificar si una mayoría (al menos dos agentes) ha elegido el mismo número.
4.  **Ciclo de Negociación**:
    * **Si NO hay consenso**: El `Observador` incrementa el número de ronda y publica un estado `{"status": "CONTINUE", "round": X}` en el endpoint `/status`.
    * **Si SÍ hay consenso**: El `Observador` publica un estado `{"status": "STOP"}` en el endpoint `/status`.
5.  **Reacción de los Agentes**:
    * Al detectar que el número de ronda en `/status` ha aumentado, los agentes saben que deben generar un nuevo número y volver al paso 2.
    * Al detectar el estado `STOP`, los agentes terminan su ejecución.
6.  **Finalización**: Una vez que el `Observador` publica la señal de `STOP`, también finaliza su propio proceso.

## Roles de los Componentes

El proyecto se divide en tres componentes lógicos principales, cada uno ejecutándose en su propio contenedor Docker.

### 1. `app.py` (El Servidor / Gestor de Estado)
Es el núcleo del sistema. Un servidor Flask que no contiene lógica de consenso, su única responsabilidad es gestionar el estado compartido de la simulación.
* **Endpoints**:
    * `GET /nums`: Devuelve la lista actual de números de todos los agentes.
    * `POST /nums`: Permite a un agente actualizar su número.
    * `GET /status`: Permite a los agentes consultar el estado actual de la simulación (`CONTINUE` o `STOP`) y la ronda actual.
    * `POST /status`: Endpoint exclusivo para que el observador actualice el estado de la simulación y dirija el flujo.

### 2. `agent.py` (El Agente de Trabajo)
Es un cliente simple y reactivo. Su comportamiento se define por un ciclo:
1.  Genera un número aleatorio y lo envía al servidor.
2.  Espera hasta que el `Observador` le indique (a través del estado en el servidor) que debe actuar de nuevo o detenerse.
3.  No tiene conocimiento de los otros agentes ni de la lógica de consenso.

### 3. `observer.py` (El Coordinador / Observador)
Es el "cerebro" de la simulación y el único componente que contiene la lógica para determinar si se ha alcanzado un consenso.
1.  Lee el estado de los agentes.
2.  Decide si el proceso debe continuar o detenerse.
3.  Comunica su decisión actualizando el estado en el servidor, dirigiendo así el comportamiento de los agentes.
4.  Registra el número de intentos necesarios para alcanzar el consenso.

## Cómo Ejecutar el Proyecto
Para ejecutar la simulación, solo se necesita tener instalados **Git** y **Docker**.

### Pasos
1.  **Clonar el repositorio:**
    git clone <URL_DEL_REPOSITORIO>

2.  **Levantar los contenedores y ejecutar la simulación:**
    docker-compose up --build

En la terminal se ven los logs de los agentes y del observador en tiempo real hasta que se alcanza un consenso y todos los contenedores se detienen automáticamente.