# 🧪 Comandos curl de prueba

Estos ejemplos muestran cómo interactuar con la API bancaria simulada usando `curl`. Son útiles para pruebas manuales o automatización con scripts.

---

## 🔍 Obtener saldo

```bash
curl -X GET http://localhost:8000/balance
💸 Realizar un pago
bash
Copy code
curl -X POST http://localhost:8000/payments \
  -H "Content-Type: application/json" \
  -d '{
    "to_account": "juan_perez",
    "amount": 500,
    "currency": "MXN",
    "idempotency_key": "test-12345"
  }'
Reemplaza "idempotency_key" con un valor único por transacción si pruebas múltiples veces.

📄 Consultar transacciones
bash
Copy code
curl -X GET http://localhost:8000/transactions
🔁 Reintentar pago con misma clave de idempotencia
bash
Copy code
curl -X POST http://localhost:8000/payments \
  -H "Content-Type: application/json" \
  -d '{
    "to_account": "juan_perez",
    "amount": 500,
    "currency": "MXN",
    "idempotency_key": "test-12345"
  }'
Este ejemplo debería retornar la misma transacción sin duplicar el cargo.
