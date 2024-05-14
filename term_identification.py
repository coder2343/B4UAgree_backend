import re
import json
import os

# Define fixed topics and their associated keywords
# Keywords are assigned weight according to how unique they are to their respective topic
topics_keywords = {
    "data collection and usage": {
        "personal information": 3, "data categories": 4, "collection methods": 3,
        "purpose of collection": 3, "consent": 1, "cookies": 1, "tracking technologies": 2,
        "user activity": 3, "location data": 4, "device information": 4,
        "analytics": 3, "profile creation": 3, "communication preferences": 3,
        "account registration": 4, "surveys and feedback": 4, "social media integration": 4,
        "third-party data sources": 5, "data retention": 4, "data deletion": 3, "data aggregation": 3,
        "data analysis": 4, "user behavior": 4, "data utilization": 4, "information gathering": 4,
        "data storage": 3, "data processing": 3, "data tracking": 3, "data usage policies": 2
    },
    "data sharing and disclosure": {
        "third parties": 5, "sharing practices": 4, "partnerships": 4,
        "advertising networks": 4, "service providers": 4, "legal requirements": 4,
        "consent agreements": 3, "affiliate programs": 3, "data transfers": 3,
        "data sales": 3, "data anonymization": 2, "data pseudonymization": 2,
        "data licensing": 3, "business transactions": 4, "merger or acquisition": 4,
        "publicly available information": 4, "aggregated data": 4,
        "cross-border transfers": 5, "data processing agreements": 4, "data breach response": 4,
        "information exchange": 4, "data dissemination": 3, "data distribution": 5,
        "sharing protocols": 5, "data disclosure": 5, "data access": 3, "data transmission": 3
    },
    "data security measures": {
        "encryption": 5, "secure protocols": 5, "access controls": 4,
        "authentication methods": 3, "firewall protection": 3, "intrusion detection": 5,
        "security audits": 5, "vulnerability assessments": 5, "data encryption in transit": 5,
        "data encryption at rest": 3, "secure storage": 5, "incident response plan": 5,
        "data minimization": 2, "data masking": 2, "two-factor authentication": 4,
        "secure sockets layer (ssl)": 2, "transport layer security (tls)": 2,
        "security certifications": 5, "compliance standards": 5, "security training and awareness": 5,
        "data integrity": 4, "data protection": 4, "data confidentiality": 4,
        "data security protocols": 5, "data safeguarding": 5, "data hygiene": 5, "security measures": 3
    },
    "user rights and controls": {
        "access rights": 5, "rectification": 4, "data portability": 4,
        "data deletion": 5, "consent withdrawal": 3, "opt-out mechanisms": 3,
        "privacy settings": 5, "cookie preferences": 5, "marketing preferences": 5,
        "account management": 3, "privacy dashboard": 3, "privacy policies review": 5,
        "user profiles": 3, "account deletion": 5, "data export": 3,
        "data correction": 3, "data restriction": 3, "data erasure": 3,
        "data retention policies": 3, "user support channels": 3,
        "data ownership": 2, "user consent": 2, "user preferences": 2,
        "user privacy rights": 2, "user control": 2, "user data management": 2,
        "user data access": 2, "children's data": 5, "parental consent": 5,
        "coppa compliance": 5, "children's privacy rights": 5, "child data protection": 5,
        "child account management": 3, "child data deletion": 3, "child data access": 3, "children": 3,
        "parental controls": 5, "age verification": 3, "age-appropriate content": 4,
        "child online safety": 5, "child data collection": 5,
        "opt-out option": 4, "opt-out preferences": 4, "opt-out requests": 4, "opt-out": 4,
        "right to": 5, "upon your request": 5
    },
    "policy updates and notifications": {
        "policy changes": 5, "updates": 4, "modifications": 4,
        "notification methods": 3, "email notifications": 3, "website banners": 3,
        "privacy alerts": 3, "opt-in notifications": 3, "opt-out notifications": 3,
        "consent reminders": 3, "revision history": 3, "version control": 3,
        "review frequency": 3, "compliance updates": 3, "legal changes": 3,
        "data protection laws": 2, "privacy regulations": 2, "transparency reports": 2,
        "user communication": 2, "notification preferences": 2,
        "policy amendments": 2, "policy revisions": 2, "policy alerts": 2,
        "policy compliance": 2, "policy notifications": 2, "policy review": 2,
        "policy transparency": 2, "feedback": 5, "concerns": 5, "suggestions": 5,
        "user feedback": 5, "inquiries": 3, "complaints": 4,
        "support": 3, "assistance": 3, "help": 1,
        "customer service": 5, "user satisfaction": 3, "user experience": 1,
        "user engagement": 2,
    }
}



# Assign a paragraph to a topic based on the number of matching keywords.
def assign_paragraph_to_topic(paragraph, topics_keywords):
    
    max_score = 0
    assigned_topic = "Other"  # Default to "Other" if no specific topic is identified

    # Iterate through each topic and its associated keywords
    for topic, keywords_weights in topics_keywords.items():
        score = 0
        # Count the number of matching keywords in the paragraph
        for keyword, weight in keywords_weights.items():
            if keyword in paragraph.lower():
                score += weight
        # Update the assigned topic if the current topic has more matching keywords
        if score > max_score:
            max_score = score
            assigned_topic = topic

    return assigned_topic

# Calculate the importance score of a paragraph based on the average score of its words,
# using the same scoring system as the privacy_evaluator
def calculate_importance(paragraph):
    
    # Read privacy policy settings from 'settings.json'
    with open(os.path.join(os.path.dirname(__file__), 'privacy_policy_score/privacy_policy_evaluator/data/settings.json')) as json_file:
        privacy_policy_settings = json.load(json_file)

    # Initialize variables to store accumulated score and word count
    total_score = 0
    total_words = 0

    # Iterate through each privacy policy category
    for category in privacy_policy_settings['settings']['data']:
        # Retrieve the value assigned to the category
        category_value = privacy_policy_settings['settings']['data'][category]['value']

        # Iterate through words in the category
        for word in privacy_policy_settings['settings']['data'][category]['words']:
            # Check if the word exists in the paragraph
            if word in paragraph:
                # Accumulate the value assigned to the word
                total_score += category_value
                total_words += 1

    # Calculate the average score
    if total_words > 0:
        average_score = total_score / total_words
    else:
        average_score = 0

    return average_score