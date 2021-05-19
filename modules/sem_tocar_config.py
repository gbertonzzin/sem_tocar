"""Config file for the app, contains paths, variables and so such
PT:Arquivo de config do APP, contém paths, variáveis, e afins
"""
#How many days into the future the event request gets
DAYS_TO_REQUEST = 30

#Google user (e-mail or ID)
USER_ID = "gbertonzzin@gmail.com"

#How frequently the routine requests shall be performed
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