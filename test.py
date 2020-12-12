from dotenv import load_dotenv
import os
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

print(f'Client ID: {CLIENT_ID}, Client Secret: {CLIENT_SECRET}')