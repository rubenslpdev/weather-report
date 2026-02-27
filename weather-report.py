import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HG_API_KEY = os.getenv("HG_API_KEY")
CIDADE = os.getenv("CIDADE")

def get_saudacao():
    """Retorna uma saudação baseada na hora atual do sistema."""
    hora = datetime.now().hour
    if hora < 12:
        return "Bom dia 🌞"
    elif hora < 18:
        return "Boa tarde 🌤️"
    else:
        return "Boa noite 🌙"

def buscar_previsao_tempo():
    """Busca os dados de clima na API da HG Brasil Weather"""
    url = "https://api.hgbrasil.com/weather"
    params = {
        "key": HG_API_KEY,
        "city_name": CIDADE
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("results", {})
    except Exception as e:
        print(f"Erro ao buscar dados do clima: {e}")
        return None

def enviar_mensagem_telegram(mensagem, chat_id=None):
    """Envia a mensagem formatada para o Telegram"""
    alvo_chat_id = chat_id or TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": alvo_chat_id,
        "text": mensagem,
        "parse_mode": "HTML" # Usar HTML para garantir que o negrito (<b>) funcione sem erros
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("✅ Relatório de previsão do tempo enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem para o Telegram: {e}")

def main():
    # O chat_id pode vir via argumento (pelo listener) ou do .env (pelo cron)
    custom_chat_id = sys.argv[1] if len(sys.argv) > 1 else None

    # Verifica se todas as chaves estão no .env
    if not all([TELEGRAM_TOKEN, HG_API_KEY, CIDADE]) or (not custom_chat_id and not TELEGRAM_CHAT_ID):
        print("⚠️ Verifique seu arquivo .env. Faltam variáveis de ambiente.")
        return

    dados_clima = buscar_previsao_tempo()
    
    if not dados_clima:
        return

    # Extração das variáveis atuais
    temp_atual = dados_clima.get("temp")
    descricao_atual = dados_clima.get("description")
    wind_speedy = dados_clima.get("wind_speedy")
    humidity = dados_clima.get("humidity")
    
    # A lista 'forecast' contém a previsão diária.
    # O índice [0] é o dia de hoje. Os índices [1], [2] e [3] são os próximos dias.
    previsao = dados_clima.get("forecast", [])
    hoje = previsao[0]
    
    hoje_min = hoje.get("min")
    hoje_max = hoje.get("max")
    rain_probability = hoje.get("rain_probability")
    
    # Montagem da mensagem usando formatação HTML para o Telegram
    saudacao = get_saudacao()
    
    mensagem = f"<b>{saudacao}</b>\n"
    mensagem += f"A temperatura agora é de {temp_atual}°c e {descricao_atual}.\n"
    mensagem += f"Está prevista mínima de {hoje_min}°c e máxima de {hoje_max}°c para hoje.\n"
    mensagem += f"☂️ {rain_probability}%\n"
    mensagem += f"💨 {wind_speedy}\n"
    mensagem += f"💧 {humidity}%\n\n"
    mensagem += "Previsão para os amanhã:\n\n"
    
    # Pega os próximos 3 dias de previsão (índices 1 a 3)
    proximos_dias = previsao[1:4]
    
    for dia in proximos_dias:
        mensagem += f"<b>{dia.get('date')}</b>\n"
        mensagem += f"Min {dia.get('min')}°c\n"
        mensagem += f"Max {dia.get('max')}°c\n"
        mensagem += f"{dia.get('description')}\n\n"
        
    # Remove espaços ou quebras de linha em excesso no final
    mensagem = mensagem.strip()
    
    # Envia a mensagem
    enviar_mensagem_telegram(mensagem, custom_chat_id)

if __name__ == "__main__":
    main()
