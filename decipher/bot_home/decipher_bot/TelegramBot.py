from enum import Enum, auto
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from .events import Publisher, Subscriber


TOKEN :Final = '7448033384:AAFAebODHPDaVkDqS-XgS5u9KTOmiGf5YYw'
BOT_USERNAME :Final = '@thedecipher_bot'
class UserState(Enum):
    AWAITING_INTEGRATION_TOKEN = auto()
    AWAITING_PAGE_ID = auto()
    CONFIRMING_INPUT = auto()

class BotCommands(Enum):
    START = 'start'
    HELP = 'help'
    SET_INTEGRATION_TOKEN = 'set_integration_token'
    SET_PAGE_ID = 'set_page_id'

integration_token: str = ''
page_id: str = ''

user_state = {}

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_reply_txt = 'This is Decipher I can curate all the learning resourses for you, and set it up on notion. /help to get started and setup your integration token and page_id to let me start making notion pages for you'
    await update.message.reply_text(start_reply_txt)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_reply_txt = 'You have to enter your notion integration ID and notion page id to get started. Use commands /set_integration_id to save your integration id, /set_page_id to to save your page_id under which you want to create new decipher pages'
    await update.message.reply_text(help_reply_txt)

async def set_integration_token_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_txt = 'Enter your notion integration token'
    await update.message.reply_text(reply_txt)
    user_state[update.message.from_user.id] = UserState.AWAITING_INTEGRATION_TOKEN

    print(user_state[update.message.from_user.id])

async def set_page_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_txt = 'Enter your notion page id'
    await update.message.reply_text(reply_txt)
    user_state[update.message.from_user.id] = UserState.AWAITING_PAGE_ID

    print(user_state[update.message.from_user.id])

async def confirm_details(update: Update, _integration_token: str, _page_id: str):
    user_id = update.message.from_user.id
    user_state[user_id] = UserState.CONFIRMING_INPUT
    confirmation_txt = f'Integration token is: {_integration_token}\nPage ID: {_page_id}.\nIs this correct? (yes/no)'
    await update.message.reply_text(confirmation_txt)

# async def notify_details_confirmed(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     Publisher.dispatch('details_confirmed', integration_token, page_id)
#     await update.message.reply_text('Details notified')

# Responses

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global integration_token
    global page_id

    user_id = update.message.from_user.id
    text = update.message.text

    if user_id in user_state:
        state = user_state[user_id]
        print(state)
        
        match state:
            case UserState.AWAITING_INTEGRATION_TOKEN:
                integration_token = text
                await update.message.reply_text(f'Your Notion integration token has been set to: {integration_token}')
                print(f'Your Notion integration token has been set to: {integration_token}')
                if page_id:
                    await confirm_details(update, integration_token, page_id)
                else:
                    user_state.pop(user_id)

            case UserState.AWAITING_PAGE_ID:
                page_id = text
                await update.message.reply_text(f'Your Notion Page ID has been set to: {page_id}')
                print(f'Your Notion Page ID has been set to: {page_id}')
                if integration_token:
                    await confirm_details(update, integration_token, page_id)
                else:
                    user_state.pop(user_id)
            
            case UserState.CONFIRMING_INPUT:
                if text.lower() == 'yes':
                    user_state.pop(user_id)
                    print('Details Confirmed')
                    # Publisher.dispatch('details_confirmed', integration_token, page_id)
                    await update.message.reply_text('Great! You can start using decipher bot now, just enter a prompt and I will create a notion page for you.')
                elif text.lower() == 'no':
                    user_state.pop(user_id)
                    await update.message.reply_text('Please set your integration token and page id again.')

            case _:
                print(state)
                user_state.pop(user_id)
                await update.message.reply_text("I don't understand your request.")

    else:
        await update.message.reply_text("Please use a command to start")
    

def main():
    app = Application.builder().token(TOKEN).build()

    print('Bot Starting..')

    # Add command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('set_integration_token', set_integration_token_command))
    app.add_handler(CommandHandler('set_page_id', set_page_id_command))
    # app.add_handler(CommandHandler('notify_details', notify_details_confirmed))

    # Add message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    # Start the Bot
    print("Bot Polling...")
    app.run_polling(poll_interval=3)


if __name__ == '__main__':
    main()
