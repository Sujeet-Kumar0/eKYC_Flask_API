import unittest

from models.FilterAadhaarBackData import TextPreprocessor


class TestAddressExtraction(unittest.TestCase):

    def setUp(self):
        self.extractor = TextPreprocessor()

    def test_extract_address_no_match(self):
        text = "This is some random text."
        expected_output = ("", "")
        self.assertEqual(self.extractor.extract_address(text), expected_output)

    def test_read_aadhaar_back_data(self):
        raw_text = "Print Date 11/11/2020 5/0 , -/ , , , , 522413 Address S/O Venkaiah, 8-594/15, NEAR JAMUNA SCHOOL, Piduguralla, Guntur, Andhra Pradesh, 522413 5 "
        expected_output = (
            "S/O Venkaiah , 8-594/15 , NEAR JAMUNA SCHOOL , Piduguralla , Guntur , Andhra Pradesh ,",
            "522413")
        result = self.extractor.extract_address(raw_text)
        self.assertEqual(result, expected_output)
        self.maxDiff = None

    # def test_read_aadhaar_back_data2(self):
    #     raw_text = ""
    #     expected_output = ("", "")
    #     result = self.extractor.extract_address(raw_text)
    #     self.assertEqual(result, expected_output)
    #     self.maxDiff = None


if __name__ == '__main__':
    unittest.main()
