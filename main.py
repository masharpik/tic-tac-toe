from utils import get_env
from bot import TicTacToeBot


if __name__ == '__main__':
    env = get_env()

    bot = TicTacToeBot(env["TOKEN"])
    bot.start()
