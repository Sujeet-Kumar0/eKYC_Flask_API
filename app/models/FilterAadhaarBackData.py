import json
import os
import re

import spacy

from app.utils import Constants, TextFileManager, get_pinCode_details, IdType
from .textCleaner.textCleaner import TextCleaner


# class TextPreprocessor:

#     def __init__(self):
#         try:
#             self.nlp = spacy.load("en_core_web_sm")
#         except IOError:
#             os.system("python -m spacy download en_core_web_sm")

#     def extract_address(self, text):
#         """
#         Extracts the address and pin code from the given text.

#         Parameters:
#         text (str): The text to extract the address from.

#         Returns:
#         A tuple containing the address and pin code.
#         """
#         # find the index of the word 'address' in the text and set the starting point for processing the text
#         start = text.lower().find("addr")
#         if start == -1:
#             return "", ""
#         start = start + 8
#         text = text[start:]
#         # text = text.replace("£", "")
#         # use spacy to process the text
#         doc = self.nlp(text)
#         # create a list to store the address
#         address = []
#         pin_code = ""
#         pin_list = []
#         count = 0
#         # iterate through the tokens in the text
#         for token in doc:
#             # check if the token is a word that is likely to be part of the address
#             if (token.pos_ in [
#                     "NOUN", "PROPN", "ADJ", "ADV", "VERB", "ADP", "CONJ",
#                     "PART", "INTJ", "PUNCT"
#             ] or token.text in [".", ",", "-", "/", "#"] or token.like_num):
#                 address.append(token.text.strip())

#             # check if the token is a 6-digit number, which is likely to be the pin code
#             if token.like_num and len(token.text) == 6:
#                 pin_code = token.text
#                 pin_list.append(pin_code)
#                 count += 1

#             if count == 2:
#                 break

#         if pin_code:
#             address.reverse()
#             index = address.index(pin_code)
#             address = address[index:]
#             address.remove(pin_code)
#             if count == 2:
#                 if pin_list[0] == pin_list[1]:
#                     address.remove(pin_code)
#             address.reverse()

#         pattern = r"\s*([.\-/#])\s*"
#         # join the address list to create a string
#         addressRet = " ".join(address)
#         # Use the pattern to remove spaces from the symbols in the address
#         # as the address generate space around symbols while joining.from list to string
#         addressRet = re.sub(pattern, r"\1", addressRet)

#         return addressRet, pin_code

# class LocationIdentifier:

#     def __init__(self):
#         self.text_file_manager = TextFileManager()

#     def identify_location(self, address):
#         address = re.sub('[.,]', ' ', address.lower())

#         text_from_file = self.text_file_manager.read_text_from_file(
#             Constants.Path.STATES_JSON)

#         try:
#             location = json.loads(text_from_file)
#         except json.JSONDecodeError:
#             return "", ""

#         address_district = ""

#         # Find the state in the input string
#         state = ""
#         states_set = set(location["State"])
#         for s in states_set:
#             if s.lower() in address:
#                 state = s
#                 districts = location["State"][state]["District"]
#                 break
#         else:  # only run if the for loop is NOT exited with a break statement
#             ut_set = set(location["Union Territory"])
#             for s in ut_set:
#                 if s.lower() in address:
#                     state = s
#                     districts = location["Union Territory"][state]["District"]
#                     break

#         # If state is found, find the districts in the input string
#         if state != "":
#             # districts = location["State"][state]["District"]
#             districts_set = set(districts)
#             address_district = next(
#                 (d for d in districts_set if d.lower() in address.lower()), '')

#         if address_district != "":
#             print(f"{address_district} is in {state}")

#         return state, address_district


