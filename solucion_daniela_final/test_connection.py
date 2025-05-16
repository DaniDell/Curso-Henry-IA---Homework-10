"""
Script para probar la conexión a Supabase usando solo la API REST (sin supabase-py).
Requiere instalar requests:
    pip install requests

Configura las variables de entorno SUPABASE_URL y SUPABASE_KEY antes de ejecutar.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Carga automáticamente las variables del .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE = os.getenv("SUPABASE_TEST_TABLE", "test")  # Cambia por una tabla real si existe



if not SUPABASE_URL or not SUPABASE_KEY:
    print("[ERROR] Debes definir SUPABASE_URL y SUPABASE_KEY en tus variables de entorno.")
    exit(1)

# Construir endpoint REST
endpoint = f"{SUPABASE_URL}/rest/v1/{TABLE}"
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Accept": "application/json"
}

try:
    response = requests.get(endpoint, headers=headers, timeout=10)
    if response.status_code == 200:
        print("[OK] Conexión exitosa a Supabase REST API.")
        print("Ejemplo de respuesta:", response.json())
    else:
        print(f"[ERROR] Código {response.status_code}: {response.text}")
except Exception as e:
    print(f"[ERROR] No se pudo conectar a Supabase: {e}")
