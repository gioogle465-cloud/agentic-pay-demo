# Arquitectura del Demo Agentic Pay

## Componentes
- **agent.py**: Interpreta lenguaje natural y decide qué acción ejecutar (consultar saldo, hacer un pago, listar transacciones).
- **Ollama (LLM local)**: Procesa la entrada de texto y genera una instrucción JSON.
- **mock_bank_api.py**: API de pagos simulada con FastAPI.
  - GET /v1/accounts/{id}/balance
  - POST /v1/payments
  - GET /v1/accounts/{id}/transactions

## Flujo
1. Usuario escribe algo en lenguaje natural → “¿Cuál es mi saldo?”
2. El agente convierte eso en una acción JSON → `{"action":"get_balance","params":{"account_id":"acc_001"}}`
3. El agente llama al **Mock Bank API**.
4. API responde con datos (ej: saldo disponible).
5. El agente responde al usuario en lenguaje natural.

## Diagrama (alto nivel)

```mermaid
flowchart LR
  U[Usuario] --> A[Agente (agent.py)]
  A -->|JSON acción| API[Mock Bank API]
  API --> A
  A --> U

