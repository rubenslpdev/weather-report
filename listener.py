import os
import sys
import time
import requests
import subprocess
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def get_updates(offset=None):
    """Faz long polling na API do Telegram para obter novas mensagens."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    try:
        # timeout no requests deve ser maior que o timeout do long polling
        response = requests.get(url, params=params, timeout=35)
        response.raise_for_status()
        return response.json().get("result", [])
    except Exception as e:
        print(f"Erro ao obter atualizações: {e}")
        return []

def main():
    if not TELEGRAM_TOKEN:
        print("⚠️ Verifique seu arquivo .env. Falta a variável TELEGRAM_TOKEN.")
        sys.exit(1)

    print("Iniciando listener do Telegram...")
    offset = None
    
    # Caminho absoluto para o worker, independente de onde rodamos o listener
    script_dir = os.path.dirname(os.path.abspath(__file__))
    worker_path = os.path.join(script_dir, "weather-report.py")

    while True:
        updates = get_updates(offset)
        for update in updates:
            # Atualiza o offset para não receber a mesma mensagem novamente
            offset = update["update_id"] + 1
            
            if "message" in update and "text" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"]["text"].strip()
                
                if text == "/clima":
                    print(f"Comando /clima recebido do chat {chat_id}. Acionando worker...")
                    # Executa o worker via subprocesso sem bloquear o listener 
                    # usando sys.executable para garantir a mesma versão do python
                    subprocess.Popen([sys.executable, worker_path, str(chat_id)])
        
        # Pausa curta para evitar CPU 100% caso dê erro no request
        time.sleep(1)

if __name__ == "__main__":
    main()
