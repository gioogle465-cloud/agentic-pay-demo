# 🏗️ Arquitectura del Proyecto

Este demo de agente AI utiliza una arquitectura modular y local-first para ejecutar operaciones de pago interpretando lenguaje natural. A continuación se describe cada componente clave y cómo interactúan entre sí.

---

## 🧠 1. Agente (agent.py)

- Recibe instrucciones en lenguaje natural del usuario.
- Las convierte en un JSON estructurado (intención + parámetros).
- Llama a la API simulada de banco para ejecutar la operación.
- Imprime o registra la respuesta.

> Ejemplo:  
> Entrada: "Transfiere $500 a Juan Pérez mañana"  
> → JSON: `{ "action": "transfer", "amount": 500, "to": "Juan Pérez", "date": "mañana" }`

---

## 🔗 2. Modelo LLM (local)

- Se ejecuta con [Ollama](https://ollama.ai), sin conexión a servicios externos.
- Se utiliza el modelo `phi3:3.8b` por su tamaño liviano y capacidad razonable.
- Extrae intención, entidades y parámetros del input.

---

## 💳 3. Mock Bank API (mock_bank_api.py)

- Servidor FastAPI simula un backend bancario.
- Expone endpoints REST para:
  - `/balance`
  - `/payments`
  - `/transactions`
- Incluye validación de idempotencia y control de errores.

---

## 🌐 4. Comunicación entre módulos

- El `agent.py` actúa como orquestador:
  - Interactúa con el LLM local por `subprocess`.
  - Realiza peticiones HTTP a la API simulada con `requests`.

---

## 🗂️ 5. Estructura del repositorio

agentic-pay-demo/
├── agent.py # Orquestador principal
├── mock_bank_api.py # API bancaria simulada
├── requirements.txt # Dependencias del entorno
├── docs/
│ └── architecture.md # Este documento
├── examples/
│ └── curl_commands.md # Pruebas manuales con curl
└── README.md # Guía general de uso

yaml
Copy code

---

## 📌 Notas adicionales

- Todos los componentes corren en local sin dependencias externas.
- El diseño permite extender el agente para integrar APIs reales o validar autorización.
- Pensado para ser funcional en demos offline o pruebas de concepto.

---
