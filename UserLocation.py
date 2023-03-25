class UserLocation:

    def __init__(self, _person, place_name, lat, lon, is_there=False):
        self.place = {'name': place_name, 'latitude': lat, 'longitude': lon, 'at_location': is_there}
        self.person = _person

    def match(self, full_name, place_name, lat, lon):
        return self.person.full_name == full_name and self.place["name"] == place_name and \
            self.place["latitude"] == lat and self.place["longitude"] == lon
