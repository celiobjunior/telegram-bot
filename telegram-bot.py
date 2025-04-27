import os
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Api keys
API_KEY: Final = os.getenv('TELEGRAM_API_KEY')
GEMINI_API_KEY: Final = os.getenv('GEMINI_API_KEY')

BOT_USERNAME: Final = os.getenv('BOT_USERNAME')

# Google Gemini
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL: Final = os.getenv('GEMINI_MODEL')

# Response tones
tone_instructions = {
    "balanceado": "Responda de forma equilibrada, combinando profissionalismo e cordialidade.",
    "serio": "Responda de forma séria, formal e direta, sem brincadeiras ou linguagem casual.",
    "divertido": "Responda de forma divertida e bem-humorada, usando um tom leve e descontraído."
}

# Default tone
current_tone = "balanceado"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = """
Olá! Sou seu assistente virtual. Aqui estão os comandos disponíveis:

/start - Iniciar o bot e ver lista de comandos
/help - Obter ajuda sobre como usar o bot
/serio - Mudar para um tom de resposta mais formal e direto
/divertido - Mudar para um tom de resposta mais leve e bem-humorado
/balanceado - Mudar para um tom de resposta equilibrado (padrão)

Basta digitar sua pergunta a qualquer momento para receber uma resposta!
"""
    await update.message.reply_text(commands)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start para ver todos os comandos disponíveis. Para fazer uma pergunta, apenas digite-a diretamente!")
    
async def set_tone_serio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_tone
    current_tone = "serio"
    await update.message.reply_text("Modo sério ativado. Responderei de forma formal e direta.")

async def set_tone_divertido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_tone
    current_tone = "divertido"
    await update.message.reply_text("Modo divertido ativado! Vou responder com mais humor e descontração! 😄")

async def set_tone_balanceado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_tone
    current_tone = "balanceado"
    await update.message.reply_text("Modo balanceado ativado. Responderei de forma equilibrada.")

async def handle_response(text: str) -> str:
    try:
        # Add tone instructions to the text
        prompt = f"{tone_instructions[current_tone]} Pergunta do usuário: {text}"
        
        # Use Google Gemini to process the message
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Desculpe, tive um problema ao processar sua mensagem. Por favor, tente novamente mais tarde."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: {text}')
    print("\n")

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = await handle_response(new_text)
        else:
            return
    else:
        if text:
            response: str = await handle_response(text)
        else:
            return

    print(f'Bot response: {response}')
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}') 
        
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(API_KEY).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('serio', set_tone_serio))
    app.add_handler(CommandHandler('divertido', set_tone_divertido))
    app.add_handler(CommandHandler('balanceado', set_tone_balanceado))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)