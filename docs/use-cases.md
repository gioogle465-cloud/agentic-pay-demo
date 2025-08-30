# 🧠 Casos de uso del demo agentic-pay

Este documento ilustra escenarios funcionales que muestran cómo este demo puede escalar hacia una solución de pagos con agentes AI para entornos empresariales, fintech o banca digital.

---

## 🏢 Caso 1: Pago de Nómina Automatizado

**Escenario:**
Un agente AI recibe una instrucción como:  
> "Envía el sueldo mensual a todos los empleados del archivo payroll_agosto.csv."

**Cómo lo resuelve el demo:**
- El archivo es interpretado por el agente.
- Se genera un conjunto de pagos con claves de idempotencia.
- Se ejecutan los pagos contra el endpoint `/payments`.
- Se devuelve un resumen con los resultados de cada pago.

---

## 🔄 Caso 2: Reintento Inteligente de Transferencia Fallida

**Escenario:**
> "Vuelve a intentar el pago a María si falló por falta de fondos."

**Cómo lo resuelve el demo:**
- El agente verifica transacciones fallidas en `/transactions`.
- Detecta la causa de fallo.
- Reintenta el pago automáticamente usando la misma clave de idempotencia para evitar duplicados.

---

## 🔗 Caso 3: Transferencias entre cuentas propias

**Escenario:**
> "Transfiere $2,000 MXN de mi cuenta de ahorro a mi cuenta corriente."

**Cómo lo resuelve el demo:**
- El agente identifica las cuentas del usuario.
- Crea una transacción con el monto especificado.
- Confirma y registra la operación en `/transactions`.

---

## 📲 Caso 4: Comandos en lenguaje natural vía Chat o API

**Escenario:**
> "Muestra los últimos 3 pagos a proveedores y sus fechas."

**Cómo lo resuelve el demo:**
- El agente interpreta el texto, genera la consulta.
- Llama a `/transactions` con filtros relevantes.
- Devuelve la respuesta en lenguaje natural o JSON estructurado.

---

## 🔮 Próximas extensiones posibles

- Integración con cuentas multiusuario.
- Capacidad para autorizar pagos mediante OTP o firmas.
- Conexión con modelos externos para validación de intención o scoring de riesgo.
- Persistencia en base de datos (actualmente in-memory).

---

📎 Estos casos ilustran cómo un sistema basado en lenguaje natural y agentes puede:
- Aumentar la productividad de equipos de finanzas.
- Reducir errores operativos.
- Ofrecer experiencias de usuario conversacionales.

