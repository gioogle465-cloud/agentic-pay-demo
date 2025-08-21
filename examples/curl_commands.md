# Ejemplos de llamadas cURL

Todas requieren header de API Key:
-H "X-API-Key: demo-key-123"

## Consultar saldo
curl -s -H "X-API-Key: demo-key-123" \
http://127.0.0.1:8000/v1/accounts/acc_001/balance

## Crear un pago
curl -s -X POST -H "X-API-Key: demo-key-123" \
-H "Content-Type: application/json" \
-H "Idempotency-Key: test-123" \
-d '{"source_account_id":"acc_001","amount":500,"currency":"MXN","destination_name":"Jorge"}' \
http://127.0.0.1:8000/v1/payments

## Listar transacciones
curl -s -H "X-API-Key: demo-key-123" \
"http://127.0.0.1:8000/v1/accounts/acc_001/transactions?limit=3"

