from utils.user import User
from utils.bot import WordBot as wb
from telethon.sync import events
import asyncio, string

# Initialize global variables
user = User()
bot = wb()
bot.importWords()
config = {
    "delay": 2,
    "playingGroup": None,
    "user": {},
    "spam": "",
    "contains": "",
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
        "is accepted.",
        "won the game",
        "Total words:"
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
         
async def main() -> None:
    """
    Main function, this is required to run the bot.

    Returns:
        None
    """

    config["user"] = await user.fetchInfo(user.client)
    # The number that starts with "840338206" is the wordchain bot's id
    config.update({"players": [config["user"]["id"], 840338206]})

    await user.client.start()
    await user.client.run_until_disconnected()

@user.client.on(events.NewMessage)
async def handler(event) -> None:
    """
    Telegram messages handler.

    Args:
        event(object, required): Interacts with new messages.
    
    Returns:
        None
    """

    if event.sender_id in config["players"]:
        # Handling prompts by user
        if any(event.raw_text.startswith(prompt) for prompt in config["user-prompts"]):
            msg = event.raw_text.split()
            match msg[0]:
                case "/time": # Change the delay of bot sending the word, which 2 is default
                    updateConfig(delay=int(msg[1]))
                case "/spam": # Spams a letter that ends with your intended suffix
                    updateConfig(spam=msg[1].lower())
                case _: # Sets the group chat where the user joins a game
                    updateConfig(playingGroup=event.chat_id)
            await user.client.delete_messages(entity=event.chat_id, 
                                              message_ids=event.id) \
                if any(event.raw_text.
                    startswith(prompt) for prompt in config["user-prompts"][:2]) else None

        # Bot interacts with the game playing
        elif event.chat_id == config["playingGroup"]:
            if any(prompt in event.raw_text for prompt in config["game-prompts"]):
                msg = event.raw_text.split()

                # Removes the word at the beginning of the game
                if config["game-prompts"][0] in event.raw_text:
                    firstWord = msg[4].rstrip(".").lower()
                    bot.removeWord(word=firstWord)

                    # Handles banned letter if the game mode is banned letters
                    maxlen = msg.index("Turn")
                    banned_letters = " ".join(msg[7:maxlen]).replace(",", "").split()
                    config["bannedLetters"].extend(char.lower() for char in 
                                                    banned_letters if any(
                                                    char))
                
                # Removes the word that is accepted by the game
                elif config["game-prompts"][1] in event.raw_text:
                    word = msg[0].lower()
                    bot.removeWord(word=word)

                # Restart bot when game ends and its config
                elif config["game-prompts"][2] in event.raw_text \
                and config["game-prompts"][3] in event.raw_text:
                    bot.importWords()
                    config["spam"] = ""
                    config["contains"] = ""
                    config["bannedLetters"] = []

            # Send a word when it is our turn
            elif config["user"]["turn"] in event.raw_text:
                for num in [3, 4, 5, 6, 7, 8, 9, 10]:
                    if f"at least {num}" in event.raw_text:
                        bot.filterDict(limit=num)
                        break
                for char in string.ascii_uppercase:
                    if f"Your word must start with {char}" in event.raw_text:
                        for letter in string.ascii_uppercase:
                            if f"include {letter}" in event.raw_text:
                                config["contains"] = letter.lower()
                                break
                        
                        async with user.client.action(entity=event.chat_id,
                                                        action="typing",):
                            await asyncio.sleep(config["delay"])
                            await user.client.send_message(entity=event.chat_id,
                                                            message=bot.getWord(prefix=char.lower(),
                                                                                suffix=config["spam"],
                                                                                contains=config["contains"],
                                                                                banned=config["bannedLetters"]))
                                                    
if __name__ == "__main__":
    print("Bot Started!")
    asyncio.run(main())
