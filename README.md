# 🧠 Agentic Pay Demo

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

