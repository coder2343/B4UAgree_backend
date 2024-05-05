from privacysummarizer import html_to_summary
from bs4 import BeautifulSoup, NavigableString, Tag
import os 
import re
import json
import requests
from privacy_policy_score.ppe import evaluate 
#print(html_to_summary("https://www.grinnell.edu/policies/privacy"))


my_dict = {}
# grabbing webpage content
page = requests.get('https://www.amazon.com/gp/help/customer/display.html?nodeId=GX7NJQ4ZB8MHFRNJ&ref_=footer_privacy', headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                                'referer': 'https://google.com'})                                                                                     
print(page)
# beginning parsing with BeautifulSoup
soup = BeautifulSoup(page.content, "html.parser")
f = open("privPolicy.txt", "w")
f.write(soup.text)
f.close()

privacyScore= evaluate('privPolicy.txt')
print(privacyScore)
my_dict["PrivacyPolicyScore"] =privacyScore
