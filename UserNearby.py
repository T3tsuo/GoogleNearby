class UserNearby:

    def __init__(self, _person, timestamp, near):
        self.timestamp = timestamp
        self.near = near
        self.person = _person

    def can_refresh(self, full_name, current_time, is_near):
        # if it's the same person, and it has been over an hour since the last update, and their last state is not
        # the same as the current state
        return self.person.full_name == full_name and current_time > self.timestamp and self.near != is_near
