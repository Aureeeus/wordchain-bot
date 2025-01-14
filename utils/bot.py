import random

class WordBot:
    def __init__(self):
        """
        Bot Initializer
        """
        self.Y_SPAM = ["youthfully", "youthfullity", "yearningly", "yearnfully",
                       "yieldingly", "yellowbelly", "youngberry", "yellowberry"]
        self.dictionary = []
    
    def importWords(self) -> None:
        """
        Import words to the bot's dictionary.
        """

        with open('database/words.txt', 'r') as file:
            self.dictionary.clear()
            for word in file:
                self.dictionary.append(word.strip().lower()) if len(word) > 2 else None
    
    def filterDict(self, limit: int = 3) -> None:
        """
        Filters the bot's dictionary, 
        the words' length should be 3 or more.
        """
        
        self.dictionary = [
            word for word in self.dictionary if len(word) >= limit
            ]

    def removeWord(self, word: str) -> None:
        """
        Remove's word to the bot's dictionary,
        generally used when the game accepted a word.

        Args:
            word(str, required): The word to be removed.
        
        Returns:
            None
        """

        try:
            self.dictionary.remove(word)
            self.Y_SPAM.remove(word)
        except ValueError:
            None

    def getWord(self,
                prefix: str,
                suffix: str = "",
                contains: str = "", 
                banned: list = []) -> str:
        """
        Filters a list of words based on given criteria.

        Args:
            prefix (str, required): Words must start with this prefix.
            suffix (str, optional): Words must end with this suffix. Defaults to "".
            contains (str, optional): Words must contain these characters. Defaults to "".
            banned (list, optional): Words must not contain any of these characters. Defaults to [].

        Returns:
            str: A list of words that meet the specified criteria.
        """

        subDictionary = [
            word for word in self.dictionary if word.startswith(prefix) 
            and word.__contains__(contains) and not any(letter in word for letter in banned)
            and word.endswith(suffix)
            ]
        
        return random.choice(subDictionary) if subDictionary else self.getWord(prefix=prefix,
                                                                               suffix="",
                                                                               contains=contains,
                                                                               banned=banned)
