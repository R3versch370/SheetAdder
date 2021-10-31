from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import discord
from google.oauth2 import service_account
import datetime
import re
from dotenv import load_dotenv
from discord.ext import commands
from gtts import gTTS
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
from discord.utils import get

client = discord.Client()

#bot = commands.Bot(command_prefix="$")

project_folder = os.path.expanduser('~/')

load_dotenv(os.path.join(project_folder,'.env'))

TOKEN = os.getenv("DISCORD_BOT_SECRET")

TOKEN_FILE = os.path.join(project_folder, 'token.json')

DOCUMENT_ID = os.getenv("DOCUMENT_ID")


user_id = {}

playlist = []

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

value_render_option = 'FORMATTED_VALUE'

results = []
results.append({
            "updateCells": {
            "rows": [
                {
                    "values": [{
                                   "userEnteredFormat": {
                                       "backgroundColor": {
                                           "red": 0,
                                           "green": 1,
                                           "blue": 0,
                                           "alpha": 1
                                       }}}
                    ]
                }
            ],
            "fields": 'userEnteredFormat.backgroundColor',
            "range": {
                "sheetId": 0,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 0,
                "endColumnIndex": 1
            }
            }})

def update_doc_with_guess(date, number, colour, user, officialFlag):

    credentials =service_account.Credentials.from_service_account_file(TOKEN_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    data = service.spreadsheets().values().get(spreadsheetId=DOCUMENT_ID, range="A:A", majorDimension="ROWS").execute()
    if not officialFlag:
        range_row = find_row_number(data, date, user)
        if range_row is None:
            return None
        document = service.spreadsheets().values().update(spreadsheetId=DOCUMENT_ID, range=range_row, valueInputOption="USER_ENTERED",body={"values":[[int(number)],[colour]], "majorDimension": "COLUMNS"}).execute()
    else:
        dateRow = find_row_number(data, date, "official")
        range_row = f"C{dateRow}:D{dateRow}"
        document = service.spreadsheets().values().update(spreadsheetId=DOCUMENT_ID, range=range_row, valueInputOption="USER_ENTERED",body={"values":[[int(number)],[colour]], "majorDimension": "COLUMNS"}).execute()
        find_cells_to_highlight(number, colour, dateRow, service)
    return "Success"

@client.event
async def on_ready():

    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):

    if message.content.startswith('Hello Bot'):

        await message.channel.send(f'Hello <@{message.author.id}>!')
	if message.content.startswith('!glady'):

        date = datetime.datetime.utcnow()
        if date.hour >= 1:
            date = datetime.datetime.now() + datetime.timedelta(days=1)
        print(date)
        guess = message.content.split(" ",1)
        number, colour = guess[1].split(" ", 1)
        number = re.sub(r"[^0-9 ]+", "", number)
        colour = re.sub(r"[^A-Za-z ]+", "", colour)

        user = message.author
        response = update_doc_with_guess(date, number, colour, user, False)
        if response is None:
            await message.channel.send(f"Failed to send guess")
        else:
            await message.channel.send(f"Sent case guesses {number} {colour} to excel")

    elif message.content.startswith('!official'):

        date = datetime.datetime.utcnow()
        if date.hour < 1:
            date = datetime.datetime.now() - datetime.timedelta(days=1)

        guess = message.content.split(" ",1)
        number, colour = guess[1].split(" ", 1)
        number = re.sub(r"[^0-9 ]+", "", number)
        colour = re.sub(r"[^A-Za-z ]+", "", colour)

        update_doc_with_guess(date, number, colour, None, True)

        await message.channel.send(f"Updated official data")
