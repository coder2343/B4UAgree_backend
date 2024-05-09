"""Module providing a function for sumerizing and bs4 is for webscrapeing."""
from summarizer.sbert import SBertSummarizer
from bs4 import BeautifulSoup, NavigableString, Tag
import os 
import re
import json
import requests
from privacy_policy_score.ppe import evaluate 
from term_identification import assign_paragraph_to_topic, topics_keywords, calculate_importance


# compute summary from SBertSummarizer
def get_summary(text,num_sentences):
    """Function take text file and outputs given sumary of said text useing nlp model."""
    model = SBertSummarizer('paraphrase-MiniLM-L6-v2')
    result = model(text, num_sentences=num_sentences)
    #update_html(result)
    return result


# function that is our powerhouse. retrieves html web page and returns the headings and summaries paired in JSON.
def html_to_summary(url):
    # we store everything in a dictionary
    my_dict = {
        "PrivacyPolicyScore" : 0,
        "topics_summary": {},
        "headings_summary": {}
    }

    # grabbing webpage content
    page = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                                       'referer': 'https://google.com'})
    
    # beginning parsing with BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")
    f = open("privPolicy.txt", "w")
    f.write(soup.text)
    f.close()
    privacyScore= evaluate('privPolicy.txt')
    print(privacyScore)
    my_dict["PrivacyPolicyScore"] =privacyScore
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

        # Score each section based on term identification and importance assessment
        section_score = calculate_importance(curr_paragraphs)

        # Assign the section to a topic based on its topic-relevant score
        assigned_topic = assign_paragraph_to_topic(curr_paragraphs, topics_keywords)

        # Check if the section score is above a certain threshold
        if section_score >= 7:  
            # If the score is high, summarize the section with more detail
            curr_summary = get_summary(curr_paragraphs, 2)  
        else:
            # If the score is low, summarize the section more concisely
            curr_summary = get_summary(curr_paragraphs, 1)  

        # Store summary by topic
        # Check if the assigned_topic already exists in my_dict
        if assigned_topic not in my_dict["topics_summary"]:
            my_dict["topics_summary"][assigned_topic] = curr_summary  # Create a new entry
        else:
            my_dict["topics_summary"][assigned_topic] += curr_summary  # Append to existing entry

        # Store summary by heading
        my_dict["headings_summary"][header.get_text()] = curr_summary

    # Sort the dictionary by keys, placing 'Other' last
    sorted_topics_summary = {k: my_dict["topics_summary"][k] for k in sorted(my_dict["topics_summary"].keys(), key=lambda x: (x == 'Other', x))}
    my_dict["topics_summary"] = sorted_topics_summary

    print(json.dumps(my_dict, indent = 4))
    return my_dict
              
#html_to_summary()
