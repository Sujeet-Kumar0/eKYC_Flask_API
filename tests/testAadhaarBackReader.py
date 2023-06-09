import unittest
from models.FilterAadhaarBackData import AadhaarBackDataReader


class TestAadhaarBackDataReader(unittest.TestCase):

    def setUp(self):
        self.reader = AadhaarBackDataReader()
        self.data = {
            "address": "",
            "district": "",
            "city": "",
            "state": "",
            "pinCode": "",
            "og_add": "",
            "aadhaarNumber": "",
            "idType": "",
        }

    def test_read_aadhaar_back_data(self):

        raw_text = "_ 5/0 seex Dovoadr 8 #0IOI, Ser pap. AHI SnvodsoB decsss, Sayo Sas. SOR OD, PAY AIK,. Frese - 590008. Address. S/O Late Narayana.D, #1282, Opp Silk. Factory Manandavadi Road, Nellur Shed,. Mysore, Mysore,. Karnataka - 570008. 2120. Download Date 21'. are. 5131 6855 1928. . __VID 9109 5450 43 7. ' Game 1247 bj help uidai.gov.in cep ww. uidai. guw.in i. a. secencd."
        expected_output = {
            "aadhaarNumber": "513168551928",
            "address": "S/O Late Narayana.D, #1282, Opp Silk.Factory Manandavadi Road, Nellur Shed",
            "city": "Mysore",
            "district": "Mysore",
            "idType": "AADHAARBACK",
            # "og_add": "S/O Late Narayana.D, #1282, Opp Silk.Factory Manandavadi Road, Nellur Shed, Mysore, Mysore ,Karnataka-",
            "pinCode": "570008",
            "state": "Karnataka"
        }
        result = self.reader.read_aadhaar_back_data(raw_text, self.data)
        self.assertEqual(result, expected_output)
        self.maxDiff = None

    def test_read_aadhaar_back_data2(self):
        raw_text = " CPS DV CoQoly Sedsrd Hog. orb Unique Identification Authonty of india. ee. OUSPSr. S/O Dgrordes, 3-118/0, raredvo 38,. es0650, ey Ror se,. wog 385 - 34111. Address. S/O Satyanarayana, 3-118/B,. ramalayam street, Ananthapalle, West. Godavari,. Andhra Pradesh - 534111. 9994 2972 1088"
        expected_output = {
            "aadhaarNumber": "999429721088",
            "address": "S/O Satyanarayana, 3-118/B, .ramalayam street",
            "city": "Ananthapalle",
            "district": "West Godavari",
            "idType": "AADHAARBACK",
            # "og_add": "S/O Satyanarayana , 3-118/B ,.ramalayam street , Ananthapalle , West.Godavari ,.Andhra Pradesh-",
            "pinCode": "534111",
            "state": "Andhra Pradesh"
        }
        result = self.reader.read_aadhaar_back_data(raw_text,self.data)
        self.assertEqual(result, expected_output)
        self.maxDiff = None


if __name__ == '__main__':
    unittest.main()
