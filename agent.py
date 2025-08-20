import json
import uuid
import requests

# =========================
#   CONFIG: Mock Bank API
# =========================
BASE = "http://127.0.0.1:8000"
BANK_HEADERS = {"X-API-Key": "demo-key-123"}

def api_get_balance(account_id="acc_001"):
    r = requests.get(f"{BASE}/v1/accounts/{account_id}/balance", headers=BANK_HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()

def api_list_transactions(account_id="acc_001", limit=10):
    r = requests.get(
        f"{BASE}/v1/accounts/{account_id}/transactions",
        headers=BANK_HEADERS,
        params={"limit": limit},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()

def api_make_payment(source_account_id="acc_001", amount=0.0, currency="MXN",
                     destination_name="", idempotency_key=None):
    if not idempotency_key:
        idempotency_key = f"auto-{uuid.uuid4().hex[:8]}"
    headers = dict(BANK_HEADERS)
    headers["Idempotency-Key"] = idempotency_key
    body = {
        "source_account_id": source_account_id,
        "amount": float(amount),
        "currency": currency,
        "destination_name": destination_name,
    }
    r = requests.post(f"{BASE}/v1/payments", headers=headers, json=body, timeout=10)
    if r.status_code >= 400:
        try:
            detail = r.json().get("detail")
        except Exception:
            detail = r.text
        raise RuntimeError(f"API error {r.status_code}: {detail}")
    data = r.json()
    data["idempotency_key_used"] = idempotency_key
    return data

# =========================
#        OLLAMA LLM
# =========================
def ollama_generate(prompt: str, model: str = "phi3:3.8b", temperature: float = 0) -> str:
    resp = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False, "options": {"temperature": temperature}},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json().get("response", "").strip()

# =========================
#   PROMPTS & UTILIDADES
# =========================
SYSTEM_INSTRUCTIONS = """Eres un agente de pagos.
Tienes tres acciones válidas (no inventes otras):
- get_balance(account_id?: str = "acc_001")
- make_payment(source_account_id?: str = "acc_001", amount: float, currency?: "MXN", destination_name: str, idempotency_key?: str)
- list_transactions(account_id?: str = "acc_001", limit?: int = 10)

Cuando decidas usar una acción, RESPONDE EXCLUSIVAMENTE con UN objeto JSON válido y nada más (sin texto antes ni después), en una sola línea:
{"action":"<nombre>","params":{...}}

Ejemplos:
{"action":"get_balance","params":{"account_id":"acc_001"}}
{"action":"make_payment","params":{"source_account_id":"acc_001","amount":500,"currency":"MXN","destination_name":"Jorge"}}
{"action":"list_transactions","params":{"account_id":"acc_001","limit":3}}

Si no vas a llamar acción, responde texto normal. Mantén todo conciso y claro.
"""

def extract_first_json_object(text: str):
    """Encuentra el PRIMER objeto JSON { ... } balanceando llaves (sin comerse texto extra)."""
    start = text.find('{')
    if start == -1:
        return None
    depth = 0
    for i, ch in enumerate(text[start:], start=start):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                chunk = text[start:i+1]
                try:
                    return json.loads(chunk)
                except Exception:
                    return None
    return None

def plan_action(user_text: str) -> str:
    prompt = (
        SYSTEM_INSTRUCTIONS
        + "\n\nUsuario: "
        + user_text
        + "\nRecuerda: si llamas acción, responde SOLO JSON como en los ejemplos."
    )
    return ollama_generate(prompt)

# =========================
#          MAIN
# =========================
def main():
    print("=== Agentic Payments (Ollama + Mock Bank API) ===")
    print("Ejemplos: '¿Cuál es mi saldo?', 'Paga 500 MXN a Jorge', 'Muéstrame mis últimos 3 pagos'.")
    print("Escribe 'exit' para salir.")
    while True:
        try:
            user_text = input("\nTú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            break
        if user_text.lower() in ("exit", "quit", "salir"):
            break

        raw = plan_action(user_text)

        # Parseo robusto: toma el primer JSON aunque el modelo agregue texto extra
        action = None
        params = {}
        maybe = extract_first_json_object(raw)
        if isinstance(maybe, dict) and "action" in maybe:
            action = maybe["action"]
            params = maybe.get("params", {}) or {}

        if action == "get_balance":
            try:
                account_id = params.get("account_id", "acc_001")
                data = api_get_balance(account_id)
                print(f"Agente: Saldo disponible en {data['account_id']}: {data['available_balance']} {data['currency']}.")
            except Exception as e:
                print(f"Agente: Ocurrió un error consultando saldo: {e}")

        elif action == "make_payment":
            try:
                source_account_id = params.get("source_account_id", "acc_001")
                amount = params["amount"]
                currency = params.get("currency", "MXN")
                destination_name = params["destination_name"]
                idk = params.get("idempotency_key")
                data = api_make_payment(source_account_id, amount, currency, destination_name, idk)
                print(
                    "Agente: Pago completado "
                    f"(ref {data['reference']}) por {data['amount']} {data['currency']} a {destination_name}. "
                    f"Saldo después: {data['balance_after']}. (idemp: {data['idempotency_key_used']})"
                )
            except KeyError:
                print("Agente: Falta 'amount' y/o 'destination_name' para procesar el pago.")
            except Exception as e:
                print(f"Agente: No pude procesar el pago: {e}")

        elif action == "list_transactions":
            try:
                account_id = params.get("account_id", "acc_001")
                limit = int(params.get("limit", 10))
                data = api_list_transactions(account_id, limit)
                txs = data.get("transactions", [])
                if not txs:
                    print("Agente: No hay transacciones recientes.")
                else:
                    lines = [
                        f"- {t['created_at']} | {t['amount']} {t['currency']} → {t['to']} (ref {t['reference']})"
                        for t in txs
                    ]
                    print("Agente:\n" + "\n".join(lines))
            except Exception as e:
                print(f"Agente: Error al listar transacciones: {e}")

        else:
            # Respuesta libre si el modelo no eligió acción
            print(f"Agente: {raw or '¿Podrías reformular tu solicitud?'}")

if __name__ == "__main__":
    main()
