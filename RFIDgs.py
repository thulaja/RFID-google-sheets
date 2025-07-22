import RPi.GPIO as GPIO
import time
import requests
from mfrc522 import SimpleMFRC522

# Google Sheets Web App URL
WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbzJaQ_lWnu-H29qyAy33UfeMi8rr7s8IgEL0n75i-WRm-ULc3fu5_n-3JtNLHc2gEsy5Q/exec'

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
reader = SimpleMFRC522()

try:
    while True:
        print("Place your card...")
        id, text = reader.read()
        cleaned_text = text.strip().upper()
        print("ID:", id)
        print("Text:", cleaned_text)

        if id == 782698349564 and cleaned_text == 'NIRU':
            team_name = 'CHUK CHUK CHUU'
            access_status = 'Access Granted'
            GPIO.output(40, 1)
        elif id == 456761152055 and cleaned_text == 'JHGF':
            team_name = 'SVAMJPL'
            access_status ='Access Granted'
            GPIO.output(40, 1)
        else:
            team_name = cleaned_text
            access_status = 'Access Denied'
            GPIO.output(40, 0)

        payload = {
            'rfid_id': str(id),
            'team_name': team_name,
            'access_status': access_status
        }

        response = requests.post(WEBHOOK_URL, json=payload)
        print("Sent to Google Sheets:", response.text)

        time.sleep(5)
        GPIO.output(40, 0)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
