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

# login to google maps
cookies_file = 'cookies.txt'
service = Service(cookies_file=cookies_file, authenticating_account=google_email)

# loading saved_locations format: FullName,LocationName,Latitude,Longitude
saved_locations = []
if os.path.isfile("saved_locations.txt"):
    with open ("saved_locations.txt", "r") as location_text:
        location_data = location_text.read().splitlines()
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
            # if distance is less or equal to 150 meters
            if d <= 0.15:
                message += str(person.full_name) + " is " + str(round(d * 1000, 2)) + " meters away\n"
    if message == "":
        print("No One is Nearby")
    return message


def at_location_check():
    message = ""
    for personExtended in saved_locations:
        d = distance_km(personExtended.place["latitude"],
                        personExtended.place["longitude"],
                        personExtended.person.latitude, personExtended.person.longitude)
        # if person was not at the location but just arrived
        if d <= 0.15 and not personExtended.place['at_location']:
            personExtended.place['at_location'] = True
            message += personExtended.person.full_name + " has arrived at " + personExtended.place["name"] + "\n"
        # if person is away from the location but was just there
        elif d > 0.15 and personExtended.place['at_location']:
            personExtended.place['at_location'] = False
            message += personExtended.person.full_name + " just left " + personExtended.place["name"] + "\n"
    return message


def run():
    while True:
        message = ""
        message += nearby()
        message += at_location_check()
        if message != "":
            ping_mail(google_email, mail_password, message)
            print(message)
        # checks once a minute
        time.sleep(60)
