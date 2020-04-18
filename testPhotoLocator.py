import unittest
import photolocator

class TestPhotoLocator(unittest.TestCase)

    def test_addGPSTags(self):
        #send lat and long and an image with no gps tags

        #verify that the image now has the lat and long in the tags