import os
import pickle

if not os.path.isfile("email.dat"):
    google_email = input("Enter email that's linked to cookies: ")
    pickle.dump(google_email, open("email.dat", "wb"))

if not os.path.isfile("mail_password.dat"):
    mail_password = input("Email's password (if using gmail, generate App Password): ")
    pickle.dump(mail_password, open("mail_password.dat", "wb"))

if not os.path.isfile("saved_locations.txt"):
    f = open("saved_locations.txt", "w")
    f.close()
