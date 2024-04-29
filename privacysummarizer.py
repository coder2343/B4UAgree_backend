"""Module providing a function for sumerizing and bs4 is for webscrapeing."""
from summarizer.sbert import SBertSummarizer
from bs4 import BeautifulSoup, NavigableString, Tag
import os 
import re
import json
import requests

def receive_text(self):
    pass
# --- MIA H - More cleanup should be done. I would like to remove unused functions, but will keep but commented until I have approval from group.

# ---- UNUSED 
# update_html content with created summary
# def update_html(summary): 
#     base = os.path.dirname(os.path.abspath(__file__))
#     html = open(os.path.join(base, "index.html"))
#     soup = BeautifulSoup(html, "html.parser")
#     old_text = soup.find('p', id='content')
#     tag = soup.new_tag("p", id='content')
#     tag.string = summary
#     old_text.replace_with(tag)
#     with open("index.html", "wb") as f_output:
#         f_output.write(soup.prettify("utf-8"))

# ---- UNUSED 
# in the works function from Liam                              
# def html_to_text(html):
#     """Function take html file and extract given text."""
#     f = open("output/privacyPolicy.txt", "a", encoding="utf-8")
#     soup = BeautifulSoup(html, 'html.parser')
#     for header in soup.find_all({'h3','h2','h1'}):
#         next_node = header
#         while True:
#             next_node = next_node.nextSibling
#             if next_node is None:
#                 break
#             if isinstance(next_node,NavigableString ):
#                 print (next_node.strip())
#             if isinstance(next_node, Tag):
#                 if next_node.name == "h2"or next_node.name == "h1" or next_node.name == "h3" :
#                     #print(soup.find(string=nextNode.text.strip()))
#                     break
#                 f.write(next_node.get_text(strip=True).strip())
#     f.close()

# compute summary from SBertSummarizer
def get_summary(text,num_sentences):
    """Function take text file and outputs given sumary of said text useing nlp model."""
    model = SBertSummarizer('paraphrase-MiniLM-L6-v2')
    result = model(text, num_sentences=num_sentences)
    #update_html(result)
    return result

# ---- UNUSED 
# function in the works from Liam 
# def send_summary(result):
#     """Function take summary and saves text file"""
#     f = open("output/summary.txt", "a", encoding="utf-8")
#     f.write(result)
#     f.close()

# function that is our powerhouse. retrieves html web page and returns the headings and summaries paired in JSON.
def html_to_summary(url):
    # we store everything in a dictionary
    my_dict = {}

    # grabbing webpage content
    page = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    
    # beginning parsing with BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    # -- parsing and finding the correct content 

    # regex for all headers
    header_pattern = re.compile('^h[1-6]$')

    # iterate through all headers in webpage
    for header in soup.find_all(header_pattern): 
        # variable holds all paired paragraphs to headers
        curr_paragraphs = ""

        # iterate through the siblings
        for sibling in header.next_siblings:
          
          # hold siblings tag name
          curr_name = sibling.name
          
          # if paragraph, then add them to our curr_paragraphs variable 
          if curr_name == "p":
              curr_paragraphs = curr_paragraphs + sibling.get_text()

          # if header, then break. we found all paired paragraphs 
          elif curr_name != None and header_pattern.match(curr_name): 
              break
          
          # we would like to avoid summarizing any content with embedded links in their paragraphs, which is common in many privacy policies 
          # so if found, then leave that whole section blank
          elif curr_name == "a" or curr_name == "ul": 
              curr_paragraphs = ""
              break
          
          # if not what we're looking for, just keeping go 
          else: 
              continue
          
        # -- moving into creating summaries

        # count the number of sentences 
        sentences_arr = curr_paragraphs.split(".")
        sentences_num = len(sentences_arr)

        # if less than 3 sentences, then no need to summarize
        if sentences_num <= 3: 
            my_dict[header.get_text()] = curr_paragraphs

        # current rule of thumb is to summarize the number of sentences within the section by half
        else: 
           curr_summary = get_summary(curr_paragraphs, round(sentences_num / 2))
           my_dict[header.get_text()] = curr_summary


    print(json.dumps(my_dict, indent = 4))
    return my_dict
              
#html_to_summary()
