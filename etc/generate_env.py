# generate_env.py
import os
from pathlib import Path
import secrets

env_file = Path(".env")

defaults = {
    "POSTGRES_USER": os.getenv("POSTGRES_USER", "admin"),
    "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD", secrets.token_urlsafe(20)),
    "POSTGRES_DB": os.getenv("POSTGRES_DB", "todo_app"),
    "DB_HOST": os.getenv("DB_HOST", "localhost"),
    "DB_PORT": os.getenv("DB_PORT", "5432"),
    "APP_PORT": os.getenv("APP_PORT", "8000"),
    "APP_IMAGE_NAME": os.getenv("APP_IMAGE_NAME", "todo-app"),
}

print("Generating .env file with the following values:")
for k, v in defaults.items():
    masked = v if "PASSWORD" not in k else "[hidden]"
    print(f"  {k} = {masked}")

with env_file.open("w") as f:
    for k, v in defaults.items():
        f.write(f"{k}={v}\n")

print("\n.env file created!")