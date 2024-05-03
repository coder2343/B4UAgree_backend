import json
from flask import Flask, request
from privacysummarizer import html_to_summary
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


PrivacyPolicy= []

# function gets privacy policy
@app.route('/sendpolicy', methods=['POST'])
def get_privacy_policy():
  request_data = request.get_json()
  retrivedPolicy= request_data['privacyPolicy']
  PrivacyPolicy.append(retrivedPolicy)
  print("append_privacyPolicy")
  return PrivacyPolicy

# get request 
# LIAM'S REQUEST 05/02/2024
# @app.route('/sum', methods=['GET'])
# def send_summary():
#   print("request headers")
#   privacyPolicy= request.headers.get('privacyPolicy')
#   make_sum = html_to_summary(privacyPolicy)
#   print("return privacy policy sum")
#   return json.dumps(make_sum)

# get request 
# needed to add a post for local server or it was rejected
@app.route('/sum', methods=['POST','GET'])
def send_summary():
  request_data = request.get_json()
  retrivedPolicy= request_data['privacyPolicy']
  make_sum = html_to_summary(retrivedPolicy)
  return json.dumps(make_sum)



if __name__ == '__main__':
  app.run(port=5000)