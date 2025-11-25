#!/usr/bin/env python3
"""
Gmail API Authorization Script
Run this ONCE locally to generate token.json
"""
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authorize_gmail():
    """Authorize Gmail API and save token"""
    creds = None
    
    # Check if we already have a token
    if os.path.exists('token.json'):
        print("⚠️  token.json already exists!")
        overwrite = input("Do you want to create a new token? (yes/no): ")
        if overwrite.lower() != 'yes':
            print("❌ Aborted")
            return
    
    # Check for credentials file
    cred_file = 'client_secret_706742278115-u9q2omvnuj971ch42k93e9bc4e8m7oio.apps.googleusercontent.com.json'
    if not os.path.exists(cred_file):
        print(f"❌ Credentials file not found: {cred_file}")
        print("Please make sure the OAuth credentials JSON file is in the backend directory")
        return
    
    print("🔐 Starting OAuth flow...")
    print("📱 Your browser will open. Please authorize the application.")
    
    flow = InstalledAppFlow.from_client_secrets_file(cred_file, SCOPES)
    creds = flow.run_local_server(port=8080)
    
    # Save the credentials
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    
    print("\n✅ Authorization successful!")
    print("📄 token.json has been created")
    print("\n📋 Next steps:")
    print("1. Copy the content of token.json")
    print("2. In Render dashboard, add environment variable:")
    print("   Name: GMAIL_TOKEN")
    print("   Value: <paste the entire content of token.json>")
    print("\n3. Also make sure EMAIL_SENDER is set to your Gmail address")
    print("\n4. Redeploy your app on Render")
    
    # Display token content for easy copying
    print("\n" + "="*60)
    print("TOKEN CONTENT (copy this):")
    print("="*60)
    with open('token.json', 'r') as f:
        print(f.read())
    print("="*60)

if __name__ == '__main__':
    authorize_gmail()
