import db_handler
from os import sys
import json

# + ---------------- boiler plate tdd -------------------------------- +
def print_fail(message):
    red_color = "\033[31m"
    reset_color = "\033[0m"    
    sys.stdout.write(f"{red_color}{message}{reset_color}\n")

def print_success(message):
    light_green_color = "\033[92m"
    reset_color = "\033[0m"
    sys.stdout.write(f"{light_green_color}{message}{reset_color}\n")

def verdict(a, b, msg ):
    if ( a == b ):
        print_success("PASS {}".format(msg))        
    else:
        print_fail("FAIL {}".format(msg))
        print(a)
    
# + ---------------- tests -------------------------------------------- +

def test_validate_user():
    actual = db_handler.validate_user("kermitt","a")
    verdict(True, actual, "test_validate_user")

def test_get_stores():
    actual = db_handler.get_stores()
    expected = [{'address': '232 Alameda, Oregon City, OR', 'lat': 45.3573, 'lon': -122.6068, 'merchantId_fk': 1, 'name': 'Kitty Buds', 'phone': '5032492584', 'storeId': 1, 'image': 'big_kittybuds.jpg'}, {'address': '3000 NE Alberta, LA, CA', 'lat': 34.0522, 'lon': -118.2437, 'merchantId_fk': 1, 'name': 'Bright Flower', 'phone': '5032492999', 'storeId': 2, 'image': 'big_brightflower.jpg'}, {'address': '223 SW 18th ave, NYC, NY', 'lat': 40.7128, 'lon': -74.006, 'merchantId_fk': 2, 'name': 'House of Johnson', 'phone': '9714342669', 'storeId': 3, 'image': 'big_house_of_johnson.jpg'}]
    verdict(actual, expected, "test_validate_user")


if __name__ == '__main__':
    test_validate_user()
    test_get_stores()