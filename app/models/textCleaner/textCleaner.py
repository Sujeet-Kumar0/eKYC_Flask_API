import re

from app.utils import IdType


class TextCleaner:

    def __init__(self, idtype=None):
        self.idType = idtype
        self.pattern = re.compile(r'[^\w\s#\'.,\-/]+')
        self.date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
        self.word_pattern = re.compile(r'\b\w\b')

    def text_cleaner(self, text):
        # Remove all special characters and symbols except allowed ones
        text = self.pattern.sub('', text)

        # Replace all unicodes with an appropriate ASCII character
        text = text.encode('ascii', 'ignore').decode()

        if self.idType != IdType.AADHAARBACK and self.idType is None:
            # Replace all single letters that are not part of a word
            text = self.word_pattern.sub('', text)

            # Replace one or more consecutive newlines with a period and space
            # ehy needed because string literals from ocr directly contains blank newlines
            text = re.sub('\n+', '.', text)

        if self.idType == IdType.PAN:
            if self.date_pattern.match(text):
                # If date is found, don't remove forward slash
                return text

            # Remove forward slash input list
            text = text.replace('/', '')

            # Replace one or more consecutive newlines with a period and space
            text = re.sub('\n+', '. ', text)

        # Remove multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)

        return text
