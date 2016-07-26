from app import models
import models.database

database.create_tables([User, State, City, Place, Amenity, PlaceBook, PlaceAmenities])
