# 🧠 Agentic Pay Demo

Este proyecto es un **demo de agente AI** que entiende lenguaje natural y ejecuta operaciones contra un **API de pagos simulado**.

## 🚀 Qué incluye

- **Mock Bank API**: FastAPI con endpoints de saldo, pagos (con idempotencia) y transacciones.
- **Agente (`agent.py`)**: Toma instrucciones en texto, las convierte en JSON y llama al API.
- **LLM local con Ollama**: Procesa el lenguaje natural sin depender de servicios externos.
- **Documentación extra** en `docs/` y ejemplos en `examples/`.

## 🛠️ Requisitos

- Python 3.10+
- [Ollama](https://ollama.ai) instalado y corriendo (`ollama serve`)
- FastAPI + Uvicorn (`pip install fastapi uvicorn requests`)

## ▶️ Cómo correr el demo

```bash
# 1. Clona el repositorio
git clone https://github.com/gioogle465-cloud/agentic-pay-demo.git
cd agentic-pay-demo

# 2. Crea entorno virtual e instala dependencias
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Inicia la API de banco
uvicorn mock_bank_api:app --reload --port 8000

# 4. En otra terminal, inicia Ollama y carga un modelo
ollama serve
ollama pull phi3:3.8b   # o llama3:8b

# 5. Ejecuta el agente
python agent.py
```

