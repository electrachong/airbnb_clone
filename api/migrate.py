import sys
sys.path.insert(0, './app/models')
import base
from user import User
from state import State
from city import City
from place import Place
from amenity import Amenity
from place_book import PlaceBook
from place_amenity import PlaceAmenities

base.database.create_tables([User, State, City, Place, Amenity, PlaceBook, PlaceAmenities])
