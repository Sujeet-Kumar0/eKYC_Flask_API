import requests


def get_pinCode_details(pincode):
    r = requests.get("https://api.postalpincode.in/pincode/" + pincode)

    if r.status_code == 200:
        return r.json()


if __name__ == "__main__":
    print(get_pinCode_details("751012")[0]["PostOffice"][0]["Name"])
