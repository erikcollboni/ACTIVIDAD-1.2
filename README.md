# Herramientas y Tecnologías
La comunicación del sistema se centraliza a través de una API RESTful, implementada con las siguientes tecnologías:

* **Servidor API (Flask y Gunicorn)**: El servidor central está construido con **Flask**, un micro-framework de Python que facilita la creación de los endpoints (`/nums` y `/status`). Dentro del contenedor de Docker, la aplicación es gestionada por **Gunicorn**, un servidor WSGI (Web Server Gateway Interface) robusto y preparado para producción.

* **Clientes HTTP (Requests)**: Los componentes `agent.py` y `observer.py` actúan como clientes HTTP. Utilizan la librería **Requests** de Python para interactuar con la API, enviando peticiones `GET` para consultar el estado y `POST` para publicar sus números o actualizar el estado de la simulación.

* **Formato de Datos (JSON)**: Toda la información intercambiada entre los clientes y el servidor se serializa en formato **JSON** (JavaScript Object Notation), un estándar ligero y fácil de interpretar para la comunicación entre servicios web.

# Cómo Ejecutar el Proyecto
Para ejecutar la simulación, solo se necesita tener instalados **Git** y **Docker**.

## Pasos
1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/erikcollboni/ACTIVIDAD-1.2.git
    ```

2.  **Levantar los contenedores y ejecutar la simulación:**
    ```bash
    docker-compose up --build
    ```
En la terminal se ven los logs de los agentes y del observador en tiempo real hasta que se alcanza un consenso y todos los contenedores se detienen automáticamente.