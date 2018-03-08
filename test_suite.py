# check that all latitude and longitude values are valid
import unittest
from find_store import LocationFinder, EARTH_KM_RADIUS
from math import pi


class TestStoreFinder(unittest.TestCase):
    """
    I didn't test the output function, or that the Geocoder service works- I am assuming that is tested
    independently. I did test the formulas and logic I had to implement myself.
    """

    def setUp(self):
        self.store_finder = LocationFinder()

    def test_csv_read_successful(self):
        # first check that there is data in the list
        self.assertGreater(len(self.store_finder.store_list), 0)

        # now check for valid input information
        first_entry = self.store_finder.store_list[0]
        self.assertEqual(len(first_entry), 3)
        self.assertIsInstance(first_entry[0], str)
        self.assertIsInstance(first_entry[1], float)
        self.assertIsInstance(first_entry[2], float)

        # check latitude and longitude within correct range
        self.assertTrue(-90 <= first_entry[1] <= 90)
        self.assertTrue(-180 <= first_entry[2] <= 180)

    def test_haversine_distance(self):
        # check that same coordinates produces 0
        self.assertEqual(self.store_finder.haversine_distance(10.0, 11.0, 10.0, 11.0), 0)
        self.assertAlmostEqual(self.store_finder.haversine_distance(0, -180.0, 0.0, 180.0), 0, 4)

        # check known distance for sanity (distance from north to south pole along circumference of Earth)
        self.assertAlmostEqual(self.store_finder.haversine_distance(-90.0, 0, 90.0, 0), EARTH_KM_RADIUS * pi, 5)

    def test_find_nearest_location_and_distance(self):
        # check that this outputs the right answer to at least one query. This is unfortunately reliant on
        # the list/store locations not changing, but its worth the sanity check
        distance, address = self.store_finder.find_nearest_location_and_distance('218 Hemenway Street Boston')

        self.assertIsInstance(distance, float)
        self.assertIsInstance(address, str)

        self.assertTrue(distance < 1)
        self.assertTrue('Boston, MA' in address)


if __name__ == '__main__':
    unittest.main()
