# basic version of the program which was run to test the functionality of the bot
# necessary to prove whether the bot connected to the twitch chat and was able to detect the messages
# not to be considered with alignment of the flowchart






import os
from twitchio.ext import commands

# Replace these with your own credentials
BOT_TOKEN = '45pn817eczcun2j7470fdd9o2ni6xi'  # Replace with your new OAuth token
CHANNEL = 'kyedae'
DETECTION_TEXT = 's'

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=BOT_TOKEN, prefix='!', initial_channels=[CHANNEL])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Make sure the bot ignores itself
        if message.author.name.lower() == self.nick.lower():
            return

        print(f'Received message: {message.content} from user: {message.author.name}')

        # Check if the message contains the detection text
        if DETECTION_TEXT in message.content:
            print(f"Detection Text '{DETECTION_TEXT}' found in message: {message.content}")

bot = Bot()

# Added detailed error handling
try:
    bot.run()
except Exception as e:
    print(f"An error occurred: {e}")
