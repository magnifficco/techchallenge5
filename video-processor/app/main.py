print("[DEBUG] Entrou no main.py")
from app.worker.consumer import process_messages

if __name__ == "__main__":
    print("[DEBUG] Rodando process_messages()")
    process_messages()
