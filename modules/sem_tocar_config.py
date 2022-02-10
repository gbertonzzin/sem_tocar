"""Config file for the app, contains paths, variables and so such
PT:Arquivo de config do APP, contém paths, variáveis, e afins
"""
import os

#Google user (e-mail or ID)
USER_ID = "centro.vitalis.jau@gmail.com"

#Self-explanatory
COMPANY_NAME = "Centro Vitallis"

#Self-explanatory
CONTACT_PHONE = "(14)981605496"

#How many days into the future the event request gets
DAYS_TO_REQUEST = 30

#How frequently the routine requests shall be performed, IN SECONDS
ROUTINE_FREQ = 60

#Save webcam image when QR code is shown?
SAVE_WEBCAM = False

#TODO: Keep logs regarding QR codes on entrance?
WEBCAM_QR_LOGS = False

#Time tolerance for entrance, in minutes
TOLERANCE = 15

#Google credentials file
GOOGLE_CREDS = os.getenv('GOOGLE_API_CREDENTIALS')

#Print invitation if there are no guests in a new event?
PRINT_INVITE = False

#GPIO pins
RELAY_PIN = 40

RED_LED_PIN = 29

GREEN_LED_PIN = 35

BLUE_LED_PIN = 31

BUZZER_PIN = 33

#Current timezone, according to pendulum.timezones list
TIMEZONE = 'Brazil/East'

#How many seconds shall the relay remain open
OPEN_DOOR = 3

#Use encryption? Encryption demands big QR codes which are not very readable
ENCRYPTION = False

#Filler in case the calendar and event IDs are not same lenght. Unused.
CRYPTO_FILLER = ""