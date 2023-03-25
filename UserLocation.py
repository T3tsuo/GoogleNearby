class UserLocation:

    def __init__(self, _person, place_name, lat, lon, is_there=False):
        self.place = {'name': place_name, 'latitude': lat, 'longitude': lon, 'at_location': is_there}
        self.person = _person
