import os
from twitchio.ext import commands
import sqlite3
from datetime import datetime

# Database setup
class DatabaseManager:
    def __init__(self):
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect('chat_log.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS chat_log (
                     username TEXT,
                     message TEXT,
                     timestamp TEXT
                     )''')
        conn.commit()
        conn.close()
        print("Database and table created successfully")

    def log_message(self, username, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect('chat_log.db')
        c = conn.cursor()
        c.execute("INSERT INTO chat_log (username, message, timestamp) VALUES (?, ?, ?)",
                  (username, message, timestamp))
        conn.commit()
        conn.close()
        print(f"Logged message: {message} from user: {username}")

    def is_message_logged(self, username, message):
        conn = sqlite3.connect('chat_log.db')
        c = conn.cursor()
        c.execute("SELECT * FROM chat_log WHERE username=? AND message=?", (username, message))
        result = c.fetchone()
        conn.close()
        return result is not None

class Bot(commands.Bot):
    def __init__(self, username, token, channel, detection_text, detection_threshold):
        super().__init__(token=token, prefix='!', initial_channels=[channel])
        self.detection_text = detection_text
        self.detection_threshold = detection_threshold
        self.detection_count = 0
        self.db_manager = DatabaseManager()

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Make sure the bot ignores itself
        if message.author.name.lower() == self.nick.lower():
            return

        username = message.author.name
        message_content = message.content

        print(f"Received message: {message_content} from user: {username}")

        if not self.db_manager.is_message_logged(username, message_content):
            self.db_manager.log_message(username, message_content)
            if self.detection_text in message_content:
                self.detection_count += 1
                print(f"Detection Text '{self.detection_text}' count: {self.detection_count}")
                if self.detection_count >= self.detection_threshold:
                    self.end_capture()

    def end_capture(self):
        with open('end_clip.txt', 'w') as file:
            file.write('')  # Write an empty string to the file
        print("Detection threshold reached. Ending capture.")
        self.loop.stop()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("streamer", help="the name of the streamer")
    parser.add_argument("detection_text", help="the text to detect in chat")
    args = parser.parse_args()

    streamer = args.streamer
    detection_text = args.detection_text
    detection_threshold = 10  # Set your desired detection threshold here

    username = 'nulltrades'  # The bot's Twitch username
    token = '45pn817eczcun2j7470fdd9o2ni6xi'  # The bot's OAuth token
    channel = streamer

    bot = Bot(username, token, channel, detection_text, detection_threshold)
    bot.run()
