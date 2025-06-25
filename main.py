from flask import Flask
from threading import Thread
import requests
import feedparser
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask('')


@app.route('/')
def home():
    return "Agent is awake!"


@app.route('/run-agent')
def run_agent():
    now = datetime.now()
    if now.hour == 9:  # only run at 9 AM server time
        try:
            # 1. Get Google News RSS Feed
            rss_url = "https://news.google.com/rss/search?q=ai+marketing&hl=en-IN&gl=IN&ceid=IN:en"
            feed = feedparser.parse(rss_url)
            top_story = feed.entries[0].title

            # 2. Google Sheets API
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                "creds.json", scope)
            client = gspread.authorize(creds)

            # 3. Write to sheet
            sheet = client.open("AI Trends").sheet1
            sheet.update_cell(2, 1, top_story)

            return f"✅ Posted: {top_story}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    return "⏰ Not time yet."


def run():
    app.run(host='0.0.0.0', port=8080)


Thread(target=run).start()
