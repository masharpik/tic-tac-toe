import os
from dotenv import load_dotenv


def get_env():
    load_dotenv()
    token = os.getenv('TOKEN')

    return {
        "TOKEN": token
    }


filename, extension = "field{}.png", "PNG"

texts = {
    "start": {
        "greeting": "Welcome, {}, to my room. Write the command /new_game to start the game.",
    },
    "new_game": {
        "choice": "Choose who you will play?",
        "role_accepted": 'Great! You will play for "{}".',
    },
    "end_game": {
        "win": 'You are win. Write the command /new_game to start the game.',
        "lose": 'You are lose. Write the command /new_game to start the game.',
        "tie": 'Tie. Write the command /new_game to start the game.',
    },
}
