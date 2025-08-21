# 💳 Agentic Pay Demo

Este proyecto es un **demo de agente AI** que entiende lenguaje natural y ejecuta operaciones contra un **API de pagos simulado**.

## 🚀 Qué incluye
- **Mock Bank API**: FastAPI con endpoints de saldo, pagos (con idempotencia) y transacciones.
- **Agente (agent.py)**: Toma instrucciones en texto, las convierte en JSON y llama al API.
- **LLM local con Ollama**: Procesa el lenguaje natural sin depender de servicios externos.
- **Documentación extra** en `docs/` y ejemplos en `examples/`.

## 🛠️ Requisitos
- Python 3.10+
- [Ollama](https://ollama.ai) instalado y corriendo (`ollama serve`)
- FastAPI + Uvicorn (`pip install fastapi uvicorn requests`)

## ▶️ Cómo correr el demo

1. Clonar repo:
   ```bash
   git clone https://github.com/carlosreyes/agentic-pay-demo.git
   cd agentic-pay-demo

2.Crear entorno virtual e instalar dependencias:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
3. Iniciar el Mock Bank API:
uvicorn mock_bank_api:app --reload --port 8000
4.En otra ventana, iniciar Ollama:
ollama serve
ollama pull phi3:3.8b   # o llama3.1:8b
5.En otra ventana, correr el agente:
python agent.py
Ejemplos de uso
Usuario: ¿Cuál es mi saldo?
Agente: Saldo disponible en acc_001: 5000.0 MXN.

Usuario: Paga 500 MXN a Jorge
Agente: Pago de 500 MXN a Jorge realizado. Balance después: 4500.0 MXN.

Usuario: Muéstrame mis últimos 3 pagos
Agente: Lista de transacciones [...]
📂 Recursos
Arquitectura

Ejemplos cURL

3. Guarda con `CTRL + O` → Enter y sal con `CTRL + X`.

---

👉 ¿Quieres que después preparemos también el `requirements.txt` (lista de dependencias) para que cualquiera pueda instalar el demo sin errores?

