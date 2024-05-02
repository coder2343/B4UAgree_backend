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

# get request 
@app.route('/sum', methods=['GET'])
def send_summary():
  print("request headers")
  privacyPolicy= request.headers.get('privacyPolicy')
  make_sum = html_to_summary(privacyPolicy)
  print("return privacy policy sum")
  return json.dumps(make_sum)

if __name__ == '__main__':
  app.run(port=5000)