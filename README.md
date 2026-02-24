#  Weather Report Telegram bot

Um script em Python simples e eficiente que envia um relatório completo de previsão do tempo diretamente para o seu Telegram. O bot consome os dados da API **HG Brasil Weather** e formata a mensagem de forma amigável, incluindo a temperatura atual, umidade, velocidade do vento e a previsão para os próximos dias.

##  Funcionalidades

- **Saudação Dinâmica**: O bot envia "Bom dia", "Boa tarde" ou "Boa noite" dependendo do horário em que o script é executado.
- **Resumo Atual**: Mostra a temperatura no momento, descrição do clima (nublado, ensolarado, etc.), probabilidade de chuva, ventos e umidade.
- **Previsão Futura**: Informa a mínima, máxima e condições climáticas para os próximos dias.
- **Segurança**: Uso da biblioteca `dotenv` para esconder chaves de API e Tokens de bots (nunca exponha suas credenciais!).

##  Pré-requisitos

Antes de começar, você precisará de:
1. **Python 3.x** instalado no seu computador ou servidor.
2. Um **Token de Bot no Telegram** (crie um conversando com o [@BotFather](https://t.me/botfather) no Telegram).
3. O **Chat ID** do seu usuário, grupo ou canal no Telegram onde o bot enviará as mensagens.
4. Uma **API Key** gratuita da [HG Brasil Weather](https://hgbrasil.com/).

##  Instalação e Configuração

**1. Clone ou baixe este repositório**
```bash
git clone https://github.com/seu-usuario/telegram-clima-bot.git
cd telegram-clima-bot
```

**2. Instale as dependências**
O projeto requer as bibliotecas `requests` e `python-dotenv`. Instale-as usando o pip:
```bash
pip install requests python-dotenv
```

**3. Configure suas variáveis de ambiente**
Crie um arquivo chamado `.env` na raiz do projeto e adicione as suas credenciais no seguinte formato:
```env
TELEGRAM_TOKEN=seu_token_do_bot_aqui
TELEGRAM_CHAT_ID=seu_chat_id_aqui
HG_API_KEY=sua_chave_hg_brasil_aqui
CIDADE=Sao Paulo,SP
```
*(Dica: Para maior precisão na busca, utilize o formato da cidade como `NomeDaCidade,UF`)*.

##  Como usar

Basta executar o script principal no seu terminal:
```bash
python clima_bot.py
```

Você deverá ver a mensagem `"✅ Relatório de previsão do tempo enviado com sucesso!"` no terminal e receberá uma mensagem no Telegram parecida com esta:

> **Bom dia** 🌞  
> A temperatura agora é de 13°c e Tempo nublado.  
> Está prevista mínima de 11°c e máxima de 23°c para hoje.  
> ☂️ 100%  
> 💨 1.54 km/h  
> 💧 88%  
>  
> Previsão para os próximos dias:  
>  
> **25/02**  
> Min 13°c  
> Max 23°c  
> Chuvas esparsas  

##  Dica: Automação

Para que você receba esse relatório todos os dias automaticamente, você pode agendar a execução deste script:
- **No Linux/Mac:** Use o `crontab`. Exemplo para rodar todo dia às 07:00 da manhã:
  `0 7 * * * /caminho/para/o/python /caminho/para/o/clima_bot.py`
- **No Windows:** Use o "Agendador de Tarefas" (Task Scheduler) para disparar o script diariamente.

##  Observação sobre a API (Limitação de dias)

Caso você utilize o **Plano Gratuito (Free)** da HG Brasil Weather, a API retornará apenas **o dia atual + 1 dia de previsão**. Portanto, a seção "Próximos dias" mostrará apenas o dia de amanhã. 
Para exibir 3 dias ou mais de previsão futura, é necessário fazer upgrade para um plano "Member" ou superior diretamente no site da HG Brasil. O script já está configurado para mostrar até 3 dias caso o seu plano da API permita.

##  Licença

Este projeto é de código aberto. Sinta-se à vontade para clonar, modificar e utilizar em seus projetos pessoais!


