import random
import unittest
from farm_optimize import scipy_min_find_optimal_crops

#data from powell2011representative
crops = [
    {"season": "Summer", "applied water": 8, "name": "Cotton (BT, irrigated)", "yield": 9.5, "price": 538},
    {"season": "Summer", "applied water": 4, "name": "Cotton (semi-irrigated)", "yield": 6.5, "price": 518},
    {"season": "Summer", "applied water": 0, "name": "Cotton (dryland)", "yield": 3.5, "price": 488},
    {"season": "Summer", "applied water": 7.15, "name": "Maize (irrigated)", "yield": 9, "price": 287},
    {"season": "Summer", "applied water": 4.5, "name": "Sorghum (irrigated)", "yield": 8, "price": 242},
    {"season": "Summer", "applied water": 1.5, "name": "Sorghum (semi irrigated)", "yield": 5.5, "price": 242},
    {"season": "Summer", "applied water": 5.8, "name": "Soybean (irrigated)", "yield": 3, "price": 350},
    {"season": "Winter", "applied water": 0, "name": "Chickpea (dryland)", "yield": 1.3, "price": 468},
    {"season": "Winter", "applied water": 2.7, "name": "Faba bean (irrigated)", "yield": 5, "price": 348},
    {"season": "Winter", "applied water": 0, "name": "Faba bean (dryland)", "yield": 1.4, "price": 348},
    {"season": "Winter", "applied water": 0, "name": "Wheat (bread, dryland)", "yield": 1.8, "price": 244},
    {"season": "Winter", "applied water": 1.5, "name": "Wheat (bread, semi irrigated)", "yield": 4, "price": 244},
    {"season": "Winter", "applied water": 3.6, "name": "Wheat (bread, irrigated)", "yield": 7, "price": 244},
    {"season": "Winter", "applied water": 3.6, "name": "Wheat (durum, irrigated)", "yield": 7, "price": 275},
    {"season": "Winter", "applied water": 1.4, "name": "Vetch (irrigated)", "yield":0, "price":0}
]


class TestFarmOpt(unittest.TestCase):

    # def setUp(self):
    #     self.seq = range(10)

    def test_random_sums(self):
    	water = random.random()*1500
    	land = random.random()*1000
    	res = scipy_min_find_optimal_crops(crops, land, water)
    	self.assertLessEqual(sum([res.x[i] for i,crop in enumerate(crops) if crop["season"] == "Summer" ]), land+1)
    	self.assertLessEqual(sum([res.x[i] for i,crop in enumerate(crops) if crop["season"] == "Winter" ]), land+1)
    	self.assertLessEqual(sum([res.x[i] * crop["applied water"] for i,crop in enumerate(crops)]), water+1)
    	self.assertGreaterEqual(sum([res.x[i] * crop["yield"] * crop["price"] for i, crop in enumerate(crops)]), 0)

    def test_unlimited_water(self):
    	res = scipy_min_find_optimal_crops(crops, 1300, 1e32)
        self.assertAlmostEqual(res.x[0], 1300, 1)
        self.assertEqual(crops[0]["name"], "Cotton (BT, irrigated)")

    def test_typical_drought(self):
    	res = scipy_min_find_optimal_crops(crops, 1300, 800)
        self.assertAlmostEqual(res.x[0], 100, 1)
        self.assertEqual(crops[0]["name"], "Cotton (BT, irrigated)")
        self.assertAlmostEqual(res.x[2], 1200, 1)
        self.assertEqual(crops[2]["name"], "Cotton (dryland)")
        self.assertAlmostEqual(res.x[7], 1300, 1)
        self.assertEqual(crops[7]["name"], "Chickpea (dryland)")


if __name__ == '__main__':
    # tests
    unittest.main()