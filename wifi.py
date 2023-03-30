import re
import locale
import subprocess

def get_pass():
    loc = locale.getdefaultlocale()
    language = loc[0]
    encoding = loc[1]

    user_profile_en = "All User Profile     : (.*)\r"
    user_profile_de = "Profil fur alle Benutzer : (.*)\r"
    user_profile_ja = "すべてのユーザー プロファイル     : (.*)\r"

    key_content_en = "Key Content            : (.*)\r"
    key_content_de = "Schlusselinhalt            : (.*)\r"
    key_content_ja = "主要なコンテンツ       : (.*)\r"

    if language == "de_DE":
        user_profile = user_profile_de
        key_content = key_content_de
    elif language == "ja_JP":
        user_profile = user_profile_ja
        key_content = key_content_ja
    else:
        user_profile = user_profile_en
        key_content = key_content_en

    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode(encoding)
    profile_names = (re.findall(user_profile, command_output))

    wifi_list = []

    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = {}
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode(encoding)
            password = re.search(key_content, profile_info_pass)
            wifi_profile = {
                "ssid" : name,
                "password" : None if password == None else password[1]
            }
            wifi_list.append(wifi_profile)
    else:
        print("見つからん...(´；ω；｀)")

    return wifi_list

if __name__ == "__main__":
    for l in get_pass():
        print(l)
