from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import re
from twilio.rest import Client

app = Flask(__name__)

# Twilio API Credentials (Replace with your own or store in environment variables)
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

# List of admin phone numbers (replace with your admin number in E.164 format)
ADMIN_NUMBERS = ["+2348138860175"]  # Your admin number

def contains_link(message):
    # Regex to check for links in the message
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.search(url_pattern, message) is not None

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    # Check if the sender is an admin
    if from_number in ADMIN_NUMBERS:
        msg.body(f"Admin message received: {incoming_msg}")
    elif contains_link(incoming_msg):
        msg.body("Your message contained a link and has been deleted.")
    else:
        # Example response logic
        if 'hello' in incoming_msg.lower():
            msg.body('Hello! How can I help you today?')
        elif 'bye' in incoming_msg.lower():
            msg.body('Goodbye! Let me know if you need further assistance.')
        else:
            msg.body("I'm here to help. You can try saying 'hello' or 'bye'.")

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
    

