import re
import json
import os

# Define fixed topics and their associated keywords
topics_keywords = {
    "Data Collection and Usage": [
        "personal information", "data categories", "collection methods",
        "purpose of collection", "consent", "cookies", "tracking technologies",
        "user activity", "location data", "device information",
        "analytics", "profile creation", "communication preferences",
        "account registration", "surveys and feedback", "social media integration",
        "third-party data sources", "data retention", "data deletion", "data aggregation",
        "data analysis", "user behavior", "data utilization", "information gathering",
        "data storage", "data processing", "data tracking", "data usage policies"
    ],
    "Data Sharing and Disclosure": [
        "third parties", "sharing practices", "partnerships",
        "advertising networks", "service providers", "legal requirements",
        "consent agreements", "affiliate programs", "data transfers",
        "data sales", "data anonymization", "data pseudonymization",
        "data licensing", "business transactions", "merger or acquisition",
        "publicly available information", "aggregated data",
        "cross-border transfers", "data processing agreements", "data breach response",
        "information exchange", "data dissemination", "data distribution",
        "sharing protocols", "data disclosure", "data access", "data transmission"
    ],
    "Data Security Measures": [
        "encryption", "secure protocols", "access controls",
        "authentication methods", "firewall protection", "intrusion detection",
        "security audits", "vulnerability assessments", "data encryption in transit",
        "data encryption at rest", "secure storage", "incident response plan",
        "data minimization", "data masking", "two-factor authentication",
        "secure sockets layer (ssl)", "transport layer security (tls)",
        "security certifications", "compliance standards", "security training and awareness",
        "data integrity", "data protection", "data confidentiality",
        "data security protocols", "data safeguarding", "data hygiene", "security measures"
    ],
    "User Rights and Controls": [
        "access rights", "rectification", "data portability",
        "data deletion", "consent withdrawal", "opt-out mechanisms",
        "privacy settings", "cookie preferences", "marketing preferences",
        "account management", "privacy dashboard", "privacy policies review",
        "user profiles", "account deletion", "data export",
        "data correction", "data restriction", "data erasure",
        "data retention policies", "user support channels",
        "data ownership", "user consent", "user preferences",
        "user privacy rights", "user control", "user data management",
        "user data access", "children's data", "parental consent",
        "coppa compliance", "children's privacy rights", "child data protection",
        "child account management", "child data deletion", "child data access",
        "child", "children", "child data",
        "parental controls", "age verification", "age-appropriate content",
        "child online safety", "child data collection", "aware"
    ],
    "Policy Updates and Notifications": [
        "policy changes", "updates", "modifications",
        "notification methods", "email notifications", "website banners",
        "privacy alerts", "opt-in notifications", "opt-out notifications",
        "consent reminders", "revision history", "version control",
        "review frequency", "compliance updates", "legal changes",
        "data protection laws", "privacy regulations", "transparency reports",
        "communication", "notification preferences",
        "policy amendments", "policy revisions", "policy alerts",
        "policy compliance", "policy notifications", "policy review",
        "policy transparency",
        "opt-out option", "opt-out preferences", "opt-out requests", 
        "feedback", "concerns", "suggestions",
        "feedback", "inquiries", "complaints",
        "user support", "assistance", "help",
        "customer service", "user satisfaction", "experience",
        "engagement"
    ]
}


# Assign a paragraph to a topic based on the number of matching keywords.
def assign_paragraph_to_topic(paragraph, topics_keywords):
    
    max_match_count = 0
    assigned_topic = "Other"  # Default to "Other" if no specific topic is identified

    # Iterate through each topic and its associated keywords
    for topic, keywords in topics_keywords.items():
        match_count = 0
        # Count the number of matching keywords in the paragraph
        for keyword in keywords:
            if keyword in paragraph.lower():
                match_count += 1
        # Update the assigned topic if the current topic has more matching keywords
        if match_count > max_match_count:
            max_match_count = match_count
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