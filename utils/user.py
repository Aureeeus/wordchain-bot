import json
from telethon.sync import TelegramClient


class User:
    def __init__(self):
        """
        User initializer for making a Telegram Client Object

        Features:
            API_ID and API_HASH will be prompt when the value is null,
            this is good for handling user's data and not prompting when
            there's already a value.
        """
        with open('database/config.json', 'r+') as file:
            data = json.load(file)
            try:
                self.API_ID = data['api-id']
                self.API_HASH = data['api-hash']

                if (self.API_ID is None and self.API_HASH is None):
                    raise ValueError
            except ValueError:
                self.API_ID = int(input("Enter your API ID: "))
                self.API_HASH = str(input("Enter your API HASH: "))

                dataUpdate = {
                    "api-id": self.API_ID,
                    "api-hash": self.API_HASH
                }

                # Update details
                for key, value in dataUpdate.items():
                    data[key] = value
                file.seek(0)
                json.dump(dataUpdate, file, indent=4)
            finally:
                self.client = TelegramClient(session="anon",
                                             api_hash=self.API_HASH,
                                             api_id=self.API_ID)

    @staticmethod
    async def fetchInfo(client: TelegramClient) -> dict:
        """
        Gets the user's info that pertains to the 
            Turn: {user.firstName} {user.lastName}

        Args:
            client(TelegramClient, required): The method needs to work 
                with this client object.

        Returns a dictionary type with user's info.
        """

        async with client:
            info = {}  # Empty for now, will add keys and value to it later
            me = await client.get_me()

            info.update({"turn": f"Turn: {me.first_name} {me.last_name}" if me.last_name is not None
                         else f"Turn: {me.first_name}",
                         "id": me.id})
            return info
