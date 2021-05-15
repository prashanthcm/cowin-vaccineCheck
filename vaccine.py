import requests
from datetime import datetime, timedelta
import smtplib
import ssl
import time
import sys

# python3 vaccine.py 560001 1800
#560001 pincode and 1800 seconds
# smtplib, ssl and requests modules are required

context = ssl.create_default_context()
port = 465

sender = "abc@xyz.com" #email id for sender account
password = "*****" # email password here
receiver = ["abc@gmail.com", "xyz@gmail.com"] # receiver's email



def sendit(message):

        # Login via STMP and send email

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, password)
            for address in receiver:
                server.sendmail(sender, address, message)


pincode = sys.argv[1] if len(sys.argv) > 1 else "560001" # default pin code or can pass in cmd line args
date = datetime.today()


subject = "Covid Vaccine Appointment Available! in Pincode " + str(pincode)


url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin" #API end point for fetching data
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

ls = ""

while True:
    try:
        for i in range(1,8): # runs to check for 7 days
            payload = {'pincode': pincode, 'date': (date + timedelta(days=i)).strftime('%d-%m-%Y')} #needed pincode and date to check for
            get_req = requests.get(url, headers=headers, params=payload)
            data = get_req.json()['sessions'] # data is stored in 'sessions' key
            # sendit()
            # print(data)
            for centre in data:
                text = "Date:" + centre['date'] + " center:"+ centre['name'] + " type:" + centre['vaccine'] + " available:" + str(centre['available_capacity']) + " Minimum age limit: " + str(centre['min_age_limit'])
                # print(text)
                ls += text
                ls += '\n'
        if len(ls) > 0:
            message = 'Subject: {}\n\n{}'.format(subject, ls)
            sendit(message) #send email if there is any data in json
            break
        print("no data")
        time.sleep(int(sys.argv[2]) if len(sys.argv) > 2 else 1800) # default is 30 mins, we can set via cmd line args
    except:
        print("Something went wrong, rerunning the script")
