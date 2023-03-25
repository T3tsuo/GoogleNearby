class UserLocation:

    def __init__(self, _person):
        self.places = []
        self.person = _person

    def add_place(self, place_name, lat, lon, is_there):
        self.places.append({'name': place_name, 'latitude': lat, 'longitude': lon, 'at_location': is_there})

    def remove_place(self, place_name):
        index = 0
        found = False
        for place in self.places:
            if place["name"] == place_name:
                found = True
                break
            else:
                index += 1
        if found:
            self.places.pop(index)
