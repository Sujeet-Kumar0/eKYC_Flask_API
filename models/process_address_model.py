import re
import json
from utils import Path
import requests
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)


def find_by_pinCode(pincode):
    try:
        r = requests.get("https://api.postalpincode.in/pincode/" + pincode, timeout=2)

        if r.status_code == 200:
            pinDetails = r.json()
        else:
            pinDetails = None

    except Exception as e:
        # print(str(e))
        pinDetails = None
        pass

    if pinDetails is not None:
        if pinDetails[0]["Status"] == "Success":
            district = pinDetails[0]["PostOffice"][0]["District"]
            state = pinDetails[0]["PostOffice"][0]["State"]
            if len(pinDetails[0]["PostOffice"]) == 1:
                city = pinDetails[0]["PostOffice"][0]["Name"]

            return state, district

    return "", ""


def identify_location(address):
    address = re.sub("[.,]", " ", address.lower())

    with open(Path.STATES_JSON, "r") as file:
        text_from_file = file.read()

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
            (d for d in districts_set if d.lower() in address.lower()), ""
        )

    if address_district != "":
        print(f"{address_district} is in {state}")

    return state, address_district


def process_address(address):
    pattern = re.compile(r"[^\w\s#\'.,\-/]+")

    # Remove all special characters and symbols except allowed ones
    text = pattern.sub("", address)

    # Replace all unicodes with an appropriate ASCII character
    text = text.encode("ascii", "ignore").decode()

    # Remove multiple spaces with single space
    text = re.sub(r"\s+", " ", text)

    # extacting pin Code
    match = re.search(r"\d{6}", text)
    if match:
        pincode = match.group()
    else:
        pincode = ""

    start = text.lower().find("addr")
    if start == -1:
        pass
    else:
        start = start + 8
        text = text[start:]

    address = text.replace("-", "").replace(pincode, "")

    state, district = identify_location(text)

    if state == "" or district == "":
        with ThreadPoolExecutor() as executor:
            try:
                updated_state, updated_district = executor.submit(
                    find_by_pinCode, pincode
                ).result()
                state = updated_state if state == "" else state
                district = updated_district if district == "" else district
            except Exception as e:
                logger.error(
                    "Error updating state and district from pinCode.\nError: " + str(e),
                    stack_info=True,
                )
                pass

    return address, pincode, state, district
