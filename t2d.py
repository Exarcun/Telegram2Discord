import discord
from discord import Intents
import asyncio
from telegram import Update
from telegram import Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import logging

#Logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize
telegram_bot = Bot('6910311009:AXFs4EkQT6N_pjnk1cEz84ptHgUTylSAwNg')
intents = discord.Intents.default()  
intents.messages = True              
intents.message_content = True       
discord_client = discord.Client(intents=intents) 


@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if message.channel.id == discord_channel_id:
        message_content = message.content  # Get the message content
        logging.info(f"Raw message content: {message_content}")  # Log the raw message content

        formatted_message = f"from Discord {message.author}: {message_content}"
        logging.info(f"Received message on Discord: {formatted_message}")

        # Send the message to Telegram chat
        telegram_chat_id = -4025797250
        await telegram_bot.send_message(chat_id=telegram_chat_id, text=formatted_message)




#Telegram Bot 
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    chat_type = update.message.chat.type  # Type of chat - private or group
  
    if chat_type == 'private':
        sender_name = update.message.from_user.first_name
    else:  
        sender_name = update.message.from_user.first_name
        
    formatted_message = f"from {sender_name} in Telegram chat: {message_text}"
    
    logging.info(f"Received message on Telegram: {formatted_message}")

    # Forward to Discord
    channel = discord_client.get_channel(discord_channel_id)
    if channel:
        await channel.send(formatted_message)
        logging.info(f"Sent message to Discord: {formatted_message}")

      
        

if __name__ == '__main__':
    # Discord Bot Token and Channel ID
    discord_token = 'MTE5MSM0MzgwMTI1NjIxODc2NQ.GPDpSw.RaHQSBN50v_Z59oaBv9s8hz9IWw4hw-zcjo2TU'
    discord_channel_id = 1192121235808866374

    # Discord Bot Run in Background
    asyncio.get_event_loop().create_task(discord_client.start(discord_token))

    # Telegram Bot
    telegram_token = '6910301009:AAFs4EkQT6N_pjnk1cEz84ptHgUTylSAwNg'
    application = ApplicationBuilder().token(telegram_token).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    application.run_polling()