class AadhaarBackDataReader:

    def __init__(self):
        # self.address_extractor = TextPreprocessor()
        # self.location_identifier = LocationIdentifier()
        self.text_file_manager = TextFileManager()

        try:
            self.nlp = spacy.load("en_core_web_sm")
        except IOError:
            os.system("python -m spacy download en_core_web_sm")
        self.textCleaner = TextCleaner(IdType.AADHAARBACK)

    def get_occurences(self, text):
        # Find the index of the second occurrence of "S/O", "W/O", "D/O", or "C/O"
        prefix_count = 0
        for i, word in enumerate(text.split()):
            if any(prefix in word for prefix in ["S/O", "W/O", "D/O", "C/O"]):
                prefix_count += 1
                text = " ".join(text.split()[i:])
                if prefix_count == 2:
                    text = " ".join(text.split()[i:])
                    break
            else:
                text = ""
        return text

    def identify_location(self, address):
        address = re.sub('[.,]', ' ', address.lower())

        text_from_file = self.text_file_manager.read_text_from_file(
            Constants.Path.STATES_JSON)

        try:
            location = json.loads(text_from_file)
        except json.JSONDecodeError:
            return "", ""

        address_district = ""

        # Find the state in the input string
        state = ""
        states_set = set(location["State"])
        for s in states_set:
            if s.lower() in address:
                state = s
                districts = location["State"][state]["District"]
                break
        else:  # only run if the for loop is NOT exited with a break statement
            ut_set = set(location["Union Territory"])
            for s in ut_set:
                if s.lower() in address:
                    state = s
                    districts = location["Union Territory"][state]["District"]
                    break

        # If state is found, find the districts in the input string
        if state != "":
            # districts = location["State"][state]["District"]
            districts_set = set(districts)
            address_district = next(
                (d for d in districts_set if d.lower() in address.lower()), '')

        if address_district != "":
            print(f"{address_district} is in {state}")

        return state, address_district

    def extract_address(self, text):
        """
        Extracts the address and pin code from the given text.

        Parameters:
        text (str): The text to extract the address from.

        Returns:
        A tuple containing the address and pin code.
        """
        # # find the index of the word 'address' in the text and set the starting point for processing the text
        # start = text.lower().find("addr")
        # if start == -1:
        #     new_start = self.get_occurences(text)
        #     if new_start == -1:
        #         return "", ""
        #     else:
        #         start = new_start
        # else:
        #     start = start + 8

        # text = text[start:]
        # text = text.replace("£", "")
        # use spacy to process the text
        doc = self.nlp(text)
        # create a list to store the address
        address = []
        pin_code = ""
        pin_list = []
        count = 0
        # iterate through the tokens in the text
        for token in doc:
            # check if the token is a word that is likely to be part of the address
            if (token.pos_ in [
                "NOUN", "PROPN", "ADJ", "ADV", "VERB", "ADP", "CONJ",
                "PART", "INTJ", "PUNCT"
            ] or token.text in [".", ",", "-", "/", "#"] or token.like_num):
                address.append(token.text.strip())

            # check if the token is a 6-digit number, which is likely to be the pin code
            if token.like_num and len(token.text) == 6:
                pin_code = token.text
                pin_list.append(pin_code)
                count += 1

            if count == 2:
                break

        if pin_code:
            address.reverse()
            index = address.index(pin_code)
            address = address[index:]
            address.remove(pin_code)
            if count == 2:
                if pin_list[0] == pin_list[1]:
                    address.remove(pin_code)
            address.reverse()

        pattern = r"\s*([.\-/#])\s*"
        # join the address list to create a string
        addressRet = " ".join(address)
        # Use the pattern to remove spaces from the symbols in the address
        # as the address generate space around symbols while joining.from list to string
        addressRet = re.sub(pattern, r"\1", addressRet)

        return addressRet, pin_code

    def read_vid(self, text):
        pass

    def read_aadhaar_Number(self, text):
        # get vid
        vid_match = re.search(r"\d{4}\s\d{4}\s\d{4}\s\d{4}", text)
        if vid_match:
            vid = vid_match.group()
            text = text.replace(vid, "")
        else:
            vid = ""
        # Get the Aadhaar number
        aadhaar_match = re.search(r"\d{4}\s\d{4}\s\d{4}", text)
        if aadhaar_match:
            aadhaar_number = aadhaar_match.group()
        else:
            aadhaar_number = ""
        return aadhaar_number

    def read_aadhaar_back_data(self, text, data):

        if data["idType"] == "":
            data["idType"] = IdType.AADHAARBACK.name

        clean_text = self.textCleaner.text_cleaner(text)
        if clean_text == "":
            return None

        if data["aadhaarNumber"] == "":
            aadhaar_number = self.read_aadhaar_Number(text)
            data["aadhaarNumber"] = aadhaar_number
        else:
            aadhaar_number = data["aadhaarNumber"]

        # find the index of the word 'address' in the text and set the starting point for processing the text
        start = clean_text.lower().find("addr")
        if start == -1:
            clean_text = self.get_occurences(clean_text)
        else:
            start = start + 8
            clean_text = clean_text[start:]

        if aadhaar_number != "":
            end = clean_text.find(aadhaar_number)
            clean_text = clean_text[:end]

        #     if data["pinCode"] != "":
        #         end = clean_text.find(matches[0])
        #         clean_text = clean_text[:end]
        # else:
        #     end = clean_text.find(data["pinCode"])
        #     clean_text = clean_text[:end]

        og_address, pin_code = self.extract_address(clean_text)

        if pin_code == "" and data["pinCode"] == "":
            # Define a regular expression pattern to match the pincode
            pattern = r"\b\d{6}\b"

            # Find all matches of the pattern in the address string
            matches = re.findall(pattern, clean_text)

            # Extract the pincode from the matches
            data["pinCode"] = matches[0] if matches else ""

            if data["pinCode"] != "":
                end = clean_text.find(data["pinCode"])
                clean_text = clean_text[:end]
        else:
            data["pinCode"] = pin_code

        if og_address == "":
            data["aadhaarNumber"] = aadhaar_number
            data["og_add"] = og_address
            return data

        if data["district"] == "" or data["state"] == "":
            state, district = self.identify_location(og_address)
            if data["state"] == "":
                data["state"] = state
            elif state == "" and data["state"] != "":
                state = data["state"]
            if data["district"] == "":
                data["district"] = district
            elif district == "" and data["district"] != "":
                district = data["district"]
        else:
            district = data["district"]
            state = data["state"]

        # # Find the index of the second occurrence of "S/O", "W/O", "D/O", or "C/O"
        # prefix_count = 0
        # for i, word in enumerate(og_address.split()):
        #     if any(prefix in word for prefix in ["S/O", "W/O", "D/O", "C/O"]):
        #         prefix_count += 1
        #         og_address = " ".join(og_address.split()[i:])
        #         if prefix_count == 2:
        #             og_address = " ".join(og_address.split()[i:])
        #             break

        og_address = og_address.replace(".", " ")
        adres = og_address.split(",")
        city = ""

        # adres = [ad.strip() for ad in adres if ad.strip() and state not in ad]
        if state != "":
            adres = [
                ad.strip() for ad in adres
                if ad.strip() and state not in ad  # and district not in ad
            ]

        if district != "":
            for i, ad in enumerate(adres):
                if ad.lower() in district.lower():
                    # Remove the substring from the list of strings
                    adres[i] = ad.replace(district, "", 1)
                    break

        adres = [i for i in adres if i]

        if adres[-1].find("-") != -1:
            adres.pop()

        # Set the city to the last value of the list
        city = adres.pop() if len(adres) > 1 and len(
            adres[-1].split()) < 2 else ""

        # If there is only one value left, it is the address
        address = ", ".join(adres) if len(adres) > 1 else og_address

        # this works if there is no State or District Value found in the text
        # this class a function thats takes pincode as input and returns pincode information from online.
        # pincode information contains State and District along with the name of the postal offices.
        if data["pinCode"] != "" and (data["district"] == ""
                                      or data["state"] == ""):

            pinDetails = get_pinCode_details(data["pinCode"])

            if pinDetails[0]["Status"] == "Success":

                if data["district"] == "":
                    data["district"] = pinDetails[0]["PostOffice"][0][
                        "District"]
                    district = data["district"]

                if state == "":
                    state = pinDetails[0]["PostOffice"][0]["State"]

                if len(pinDetails[0]["PostOffice"]) == 1:
                    city = pinDetails[0]["PostOffice"][0]["Name"]

                data["pinVerification"] = True

            else:
                data["pinVerification"] = False

        # Get the result of the location
        # state, district = location_future.result()
        data = {
            "address": address.strip(),
            "district": district,
            "city": city,
            "state": state,
            "pinCode": pin_code,
            "og_add": og_address,
            "aadhaarNumber": aadhaar_number,
            "idType": IdType.AADHAARBACK.name,
        }

        myKeys = list(data.keys())
        myKeys.sort()
        data = {i: data[i] for i in myKeys}

        return data
