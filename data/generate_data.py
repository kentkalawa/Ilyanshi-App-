import pandas as pd
import random

# Sample complaint templates
subjects = {
    "Claim": [
        "My claim was rejected without proper explanation",
        "The claim process is taking too long",
        "I submitted my claim three weeks ago and no response",
        "My claim was denied unfairly",
        "The claim amount paid was less than expected"
    ],
    "Payment": [
        "My payment is delayed by two weeks",
        "I have not received my payout",
        "The payment amount is incorrect",
        "Payment was made to the wrong account",
        "I am still waiting for my refund"
    ],
    "Policy": [
        "The policy terms are unclear",
        "I was not informed about the exclusions",
        "The policy was cancelled without notice",
        "I need to change my policy details",
        "The policy renewal process is confusing"
    ],
    "Premium": [
        "My premium increased without explanation",
        "The premium amount is too high",
        "I was charged twice for the same month",
        "Premium deduction was incorrect",
        "I need to update my payment method"
    ],
    "Service": [
        "Customer service is very poor",
        "No one responds to my emails",
        "The call centre keeps transferring me",
        "Staff were rude and unhelpful",
        "I have been waiting for a response for days"
    ]
}

urgencies = ["High", "Medium", "Low"]
sentiments = ["Negative", "Neutral", "Positive"]

# Generate 500 complaints
data = []
for _ in range(500):
    subject = random.choice(list(subjects.keys()))
    text = random.choice(subjects[subject])
    
    # Add urgency based on subject
    if subject in ["Claim", "Payment"]:
        urgency = random.choice(["High", "High", "Medium"])
    elif subject in ["Policy", "Premium"]:
        urgency = random.choice(["Medium", "Medium", "Low"])
    else:
        urgency = random.choice(["Low", "Medium", "High"])
    
    # Add sentiment based on text
    if any(word in text.lower() for word in ["rejected", "delayed", "poor", "rude", "unfair", "wrong", "incorrect"]):
        sentiment = "Negative"
    elif any(word in text.lower() for word in ["confusing", "unclear", "waiting"]):
        sentiment = "Neutral"
    else:
        sentiment = random.choice(sentiments)
    
    data.append({
        "complaint_text": text,
        "subject": subject,
        "urgency": urgency,
        "sentiment": sentiment
    })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("complaints.csv", index=False)
print(f"✅ Generated {len(df)} complaints")
print(f"Saved to complaints.csv")
print(df.head())