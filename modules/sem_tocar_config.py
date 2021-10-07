"""Config file for the app, contains paths, variables and so such
PT:Arquivo de config do APP, contém paths, variáveis, e afins
"""
#Self-explanatory
COMPANY_NAME = "Batata Baroa S/A"

#Self-explanatory
CONTACT_PHONE = "666 um tapa na oreia"

#How many days into the future the event request gets
DAYS_TO_REQUEST = 30

#Google user (e-mail or ID)
USER_ID = "gbertonzzin@gmail.com"

#How frequently the routine requests shall be performed, IN SECONDS
ROUTINE_FREQ = 30

#Save webcam image when QR code is shown?
SAVE_WEBCAM = True

#TODO: Keep logs regarding QR codes on entrance?
WEBCAM_QR_LOGS = True

#Time tolerance for entrance
TOLERANCE = 0

#Filler in case the calendar and event IDs are not same lenght. Unused.
CRYPTO_FILLER = ""

#Google credentials file
GOOGLE_CREDS = "credentials.json"

#Print invitation if there are no guests in a new event?
PRINT_INVITE = False

#GPIO pin for the door magnet lock relay
RELAY_PIN = 8

#Current timezone, according to pendulum.timezones list
TIMEZONE = 'Brazil/East'

#How many seconds shall the door remain open
OPEN_DOOR = 3