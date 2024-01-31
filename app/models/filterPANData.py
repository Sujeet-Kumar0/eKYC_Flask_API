import os
import re
from datetime import datetime

import spacy

from app.utils import IdType
from .textCleaner.textCleaner import TextCleaner


class PANDataReader:

    def __init__(self):
        self.text_cleaner = TextCleaner(idtype=IdType.PAN)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except IOError:
            os.system("python -m spacy download en_core_web_sm")

    def read_pan_data(self, text):
        data = {'name': None,
                'fatherName': None,
                'DOB': None,
                'pan': None,
                'idType': IdType.PAN.name}

        if not text:
            return data

        clean_data = ''
        for i in text:
            clean_data += self.text_cleaner.text_cleaner(i)

        if not clean_data:
            return data

        doc = self.nlp(clean_data)

        # remove newline characters and trailing white spaces from each sentence in the list
        sents = [str(sent).strip().replace(".", "") for sent in doc.sents]

        # Extract DOB from date entities
        date_ents = [ent for ent in doc.ents if ent.label_ == "DATE"]
        if date_ents:
            dob_str = date_ents[0].text
        else:
            date_pattern = re.compile(r"\d{2}/\d{2}/\d{4}")
            dob_match = date_pattern.search(clean_data)
            dob_str = dob_match.group() if dob_match else None

        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%d/%m/%Y").date()
                data["DOB"] = dob.strftime("%d/%m/%Y")
            except ValueError:
                pass

        # Extract Name and Father's Name
        for i, sent in enumerate(sents):

            if "INCOME TAX DEPARTMENT" in sent:
                data["name"] = sents[i + 1]
                fname_match = sents[i + 2]

                if fname_match and "Permanent Account" not in fname_match:
                    data["fatherName"] = fname_match
                break

            name_match = re.search(r"Name", sent, re.IGNORECASE)
            if name_match and len(sents) > i + 1:
                data["name"] = sents[i + 1]
                for j in range(i + 2, len(sents)):
                    fname_match = re.search(r"Father[']?s?\s+Name", sents[j], re.IGNORECASE)
                    if fname_match:
                        data["fatherName"] = sents[j + 1]
                        # data["Father Name"] = fname_match.group(1).strip()
                        break
                break

        # Extract PAN from PAN sentence
        pan_match = None
        for i in range(len(sents) - 1):
            if sents[i] == "Permanent Account Number":
                pan_match = re.search(r'([A-Z]){5}([O0-9]){4}([A-Z]){1}', sents[i + 1])
                if pan_match:
                    data["pan"] = pan_match.group()
                break

        if not pan_match:
            # Extract PAN
            pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]{1}", clean_data)
            if pan_match:
                data["pan"] = pan_match.group()

        data["lines"] = sents
        return data
