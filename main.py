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

@client.event
async def on_ready():

    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):

    if message.content.startswith('Hello Bot'):

        await message.channel.send(f'Hello <@{message.author.id}>!')

