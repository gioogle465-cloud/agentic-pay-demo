from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

app = FastAPI(title="Mock Bank API", version="1.0.0")

# Clave "de juguete" que debe venir en el header X-API-Key
API_KEY = "demo-key-123"

# ---------- Modelos ----------
class PaymentRequest(BaseModel):
    source_account_id: str
    amount: float
    currency: str = "MXN"
    destination_name: str

class PaymentResponse(BaseModel):
    payment_id: str
    status: str
    reference: str
    amount: float
    currency: str
    created_at: str
    balance_after: float

# ---------- "Base de datos" en memoria ----------
db = {
    "accounts": {
        "acc_001": {"balance": 5000.0, "currency": "MXN", "owner": "Carlos Reyes"},
    },
    "transactions": {
        "acc_001": []
    },
    "idempotency": {}
}

# ---------- Helper de seguridad ----------
def require_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

# ---------- Endpoints ----------
@app.get("/v1/accounts/{account_id}/balance")
def get_balance(
    account_id: str,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
):
    require_api_key(x_api_key)
    acc = db["accounts"].get(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return {
        "account_id": account_id,
        "available_balance": round(acc["balance"], 2),
        "currency": acc["currency"]
    }

@app.get("/v1/accounts/{account_id}/transactions")
def list_transactions(
    account_id: str,
    limit: int = 10,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
):
    require_api_key(x_api_key)
    txs = db["transactions"].get(account_id, [])
    return {
        "account_id": account_id,
        "count": min(len(txs), limit),
        "transactions": txs[-limit:][::-1]
    }

@app.post("/v1/payments", response_model=PaymentResponse)
def create_payment(
    payment: PaymentRequest,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
):
    require_api_key(x_api_key)

    # Idempotencia básica en memoria
    if idempotency_key and idempotency_key in db["idempotency"]:
        return db["idempotency"][idempotency_key]

    acc = db["accounts"].get(payment.source_account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Source account not found")

    if acc["currency"] != payment.currency:
        raise HTTPException(status_code=400, detail="Currency mismatch")

    if payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be > 0")

    if acc["balance"] < payment.amount:
        raise HTTPException(status_code=402, detail="Insufficient funds")

    # Debitar y registrar transacción
    acc["balance"] -= payment.amount
    pid = "pay_" + uuid.uuid4().hex[:8]
    ref = "TRX_" + uuid.uuid4().hex[:6].upper()
    created_at = datetime.utcnow().isoformat() + "Z"

    tx = {
        "payment_id": pid,
        "reference": ref,
        "amount": payment.amount,
        "currency": payment.currency,
        "to": payment.destination_name,
        "created_at": created_at
    }
    db["transactions"].setdefault(payment.source_account_id, []).append(tx)

    resp = PaymentResponse(
        payment_id=pid,
        status="COMPLETED",
        reference=ref,
        amount=payment.amount,
        currency=payment.currency,
        created_at=created_at,
        balance_after=round(acc["balance"], 2)
    )

    if idempotency_key:
        db["idempotency"][idempotency_key] = resp

    return resp
