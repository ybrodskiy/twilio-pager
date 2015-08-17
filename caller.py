import os
import sys
from flask import Flask, jsonify,Response,render_template
from flask_oauth2_login import GoogleLogin
from twilio.rest import TwilioRestClient
import twilio.twiml
import praw
import csv
import requests


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

app.config.update(
  SECRET_KEY="secret",
  GOOGLE_LOGIN_REDIRECT_SCHEME="http",
)

# move to config
app_url = "http://tcb.mypaaspoc.net:8080"
allowed_users = {"ybrodskiy@gmaili.com"}
#app_url = "http://localhost:5000"
google_login = GoogleLogin(app)

def get_notification_list():
    with open('./notification_list.csv') as f:
        reader = csv.reader(f)
        return list(reader)

@google_login.login_success
def login_success(token, profile):
  if profile['email'] in allowed_users:
    return jsonify(token=token, profile=profile)
  else:
    requests.get('https://accounts.google.com/o/oauth2/revoke?token='+token['access_token'])
    return """
<html>
<h1>Invalid user</h1>
<INPUT TYPE="button" VALUE="Back" onClick="history.go(-1);">
</html>
"""

@google_login.login_failure
def login_failure(e):
  return jsonify(error=str(e))

@app.route('/')
def index():
  return """
<html>
<a href="{}">Login with Google</a>
""".format(google_login.authorization_url())

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
