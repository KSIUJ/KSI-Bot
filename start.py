from app.bot import Bot
from app.config import get_token

if __name__ == "__main__":
    bot = Bot()
    bot.run(get_token())
