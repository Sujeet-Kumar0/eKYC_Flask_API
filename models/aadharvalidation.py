import re


class CheckAadhaar:
    def __init__(self):
        self.verhoeff_table_d = (
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
            (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
            (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
            (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
            (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
            (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
            (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
            (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
            (9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
        )
        self.verhoeff_table_p = (
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
            (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
            (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
            (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
            (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
            (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
            (7, 0, 4, 6, 9, 1, 3, 2, 5, 8)
        )
        self.verhoeff_table_inv = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)

    def isValidAadhaarNumber(self, number):
        # Regex to check valid
        # Aadhaar number.
        regex = "^[2-9]{1}[0-9]{3}\\" + "s[0-9]{4}\\s[0-9]{4}$"

        # Compile the ReGex
        p = re.compile(regex)

        # If the string is empty
        # return false
        if number == None:
            return False

        # Return if the string
        # matched the ReGex
        if re.search(p, number):
            return True
        else:
            return False

    def checksum(self, number):
        """For a given number generates a Verhoeff digit and
        returns number + digit"""

        c = 0

        for i, item in enumerate(reversed(str(number))):
            c = self.verhoeff_table_d[c][self.verhoeff_table_p[i % 8][int(item)]]

        return c == 0


# obj = CheckAadhaar()
# a = obj.checksum(838579916690)
# print(a)

# b = obj.isValidAadhaarNumber("838579916690")
# print(b)
