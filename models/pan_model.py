import re
from datetime import datetime


def text_cleaner(text):
    pattern = re.compile(r"[^\w\s#\'.,\-/]+")
    # Remove all special characters and symbols except allowed ones
    text = pattern.sub("", text)

    # Replace all unicodes with an appropriate ASCII character
    text = text.encode("ascii", "ignore").decode()

    # Replace one or more consecutive newlines with a period and space
    text = re.sub("\n+", ". ", text)

    # Remove forward slash input list
    text = text.replace("/", "")

    # Remove multiple spaces with single space
    text = re.sub(r"\s+", " ", text)

    return text


def filter_name(nameData):
    clean_text = text_cleaner(nameData)

    regex = r"(Income Tax Dept\.|Income Tax Department|Permanent Account Number Card|INCOME TAX DEPARTMENT)"
    reg = r"(Permanent|Account|Number|INCOME|TAX|DEPARTMENT)"
    clean_text = re.sub(regex, "", clean_text)
    clean_text = re.sub(reg, "", clean_text)

    # remove any digits in the text
    clean_text = re.sub(r"\d+", "", clean_text)

    # remove any "name"
    if "name".lower() in clean_text.lower():
        idx = clean_text.find("Name")
        clean_text = clean_text[idx + 5 :]

    # remove dots
    sents = clean_text.split(".")
    clean_text = max([sent for sent in sents if sent.strip()], key=len, default="")

    return clean_text.strip()


def filter_father_name(fatherName):
    clean_text = text_cleaner(fatherName)
    pattern = r"[\w\s]*INCOME[\w\s]*"
    clean_text = re.sub(pattern, "", clean_text.upper())
    father_name = ""

    sents = clean_text.split(".")
    sents = [sent for sent in sents if sent.strip()]
    if len(sents) <= 1:
        return sents[0]
    for i, sent in enumerate(sents):
        fname_match = re.search(r"Father", sent, re.IGNORECASE)
        if fname_match and len(sents) > i + 1:
            father_name = sents[i + 1]
    return father_name.strip()


def filter_p_a_n_Number(panData):
    pan_number = ""
    pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]{1}", panData)
    if pan_match:
        pan_number = pan_match.group()
    return pan_number


# Extract DOB from date entities
def filter_d_o_b(dobData):
    dob = ""
    date_pattern = re.compile(r"\d{2}/\d{2}/\d{4}")
    dob_match = date_pattern.search(dobData)
    dob_str = dob_match.group() if dob_match else ""

    if dob_str:
        try:
            dob = datetime.strptime(dob_str, "%d/%m/%Y").date()
            dob = dob.strftime("%d/%m/%Y")
        except ValueError:
            pass
    return dob
