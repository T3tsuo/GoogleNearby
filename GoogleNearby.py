import time
from locationsharinglib import Service
import os
import pickle
from math import cos, asin, sqrt, pi
import smtplib

from UserLocation import UserLocation

if os.path.isfile("email.dat"):
    google_email = pickle.load(open("email.dat", "rb"))

if os.path.isfile("mail_password.dat"):
    mail_password = pickle.load(open("mail_password.dat", "rb"))

black_listed_nearby = []

# login cookies
cookies_file = 'cookies.txt'
service = Service(cookies_file=cookies_file, authenticating_account=google_email)

# loading saved_locations format: FullName,LocationName,Latitude,Longitude
if os.path.isfile("saved_locations.txt"):
    with open("saved_locations.txt", "r") as location_text:
        location_data = location_text.read().splitlines()

saved_locations = []
for data in location_data:
    user = data.split(",")
    tempuser = service.get_person_by_full_name(user[0])
    if tempuser is not None:
        saved_locations.append(UserLocation(tempuser, user[1],
                                            float(user[2]), float(user[3])))


def distance_km(lat1, lon1, lat2, lon2):
    p = pi / 180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    # radius of earth * 2 is that magic num
    return 12742 * asin(sqrt(a))


def ping_mail(user, password, mes):
    sent_from = user
    to = [user, user]
    subject = "GoogleNearby"

    email_text = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (sent_from, ", ".join(to), subject, mes)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(user, password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')


def nearby():
    message = ""
    for person in service.get_all_people():
        if person.full_name != google_email:
            d = distance_km(service.get_coordinates_by_full_name(google_email)[0],
                            service.get_coordinates_by_full_name(google_email)[1],
                            person.latitude, person.longitude)
            # if distance is less or equal to 300 meters
            if d <= 0.3 and person.full_name not in black_listed_nearby:
                message += str(person.full_name) + " is " + str(round(d * 1000, 2)) + " meters away\n"
                black_listed_nearby.append(person.full_name)
            elif d > 0.3 and person.full_name in black_listed_nearby:
                message += str(person.full_name) + " is no longer nearby\n"
                black_listed_nearby.remove(person.full_name)
    return message


def at_location_check():
    message = ""
    # refresh saved location
    for data_temp in location_data:
        userdata = data_temp.split(",")
        tempuser = service.get_person_by_full_name(userdata[0])
        if tempuser is not None:
            for i in range(len(saved_locations)):
                # find the correct saved location by comparing fullname, place name, latitude and longitude
                if saved_locations[i].person.full_name == tempuser.full_name and \
                        saved_locations[i].place["name"] == userdata[1] and \
                        saved_locations[i].place["latitude"] == float(userdata[2]) and \
                        saved_locations[i].place["longitude"] == float(userdata[3]):
                    # update the persons location
                    saved_locations[i].person = tempuser

    # check if they are at location with their new updated location
    for personExtended in saved_locations:
        d = distance_km(personExtended.place["latitude"],
                        personExtended.place["longitude"],
                        personExtended.person.latitude, personExtended.person.longitude)
        # if person was not at the location but just arrived
        if d <= 0.15 and personExtended.place['at_location'] is False:
            personExtended.place['at_location'] = True
            message += personExtended.person.full_name + " has arrived at " + personExtended.place["name"] + "\n"
        # if person is away from the location but was just there
        elif d > 0.15 and personExtended.place['at_location'] is True:
            personExtended.place['at_location'] = False
            message += personExtended.person.full_name + " just left " + personExtended.place["name"] + "\n"
    return message


def run():
    while True:
        # refresh google maps
        service = Service(cookies_file=cookies_file, authenticating_account=google_email)
        message = ""
        if service is not None:
            message += nearby()
            message += at_location_check()
        if message != "":
            ping_mail(google_email, mail_password, message)
            print(message)
        # checks every minute
        time.sleep(60)
