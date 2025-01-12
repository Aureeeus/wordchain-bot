from utils.user import User
from utils.bot import WordBot as wb
from telethon.sync import events
import asyncio, re

# Initialize global variables
user = User()
bot = wb()
bot.importWords()
config = {
    "delay": 0,
    "playingGroup": None,
    "user": None,
    "spam": "",
    "bannedLetters": [],
    "user-prompts": [
        "/time", 
        "/spam",
        "/join@on9wordchainbot", 
        "/startclassic@on9wordchainbot",
        "/startrl@on9wordchainbot",
        "/startbl@on9wordchainbot",
        "/starthard@on9wordchainbot",
        "/startcfl@on9wordchainbot",
        "/startrfl@on9wordchainbot",
        "/join"
    ],
    "game-prompts": [
        "The first word",
        "Banned letters:",
        "is accepted"
    ]
}

def updateConfig(**kwargs: dict) -> None:
    """
    Config updater. Sets the config.

    Args:
        kwargs(any, required): Utilized a dict because arguments are still unknown.
    
    Returns:
        None
    """
    for key, value in kwargs.items():
        config[key] = value
         
async def main():
    config["user"] = await user.fetchInfo(user.client)
    # The number that starts with "840338206" is the wordchain bot's id
    config.update({"players": [config["user"]["id"], 840338206]})

    await user.client.start()
    await user.client.run_until_disconnected()

@user.client.on(events.NewMessage)
async def handler(event):
    if event.sender_id in config["players"]:
        # Handling prompts by user
        if any(event.raw_text.startswith(prompt) for prompt in config["user-prompts"]):
            msg = event.raw_text.split()
            match msg[0]:
                case "/time":
                    updateConfig(delay=int(msg[1]))
                case "/spam":
                    updateConfig(spam=msg[1])
                case _:
                    updateConfig(playingGroup=event.chat_id)
            await user.client.delete_messages(entity=event.chat_id, 
                                              message_ids=event.id) \
                if any(event.raw_text.
                    startswith(prompt) for prompt in config["user-prompts"][:2]) else None

        # Bot interacts with the game playing
        elif event.chat_id == config["playingGroup"]:
            if any(prompt in event.raw_text for prompt in config["game-prompts"]):
                msg = event.raw_text.split()
                try:
                    max = msg.index("Turn")
                    modify = " ".join(msg[:max])
                    letters = " ".join(msg[7:max]).replace(",", "").split()

                    if modify.startswith("The first word"):
                        removedWord = msg[4].rstrip(".").lower()
                        bot.removeWord(removedWord)

                        # Handles banned letter game
                        config["bannedLetters"].extend([char for char in letters if any(char)])
                        print(config["bannedLetters"])
                except ValueError:
                    modify = " ".join(msg)

                    if "is accepted." in modify:
                        removedWord = msg[0].lower()
                        bot.removeWord(removedWord)
                        print("HEllo")

if __name__ == "__main__":
    print("Bot Started!")
    asyncio.run(main())



