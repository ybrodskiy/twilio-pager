import os
import sys
from flask import Flask
from flask import Response
from flask import render_template
from twilio.rest import TwilioRestClient
import twilio.twiml
import praw
import csv

app = Flask(__name__)

app_url = "http://tcb-notification.herokuapp.com"
#app_url = "http://localhost:5000"

def get_notification_list():
    with open('./notification_list.csv') as f:
        reader = csv.reader(f)
        return list(reader)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/make_call')
def make_call():
    account_sid = os.environ['ACCOUNT_SID']
    auth_token = os.environ['AUTH_TOKEN']
    client = TwilioRestClient(account_sid, auth_token)

    for contact in get_notification_list():
        client = TwilioRestClient(account_sid, auth_token)
        call = client.calls.create(
            to=contact[1],
            from_= os.environ['ACCOUNT_SID'],
            url=app_url+"/message?name=" + contact[0])
        send_sms(contact[0],contact[1])

    return "Call in progress to:" + contact[0]

@app.route('/message', methods=['GET','POST'])
def message():
    reload(sys)
    #sys.setdefaultencoding('utf8')
    #r = praw.Reddit(user_agent='web_caller_zeke')
    #titles = r.get_front_page(limit=1)
    contact_name = request.form.get('name', None)
    resp = twilio.twiml.Response()
    resp.say("Hey "+contact_name+". How is it going?.\
    This is just a test. But soon it will wake you up if there is a site issue.")
    
    #for x in titles:
    #  resp.say(str(x.title))
    
    resp.say("Cheers!")

    return Response(str(resp), mimetype='text/xml')

def send_sms(name,number):
    account_sid = os.environ['ACCOUNT_SID']
    auth_token = os.environ['AUTH_TOKEN']
    client = TwilioRestClient(account_sid, auth_token)

    client.messages.create(
        to=number,
        from_= os.environ['ACCOUNT_SID'],
        body=name + " TCB in progres.\nPlease join 408-555-1212"
        )

if __name__ == "__main__":
   app.run(debug=True)
