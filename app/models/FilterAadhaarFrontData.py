import re
from datetime import datetime

import spacy

from app.utils import IdType
from .textCleaner.textCleaner import TextCleaner


# import spacy


def get_date(text):
    dob_match = re.search(r"(\d{2}/\d{2}/\d{4})", text)
    if dob_match:
        dob_str = dob_match.group(1)
        dob = datetime.strptime(dob_str, "%d/%m/%Y").date()
        return dob.strftime("%d/%m/%Y")
    else:
        return ""


def get_father_name(text):
    new_string = (
        text
        .replace("Father", "")
        .replace("father", "")
        .replace("FATHER", "").strip()
    )
    return new_string


def read_aadhaar_number(text):
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


def read_aadhaar_front_data(text):
    data = {
        "name": "",
        "DOB": "",
        "aadhaarNumber": "",
        "gender": "",
        "father": "",
        "issueDate": "",
        "idType": IdType.AADHAARFRONT.name,
    }

    cleaner = TextCleaner()
    text = cleaner.text_cleaner(text)

    lines = [line.strip() for line in text.split(".") if line.strip()]

    text = " ".join(lines)

    # Get aadhaar no from raw text

    aadhaar_match = read_aadhaar_number(text)
    # aadhaar_match = re.search(r"\d{4}\s\d{4}\s\d{4}", text)
    if aadhaar_match != "":
        data["aadhaarNumber"] = "".join(aadhaar_match.split())
        aadhaar_index = next(
            (i for i, line in enumerate(lines) if aadhaar_match in line),
            len(lines),
        )
        lines = lines[:aadhaar_index]
    else:
        return data

    if "female" in text.lower():
        data["gender"] = "FEMALE"
    elif "male" in text.lower():
        data["gender"] = "MALE"

    if data["gender"] != "":
        gender_index = next(
            (i for i, line in enumerate(lines) if data["gender"] in line.upper()),
            len(lines),
        )
        lines = lines[:gender_index]

    dob_match = re.search(r"(\d{2}/\d{2}/\d{4})", text)
    if dob_match:
        dob_str = dob_match.group(1)
        dob = datetime.strptime(dob_str, "%d/%m/%Y").date()
        data["DOB"] = dob.strftime("%d/%m/%Y")
    else:
        return data

    issue_date_index = -1
    goi_index = -1
    father_index = -1
    dob_index = len(lines)
    for index, line in enumerate(lines):
        # print(line.lower().find("india"))
        if line.lower().find("india") != -1:
            goi_index = index

        if line.lower().find("issue date") != -1:
            data["issueDate"] = get_date(line)
            issue_date_index = index

        if line.lower().find("father") != -1:
            data["father"] = get_father_name(line)
            father_index = index

        if line.upper().find("DOB") != -1:
            data["DOB"] = get_date(line)
            dob_index = index
            break

    if (issue_date_index + 1) > dob_index or issue_date_index != dob_index:
        if father_index != -1:
            lines = lines[:father_index]
        else:
            lines = lines[:dob_index]

        if goi_index != -1:
            lines = lines[goi_index + 1:]
        elif issue_date_index != -1:
            lines = lines[issue_date_index + 1:]

    # lines = [line for line in lines if len(line) > 4]

    text = ". ".join(lines)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # for ent in doc.sents:
    #     print(ent.text,list(doc.sents))
    #     for token in ent:
    #         print("ent",token.text,token.pos_)

    # print(list(doc.sents))
    new_list = []  # create an empty list to store name tokens
    for sent in doc.sents:  # iterate over each sentence in the document
        name_tokens = []  # create an empty list to store the name tokens
        # print(sent,len(sent))
        if len(sent) >= 2:
            for token in sent:  # iterate over each token in the sentence
                if token.is_alpha:  # check if the token is alphabetic
                    if not any(
                            c.isdigit() for c in token.text
                    ):  # check if the token does not contain any digits
                        if token.text[
                            0
                        ].isupper():  # check if the first character of the token is uppercase
                            if (
                                    len(token.text) >= 2 and token.text[1].islower()
                            ):  # check if the second character of the token is not uppercase, unless the token is only one character long
                                # print("first letter is upper",token.text)
                                name_tokens.append(
                                    token.text
                                )  # add the token to the list of name tokens
                            elif token.text.isupper():
                                # print("Captial",token.text)
                                name_tokens.append(
                                    token.text
                                )  # add the token to the list of name tokens
        new_list.append(" ".join(name_tokens))

    # print(new_list)
    data["name"] = " ".join([name for name in new_list if len(name) > 5])

    # name_tokens = [
    #     token.text
    #     for sent in doc.sents
    #     for token in sent
    #     if token.is_alpha
    #     and token.text[0].isupper()
    #     and not any(c.isdigit() for c in token.text)
    # ]
    # data["name"] = " ".join(name_tokens)

    # name_start = []
    # for i, char in enumerate(text):
    #     if char == ' ' and text[i - 1].isupper() and (text[i - 2].isalnum() or text[i - 2] == '.') and (
    #             text[i + 1].islower() or text[i + 1] == '.') and not any(c.isdigit() for c in text[i + 1:]):
    #         name_start.append(i)
    # data['Name'] = name_start

    return data
