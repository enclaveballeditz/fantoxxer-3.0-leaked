import sys
import subprocess
def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "--no-warn-script-location", package])
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")
        sys.exit(2)


required = [
    "discord.py==1.7.3",    
    "aiohttp",
    "asyncio",
    "requests",
    "phonenumbers"
]

missing = []

for pkg in required:
    import_name = "discord" if pkg == "discord.py" else pkg
    
    try:
        __import__(import_name)
    except ImportError:
        missing.append(pkg)

if missing:
    for pkg in missing:
        print(f"→ Installing {pkg} ...")
        install(pkg)
    
    print("\n" + "═" * 50)
    print("  Packages installed...")

import os
import json
import time
import sys
import requests
import re
import random
import concurrent.futures
import base64
from datetime import datetime
from typing import Tuple, Optional
import asyncio
import aiohttp
from aiohttp import TCPConnector
from aiohttp.client_exceptions import *
import discord
from discord.ext import commands
import phonenumbers
from phonenumbers import carrier, geocoder, number_type, PhoneNumberType
import socket
import whois
import threading
import logging
import subprocess


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Theme:
    def __init__(self, name, header, accent, success, fail, warning, menu_colors, animation_speed=0.015):
        self.name = name
        self.header = header
        self.accent = accent
        self.success = success
        self.fail = fail
        self.warning = warning
        self.menu_colors = menu_colors
        self.animation_speed = animation_speed

Themes = {
    "classic": Theme("Classic", (140, 80, 220), (180, 140, 255), (100, 220, 100), (255, 80, 80), (255, 180, 80), [(255, 30, 30), (255, 70, 50), (255, 110, 70), (245, 90, 130), (230, 70, 170), (210, 60, 200), (190, 70, 230), (160, 90, 255), (120, 120, 255)], animation_speed=0.02),
    "cyberpunk": Theme("Cyberpunk", (0, 255, 255), (255, 0, 255), (0, 255, 100), (255, 50, 100), (255, 200, 0), [(255, 0, 255), (0, 255, 255), (255, 100, 255), (0, 255, 200), (255, 150, 0), (100, 255, 255), (255, 50, 255), (0, 200, 255), (255, 255, 0)], animation_speed=0.01),
    "blood": Theme("Blood", (180, 20, 20), (255, 60, 60), (200, 200, 200), (255, 40, 40), (255, 150, 0), [(255, 40, 40), (220, 30, 30), (200, 20, 20), (180, 10, 10), (160, 0, 0), (140, 0, 0), (120, 0, 0), (100, 0, 0), (80, 0, 0)], animation_speed=0.03),
    "ice": Theme("Ice", (100, 200, 255), (150, 220, 255), (200, 255, 255), (255, 80, 120), (255, 200, 80), [(100, 200, 255), (120, 210, 255), (140, 220, 255), (160, 230, 255), (180, 240, 255), (200, 250, 255), (220, 255, 255), (240, 255, 255), (255, 255, 255)], animation_speed=0.015),
    "toxic": Theme("Toxic", (0, 255, 100), (100, 255, 0), (200, 255, 100), (255, 50, 100), (255, 180, 0), [(0, 255, 80), (40, 255, 100), (80, 255, 120), (120, 255, 140), (160, 255, 160), (200, 255, 180), (240, 255, 200), (255, 255, 0), (255, 200, 0)], animation_speed=0.012),
    "void": Theme("Void", (80, 0, 150), (120, 0, 200), (180, 80, 255), (255, 60, 100), (255, 150, 0), [(120, 0, 180), (140, 20, 200), (160, 40, 220), (180, 60, 240), (200, 80, 255), (220, 100, 255), (240, 120, 255), (255, 140, 255), (255, 180, 255)], animation_speed=0.025),
    "neon": Theme("Neon", (0, 255, 255), (255, 0, 255), (0, 255, 150), (255, 50, 100), (255, 255, 0), [(0, 255, 255), (255, 0, 255), (0, 255, 200), (255, 100, 255), (0, 200, 255), (255, 255, 100), (100, 255, 255), (255, 50, 255), (0, 255, 100)], animation_speed=0.008),
    "sunset": Theme("Sunset", (255, 150, 80), (255, 100, 150), (255, 200, 100), (200, 50, 100), (255, 180, 0), [(255, 180, 80), (255, 140, 100), (255, 100, 120), (255, 80, 140), (255, 60, 160), (255, 40, 180), (255, 20, 200), (220, 0, 220), (180, 0, 255)], animation_speed=0.018),
    "matrix": Theme("Matrix", (0, 255, 0), (0, 200, 0), (0, 255, 150), (0, 100, 0), (100, 255, 100), [(0, 255, 0), (0, 220, 0), (0, 180, 0), (0, 140, 0), (0, 100, 0), (50, 255, 50), (100, 255, 100), (150, 255, 150), (200, 255, 200)], animation_speed=0.01),
    "pastel": Theme("Pastel", (200, 150, 255), (180, 200, 255), (150, 255, 200), (255, 180, 200), (255, 220, 150), [(200, 150, 255), (180, 170, 255), (160, 190, 255), (140, 210, 255), (120, 230, 255), (150, 255, 220), (180, 255, 200), (210, 255, 180), (240, 255, 160)], animation_speed=0.025),
    "gold": Theme("Gold", (255, 215, 0), (255, 180, 0), (255, 255, 150), (200, 150, 0), (255, 140, 0), [(255, 215, 0), (255, 190, 0), (255, 165, 0), (255, 140, 0), (255, 115, 0), (220, 180, 0), (200, 160, 0), (180, 140, 0), (160, 120, 0)], animation_speed=0.02),
    "forest": Theme("Forest", (34, 139, 34), (0, 100, 0), (50, 205, 50), (139, 69, 19), (107, 142, 35), [(34, 139, 34), (46, 139, 87), (60, 179, 113), (85, 107, 47), (107, 142, 35), (143, 188, 143), (124, 252, 0), (154, 205, 50), (34, 100, 34)], animation_speed=0.022),
    "ocean": Theme("Ocean", (0, 105, 148), (0, 150, 255), (100, 200, 255), (0, 80, 120), (0, 200, 255), [(0, 105, 148), (0, 130, 180), (0, 160, 220), (0, 190, 255), (70, 220, 255), (100, 240, 255), (130, 255, 255), (160, 255, 255), (200, 255, 255)], animation_speed=0.018),
    "retro": Theme("Retro", (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 100, 0), (255, 200, 0), [(255, 255, 0), (255, 200, 0), (255, 150, 0), (255, 100, 0), (255, 50, 0), (200, 0, 255), (150, 0, 255), (100, 0, 255), (50, 0, 255)], animation_speed=0.03),
    "ghost": Theme("Ghost", (200, 200, 255), (150, 150, 255), (220, 220, 255), (100, 100, 255), (255, 100, 150), [(200, 200, 255), (180, 180, 255), (160, 160, 255), (140, 140, 255), (120, 120, 255), (100, 100, 255), (80, 80, 255), (60, 60, 255), (40, 40, 255)], animation_speed=0.035),
    "galaxy": Theme("Galaxy", (80, 40, 150), (120, 60, 220), (200, 100, 255), (255, 80, 120), (255, 200, 80), [(80, 40, 150), (100, 50, 180), (130, 70, 220), (160, 90, 255), (190, 110, 255), (220, 140, 255), (240, 180, 255), (255, 220, 255), (255, 255, 200)], animation_speed=0.018),
    "halloween": Theme("Halloween", (200, 50, 0), (255, 140, 0), (255, 200, 50), (150, 0, 0), (255, 80, 80), [(255, 140, 0), (200, 80, 0), (150, 0, 0), (255, 50, 50), (255, 100, 0), (180, 30, 0), (220, 0, 0), (255, 0, 100), (255, 180, 50)], animation_speed=0.025),
    "christmas": Theme("Christmas", (0, 100, 0), (0, 180, 0), (220, 20, 60), (255, 215, 0), (255, 50, 50), [(0, 100, 0), (0, 140, 0), (0, 180, 0), (220, 20, 60), (255, 0, 0), (255, 50, 50), (255, 215, 0), (200, 200, 200), (255, 255, 255)], animation_speed=0.02)
}

def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def print_header(tokens_count=0, reports_count=0, current_reason="NONE"):
    clear_screen()
    status_lines = []
    status_lines.append(f"Theme: {config.theme.name}")
    if config.random_rotation_enabled:
        status_lines.append("Random Rotation: ON")
    if config.shuffle_colors_enabled:
        status_lines.append("Color Shuffle: ON")
    status_text = " | ".join(status_lines).center(35)
    
    ascii_art = [
        "   ⛧   =               ⛧          .         ✦           .      ⛧              ",
        "    .- ✦           .       ___       .        .      .         .      .       ",
        ".          ⛧            __/  |\\_      ✦    .       ✦         .        .       ",
        "   .   ✦.            _/    _|  \\_    F A N T O X X E R      ⛧       ",
        "   .  -       .    _/   _/  |    \\_           .      .     ✦           .    ",
        f"   ⛧  .     ✦    _/___/  -  |  -    \\_  TOKENS : {tokens_count:03d}     ",
        "   .   ✦        /  /        |        \\      .     .         .     -   ✦     ",
        f"    -    .  -  /  /    ⛧    |    ⛧    \\   REASON : {current_reason.upper()}   ",
        "     -        /__/__________|_________\\  ",
        f"   .⛧ .      /  /  /  /  /  /  /  /  /  TOTAL REPORTS : {reports_count:,}      ",
        "       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ",
        "            ______      _   _ _______ ______   ____   ________ _____             ",
        "           |  ____/\\   | \\ | |__   __/ __ \\ \\ / /\\ \\ / /  ____|  __ \\            ",
        "           | |__ /  \\  |  \\| |  | | | |  | \\ V /  \\ V /| |__  | |__) |           ",
        "           |  __/ /\\ \\ | . ` |  | | |  | |> <    > < |  __| |  _  /            ",
        "           | | / ____ \\| |\\  |  | | |__| / . \\  / . \\| |____| | \\ \\            ",
        "           |_|/_/    \\_\\_| \\_|  |_|  \\____/_/ \\_\\/_/ \\_\\______|_|  \\_\\           ",
        "                                                                                 ",
        "      ⛧   ╔════════════════════════════════════════════════════════════╗   ⛧",
        "          ║                        $ FANTOXXER $                       ║       ",
        "      ⛧   ╠════════════════════════════════════════════════════════════╣   ⛧",
        "          ║  [1]  SINGLE TARGET REPORT                                 ║       ",
        "          ║  [2]  MASS REPORT (links.txt)                              ║       ",
        "          ║  [3]  LOAD TOKENS                                          ║       ",
        "          ║  [4]  LOAD PROXIES                                         ║       ",
        "          ║  [5]  CONFIGURATION MENU                                   ║       ",
        "          ║  [6]  STATISTICS & STATUS                                  ║       ",
        "          ║  [7]  VALIDATE & CLEAN TOKENS                              ║       ",
        "          ║  [8]  THEME CUSTOMIZER                                     ║       ",
        "          ║  [9]  SCRAPE & TEST PROXIES                                ║       ",
        "          ║  [10] TOXXABLE MESSAGES SCRAPER                            ║       ",
        "          ║  [12] PROFILE REPORT [BETA]                                ║       ",
        "          ║  [q]  EXIT                                                 ║       ",
        "      ⛧   ╠════════════════════════════════════════════════════════════╣   ⛧",
    ]
    
    if config.selfbot_user:
        sb_txt = f"@{config.selfbot_user} | {config.selfbot_guilds} guilds | {config.selfbot_friends} friends"
        ascii_art.append(f"          ║  SELFBOT: {sb_txt[:47].ljust(47)}║       ")
    else:
        ascii_art.append("          ║                      >_   READY   _<                       ║       ")
    ascii_art.append("      ⛧   ╚════════════════════════════════════════════════════════════╝   ⛧")
    ascii_art.append("")

    for i, line in enumerate(ascii_art):
        if i < 5 or i >= len(ascii_art) - 6:
            print(rgb(*config.theme.header) + line + "\033[0m")
        
        elif "║  [" in line and "]" in line:
            try:
                idx = int(line.split("[")[1].split("]")[0]) - 1
                color = config.theme.menu_colors[idx % len(config.theme.menu_colors)]
                print(rgb(*color) + line + "\033[0m")
            except:
                print(rgb(*config.theme.accent) + line + "\033[0m")
        
        elif i == 8:
            frame_part = line
            print(rgb(*config.theme.accent) + frame_part + "\033[0m", end="")
            print(rgb(*config.theme.warning) + status_text + "\033[0m")
        
        else:
            print(rgb(*config.theme.accent) + line + "\033[0m")

    print("\n" + " "*24 + rgb(*config.theme.accent) + "COMMAND > \033[0m", end="", flush=True)

logging.getLogger("discord").disabled = True
logging.getLogger("discord").setLevel(logging.WARNING)

class ReporterConfig:
    def __init__(self):
        self.tokens: list[str] = []
        self.proxies: list[str] = []
        self.reason_pool = ["i_dont_like_it","spam","abuse_or_harassment","harmful_misinformation","doxing","something_else"]
        self.current_reason: str = random.choice(self.reason_pool)
        self.context_templates = ["This message contains verbal harassment directed at me or other users with repeated targeted insults.","The message uses rude, vulgar or highly offensive language that is disruptive and inappropriate.","This content promotes hate and discrimination based on identity, race, gender, orientation or other vulnerabilities.","The message includes explicit, graphic or unwanted sexual content that makes users uncomfortable.","There are direct or implied threats of violence or real-world harm in this message.","This content targets, involves or is inappropriate toward a minor.","This appears to be clear spam consisting of repetitive unwanted messages flooding the channel.","The message exposes private identifying information about someone (doxing) which violates Discord guidelines.","This content spreads harmful misinformation or glorifies violence in a dangerous way."]
        self.user_agents = ["Discord/9999 CFNetwork/1408.0.4 Darwin/22.5.0","Discord-Android/999;RN","Discord-iOS/999 CFNetwork/1408.0.4","Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36","Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1","Discord-Android/1000;RN","Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36","Discord/10000 CFNetwork/1490.0.4 Darwin/23.5.0","Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1","Discord-Android/1001;RN","Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 Chrome/118.0.0.0 Mobile Safari/537.36","Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 Version/17.1 Mobile/15E148 Safari/604.1","Discord/10001 CFNetwork/1492 Darwin/23.6.0","Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 Chrome/122.0.0.0 Mobile Safari/537.36","Discord/25647 CFNetwork/1568.0.0 Darwin/24.2.0",                         "Discord/25650 CFNetwork/1568.1 Darwin/24.3.0",                           "Discord-Android/256500;RN",                                               "Discord-iOS/256.0 CFNetwork/1568 Darwin/24.0.0",                          "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 Chrome/130.0.0.0 Mobile Safari/537.36","Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 Version/18.1 Mobile/15E148 Safari/604.1","Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 Chrome/128.0.0.0 Mobile Safari/537.36",  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/129.0.0.0 Safari/537.36","Mozilla/5.0 (Linux; Android 15; SM-S931B) AppleWebKit/537.36 Chrome/131.0.0.0 Mobile Safari/537.36",  "Discord/25700 CFNetwork/1570 Darwin/24.4.0",                              ]
        self.proxy_health = {}
        self.token_proxy_map = {}
        self.token_last_activity = {}
        self.delay: float = 3.5
        self.jitter: float = 2.5
        self.rotate_proxy: bool = False
        self.max_daily_reports_per_token = 35
        self.reports_success: int = 0
        self.reports_failed: int = 0
        self.invalid_tokens_count: int = 0

        self.thinking_chance = 0.92
        self.thinking_delay_min = 6.0
        self.thinking_delay_max = 38.0

        self.breathing_min_reports = 2
        self.breathing_max_reports = 7
        self.breathing_pause_min = 45.0
        self.breathing_pause_max = 420.0

        self.fake_error_chance = 0.04
        self.context_typo_chance = 0.08

        self.session_break_every_min = 3
        self.session_break_every_max = 7
        self.session_break_min = 180.0
        self.session_break_max = 1800.0

        self.selfbot_token = self._load_selfbot_token()
        self.selfbot_enabled = bool(self.selfbot_token.strip())
        self.selfbot_user = None
        self.selfbot_guilds = 0
        self.selfbot_friends = 0

        self.report_keywords = ["badword", "spam", "hate"]  
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        if hasattr(config, k):
                            setattr(config, k, v)
            except:
                pass
        self.config_file = "fantoxxer_config.json"
        self.load_config()

        self.normal_activity_chance = 0.18
        self.theme = Themes["classic"]
        self.selected_shuffle_themes = []
        if os.path.exists("shuffle_themes.json"):
            try:
                with open("shuffle_themes.json", "r") as f:
                    saved = json.load(f)
                    self.selected_shuffle_themes = [k for k in saved if k in Themes]
            except:
                pass

        self.load_theme_from_file()
        if self.selected_shuffle_themes:
            random_key = random.choice(self.selected_shuffle_themes)
            if random_key in Themes:
                self.theme = Themes[random_key]
                print(f"Auto-selected random theme from saved list: {self.theme.name}")

        self.random_rotation_enabled = len(self.selected_shuffle_themes) > 0
        self.shuffle_colors_enabled = False 
        self.report_keywords = [
            "kill yourself", "kys", "rope", "self harm", "selfharm", "commit suicide", "hang yourself",
            "nigger", "nigga", "faggot", "tranny", "retard", "autistic", "schizo", "rape", "raped", "rapist",
            "pedophile", "pedo", "cp", "child porn", "loli", "shotacon", "dox", "doxing", "address", "home address",
            "full name", "leak", "leaked", "swatting", "bomb", "explode", "terrorist", "isis", "jihad",
            "hitler", "nazi", "heil", "1488", "kike", "jewtube", "holocaust denial", "gas chamber",
            "spam", "raid", "nuke", "crash", "token grab", "token logger", "grabber", "stealer",
            "porn", "nsfw", "onlyfans", "sext", "nudes", "send nudes", "horny", "cum", "sex",
            "threat", "threaten", "harass", "stalk", "swat", "ddos", "hack", "doxxed",
        ]

    def _load_selfbot_token(self):
        if hasattr(self, 'config_file') and os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                token = data.get("selfbot_token", "").strip()
                if token:
                    return token
            except:
                pass
        env_token = os.getenv("FANTOXXER_SELF_TOKEN", "").strip()
        if env_token:
            return env_token
        if not hasattr(self, '_token_prompted'):
            #token = input("\033[96m[Selfbot] Enter user token: \033[0m").strip()
            token = "TOKEN"
            self._token_prompted = True
            if token:
                return token
        return ""

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                print("\033[92m[Config] Loaded saved settings\033[0m")
            except Exception as e:
                print(f"\033[93m[Config] Failed to load: {e}\033[0m")

    def save_config(self):
        data = {"delay": self.delay,"jitter": self.jitter,"fake_error_chance": self.fake_error_chance,"context_typo_chance": self.context_typo_chance,"normal_activity_chance": self.normal_activity_chance,"breathing_min_reports": self.breathing_min_reports,"breathing_max_reports": self.breathing_max_reports,"breathing_pause_min": self.breathing_pause_min,"breathing_pause_max": self.breathing_pause_max,"session_break_every_min": self.session_break_every_min,"session_break_every_max": self.session_break_every_max,"max_daily_reports_per_token": self.max_daily_reports_per_token,"thinking_chance": self.thinking_chance,"selfbot_token": self.selfbot_token, }
        with open(self.config_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_tokens(self, path: str = "tokens.txt") -> bool:
        if not os.path.exists(path):
            print(f"\033[91m[!] {path} not found!\033[0m")
            return False
        with open(path, "r", encoding="utf-8") as f:
            self.tokens = [t.strip() for t in f if t.strip() and len(t.strip()) > 40]
        print(f"\033[92m[+] Loaded {len(self.tokens)} tokens\033[0m")
        return True

    def load_proxies(self, path: str = "proxies.txt") -> bool:
        if not os.path.exists(path):
            print(f"\033[91m[!] {path} not found!\033[0m")
            return False
        with open(path, "r", encoding="utf-8") as f:
            self.proxies = [p.strip() for p in f if p.strip()]
        for p in self.proxies:
            self.proxy_health[p] = {"success": 0, "fail": 0}
        print(f"\033[92m[+] Loaded {len(self.proxies)} proxies\033[0m")
        return True


    def get_best_proxy_for_token(self, token: str):
        if token in self.token_proxy_map:
            p = self.token_proxy_map[token]
            if self.proxy_health.get(p, {"fail": 0})["fail"] < 4:
                return p
        good_proxies = [p for p, stats in self.proxy_health.items() if stats["fail"] < 4]
        if good_proxies:
            p = random.choice(good_proxies)
            self.token_proxy_map[token] = p
            return p
        return None

    def load_theme_from_file(self):
            if os.path.exists("theme.json"):
                try:
                    with open("theme.json", "r") as f:
                        data = json.load(f)
                        theme_name = data.get("default_theme", "classic").lower()
                        if theme_name in Themes:
                            self.theme = Themes[theme_name]
                except:
                    pass

    def save_theme_to_file(self):
        try:
            with open("theme.json", "w") as f:
                json.dump({"default_theme": self.theme.name.lower()}, f, indent=4)
        except:
            pass

    def update_proxy_health(self, proxy: str, success: bool):
        if proxy:
            if success:
                self.proxy_health[proxy]["success"] += 1
            else:
                self.proxy_health[proxy]["fail"] += 1

    def send_normal_presence(self, token: str):
        try:
            url = "https://discord.com/api/v9/users/@me/settings"
            headers = {"Authorization": token, "User-Agent": random.choice(self.user_agents)}
            data = {"status": random.choice(["online", "idle", "dnd"])}
            requests.patch(url, headers=headers, json=data, timeout=6)
        except:
            pass

    def validate_and_clean_tokens(self):
        if not self.tokens:
            print("\033[93mNo tokens loaded.\033[0m")
            return 0
        print("\n\033[93mValidating tokens...\033[0m")
        valid_tokens = []
        checked = 0
        for token in self.tokens:
            checked += 1
            try:
                r = requests.get(
                    "https://discord.com/api/v9/users/@me",
                    headers={"Authorization": token, "User-Agent": random.choice(self.user_agents)},
                    timeout=8
                )
                if r.status_code == 200:
                    valid_tokens.append(token)
                    print(f"[{checked}/{len(self.tokens)}] VALID   ", end="\r")
                else:
                    self.invalid_tokens_count += 1
                    print(f"[{checked}/{len(self.tokens)}] INVALID ", end="\r")
                time.sleep(random.uniform(1.8, 4.5))
            except:
                self.invalid_tokens_count += 1
                print(f"[{checked}/{len(self.tokens)}] ERROR   ", end="\r")
                time.sleep(2.0)
        old = len(self.tokens)
        self.tokens = valid_tokens
        print(f"\n\033[92mValidation complete:\033[0m {len(valid_tokens)} valid / {old} total")
        print(f"   Removed: {old - len(valid_tokens)} invalid tokens\n")
        return len(valid_tokens)

config = ReporterConfig()

def parse_message_link(url: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    pattern = r"https?://discord(?:app)?\.com/channels/(\d+|@me)/(\d+)/(\d+)"
    m = re.match(pattern, url.strip())
    return m.groups() if m else (None, None, None)

def get_humanized_context():
    base = random.choice(config.context_templates)
    if random.random() >= config.context_typo_chance:
        return base
    variations = [base,base + " Please take immediate action on this.",base.capitalize(),base + " This has been ongoing for some time.",base + " Thank you for reviewing.",base.replace(" ", "  ").strip()]
    return random.choice(variations)

def get_report_payload(guild_id: str, channel_id: str, message_id: str):
    payload = {
        "channel_id": channel_id,
        "message_id": message_id,
        "reason": config.current_reason
    }
    if guild_id and guild_id != "@me":
        payload["guild_id"] = guild_id
    return payload

async def send_report(
    session: aiohttp.ClientSession,
    token: str,
    guild_id: str,
    channel_id: str,
    message_id: str
) -> Tuple[bool, str]:
    url = "https://discord.com/api/v10/reporting/message"

    headers = {"Authorization": token,"Content-Type": "application/json","User-Agent": random.choice(config.user_agents),"X-Discord-Locale": "en-US","X-Debug-Options": "bugReporterEnabled","Accept-Language": "en-US,en;q=0.9","X-Super-Properties": get_random_super_properties()}
    payload = get_report_payload(guild_id, channel_id, message_id)

    proxy = config.get_best_proxy_for_token(token)
    proxy_url = f"http://{proxy}" if proxy else None
    try:
        async with session.post(url,headers=headers,json=payload,proxy=proxy_url,timeout=aiohttp.ClientTimeout(total=14)) as resp:
            if resp.status in (200, 201, 204):
                config.update_proxy_health(proxy, True)
                return True, "Success"

            elif resp.status == 429:
                try:
                    data = await resp.json()
                    retry_after = float(data.get("retry_after", 10))
                    config.update_proxy_health(proxy, False)
                    return False, f"Rate limited - wait {retry_after:.1f}s"
                except:
                    config.update_proxy_health(proxy, False)
                    return False, "Rate limited (no retry-after)"

            elif resp.status == 401:
                config.update_proxy_health(proxy, False)
                return False, "Invalid token (401)"

            else:
                text = await resp.text()
                config.update_proxy_health(proxy, False)
                return False, f"Failed {resp.status} - {text[:120]}"

    except asyncio.TimeoutError:
        config.update_proxy_health(proxy, False)
        return False, "Timeout"
    except Exception as e:
        config.update_proxy_health(proxy, False)
        return False, f"Exception: {type(e).__name__}"

def send_report_sync(token: str, guild_id: str, channel_id: str, message_id: str) -> Tuple[bool, str]:
    url = "https://discord.com/api/v10/reporting/message"
    headers = {"Authorization": token,"Content-Type": "application/json","User-Agent": random.choice(config.user_agents),"X-Discord-Locale": "en-US","X-Debug-Options": "bugReporterEnabled","Accept-Language": "en-US,en;q=0.9","X-Super-Properties": get_random_super_properties()}
    payload = get_report_payload(guild_id, channel_id, message_id)
    proxy = config.get_best_proxy_for_token(token)
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
    
    for attempt in range(2):
        try:
            use_proxies = proxies if attempt == 0 else None
            resp = requests.post(url, headers=headers, json=payload, proxies=use_proxies, timeout=14)
            print(f"\n\033[96m[DEBUG] Status: {resp.status_code}\033[0m")
            print(f"\033[96m[DEBUG] Response: -Null-\033[0m")
            if resp.status_code in (200, 201, 204):
                if attempt == 0:
                    config.update_proxy_health(proxy, True)
                return True, "Success"
            elif resp.status_code == 429:
                if attempt == 0:
                    config.update_proxy_health(proxy, False)
                try:
                    data = resp.json()
                    return False, f"Rate limited - wait {data.get('retry_after', '?')}s"
                except:
                    return False, "Rate limited"
            elif resp.status_code == 401:
                if attempt == 0:
                    config.update_proxy_health(proxy, False)
                return False, "Invalid token (401)"
            else:
                if attempt == 0:
                    config.update_proxy_health(proxy, False)
                try:
                    body = resp.text[:500]
                    print(f"\n\033[93m[DEBUG] Status: {resp.status_code}\033[0m")
                    print(f"\033[93m[DEBUG] Response: -Null-\033[0m")
                    print(f"\033[93m[DEBUG] Payload sent: {json.dumps(payload)}\033[0m")
                except:
                    pass
                return False, f"Failed {resp.status_code}"
        except (requests.Timeout, requests.exceptions.ProxyError, requests.exceptions.ConnectionError) as e:
            if attempt == 0:
                config.update_proxy_health(proxy, False)
                continue
            return False, f"Error: {type(e).__name__}"
        except Exception as e:
            if attempt == 0:
                config.update_proxy_health(proxy, False)
            print(f"\033[91m[DEBUG] Exception: {e}\033[0m")
            return False, f"Error: {type(e).__name__}"
    return False, "All attempts failed"

async def send_normal_presence_async(session: aiohttp.ClientSession, token: str):
    try:
        url = "https://discord.com/api/v9/users/@me/settings"
        headers = {"Authorization": token, "User-Agent": random.choice(config.user_agents)}
        data = {"status": random.choice(["online", "idle", "dnd"])}
        await session.patch(url, headers=headers, json=data, timeout=6)
    except:
        pass

async def async_perform_reports(link: str, loops: int = 1):
    guild_id, channel_id, message_id = parse_message_link(link)
    if not message_id:
        print("\033[91mInvalid message link!\033[0m")
        return 0, 0

    print(f"\033[96mTarget: {message_id} | Ch: {channel_id} | Guild: {guild_id}\033[0m")
    print("\033[93mWARNING: keep total reports per message low (max 8-12 recommended)\033[0m")

    if not config.tokens:
        print("\033[91mNo tokens loaded!\033[0m")
        return 0, 0

    success_count = 0
    fail_count = 0

    connector = aiohttp.TCPConnector(limit=60)  
    async with aiohttp.ClientSession(connector=connector) as session:

        if random.random() < config.thinking_chance:
            think = random.uniform(config.thinking_delay_min, config.thinking_delay_max)
            print(f"\033[90mThinking... ({think:.1f}s)\033[0m")
            await asyncio.sleep(think)

        for loop in range(loops):
            config.current_reason = random.choice(config.reason_pool)
            print(f"\n\033[95mCycle {loop+1}/{loops if loops != float('inf') else '∞'} - Reason: {config.current_reason}\033[0m")
            random.shuffle(config.tokens)

            reports_this_cycle = 0
            total_reports = len(config.tokens)

            while reports_this_cycle < total_reports:
                burst_size = min(
                    random.randint(config.breathing_min_reports, config.breathing_max_reports),
                    total_reports - reports_this_cycle
                )

                tasks = []
                for _ in range(burst_size):
                    token = config.tokens[reports_this_cycle]
                    reports_this_cycle += 1

                    print(f"[{reports_this_cycle}/{total_reports}] ", end="", flush=True)

                    if random.random() < config.normal_activity_chance:
                        print("\033[90m(normal presence)\033[0m ", end="")
                        tasks.append(send_normal_presence_async(session, token))

                    if serror(): 
                        fail_count += 1
                        config.reports_failed += 1
                        log_report_result(False, token, message_id, config.current_reason + " [sim]")
                        print("\033[93m[sim fail]\033[0m")
                    else:
                        tasks.append(asyncio.create_task(
                                send_report(session, token, guild_id, channel_id, message_id)
                            )
                        )
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for res in results:
                    if isinstance(res, Exception):
                        fail_count += 1
                        config.reports_failed += 1
                        print(f"\033[91mException in task\033[0m")
                    elif isinstance(res, tuple):
                        ok, msg = res
                        if ok:
                            print(f"\033[92m{msg}\033[0m")
                            success_count += 1
                            config.reports_success += 1
                        else:
                            print(f"\033[91m{msg}\033[0m")
                            fail_count += 1
                            config.reports_failed += 1
                        log_report_result(ok, token, message_id, config.current_reason)
                await asyncio.sleep(config.delay + random.uniform(-config.jitter * 2.0, config.jitter * 2.5))

                if reports_this_cycle < total_reports:
                    pause = random.uniform(config.breathing_pause_min, config.breathing_pause_max)
                    print(f"\033[90m  pause {pause:.0f}s  \033[0m")
                    await asyncio.sleep(pause)

            if loop < loops - 1:
                if random.randint(config.session_break_every_min, config.session_break_every_max) <= 4:
                    brk = random.uniform(config.session_break_min, config.session_break_max)
                    print(f"\n\033[90mLong session break {brk:.0f}s\033[0m\n")
                    await asyncio.sleep(brk)
                else:
                    extra = random.uniform(10, 90)
                    print(f"\033[90mWaiting {extra:.0f}s...\033[0m")
                    await asyncio.sleep(extra)

    return success_count, fail_count
def perform_reports(link: str, loops: int = 1):
    return asyncio.run(async_perform_reports(link, loops))

def serror():
    if random.random() >= config.fake_error_chance:
        return False
    fake_msgs = ["Rate limited", "Server error", "Connection timeout"]
    print(f"\033[93m[Error] {random.choice(fake_msgs)}\033[0m")
    time.sleep(random.uniform(8, 25))
    return True

def log_report_result(success: bool, token: str, message_id: str, reason: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILED"
    line = f"[{timestamp}] {status} | MSG: {message_id} | TOKEN: {token[:12]}... | REASON: {reason}\n"
    try:
        with open("reports_log.txt", "a", encoding="utf-8") as f:
            f.write(line)
    except:
        pass

def perform_reports(link: str, loops: int = 1):
    guild_id, channel_id, message_id = parse_message_link(link)
    if not message_id:
        print("\033[91mInvalid message link!\033[0m")
        return 0, 0

    print(f"\033[96mTarget: {message_id} | Ch: {channel_id} | Guild: {guild_id}\033[0m")
    print("\033[93mWARNING: keep total reports per message low (max 8-12 recommended)\033[0m")

    if not config.tokens:
        print("\033[91mNo tokens loaded!\033[0m")
        return 0, 0

    success_count = 0
    fail_count = 0

    if random.random() < config.thinking_chance:
        think = random.uniform(config.thinking_delay_min, config.thinking_delay_max)
        print(f"\033[90mThinking... ({think:.1f}s)\033[0m")
        time.sleep(think)

    endless = loops == float('inf')
    loop = 0
    while endless or loop < loops:
        config.current_reason = random.choice(config.reason_pool)
        print(f"\n\033[95mCycle {loop+1}/{'∞' if endless else loops} - Reason: {config.current_reason}\033[0m")
        random.shuffle(config.tokens)

        reports_this_cycle = 0
        total_reports = len(config.tokens)

        while reports_this_cycle < total_reports:
            burst_size = min(
                random.randint(config.breathing_min_reports, config.breathing_max_reports),
                total_reports - reports_this_cycle
            )

            for _ in range(burst_size):
                i = reports_this_cycle + 1
                token = config.tokens[reports_this_cycle]

                print(f"[{i}/{total_reports}] ", end="", flush=True)

                if random.random() < config.normal_activity_chance:
                    print("\033[90m(normal presence)\033[0m ", end="")
                    config.send_normal_presence(token)

                if serror():
                    fail_count += 1
                    config.reports_failed += 1
                    log_report_result(False, token, message_id, config.current_reason + " [sim]")
                else:
                    ok, msg = send_report_sync(token, guild_id, channel_id, message_id)
                    if ok:
                        print(f"\033[92m{msg}\033[0m")
                        success_count += 1
                        config.reports_success += 1
                    else:
                        print(f"\033[91m{msg}\033[0m")
                        fail_count += 1
                        config.reports_failed += 1

                    log_report_result(ok, token, message_id, config.current_reason)

                reports_this_cycle += 1

                time.sleep(config.delay + random.uniform(-config.jitter * 2.0, config.jitter * 2.5))

            if reports_this_cycle < total_reports:
                pause = random.uniform(config.breathing_pause_min, config.breathing_pause_max)
                print(f"\033[90m  pause {pause:.0f}s  \033[0m")
                time.sleep(pause)

        loop += 1
        if endless or loop < loops:
            if random.randint(config.session_break_every_min, config.session_break_every_max) <= 4:
                brk = random.uniform(config.session_break_min, config.session_break_max)
                print(f"\n\033[90mLong session break {brk:.0f}s\033[0m\n")
                time.sleep(brk)
            else:
                extra = random.uniform(10, 90)
                print(f"\033[90mWaiting {extra:.0f}s...\033[0m")
                time.sleep(extra)

    return success_count, fail_count

def single_report_classic():
    clear_screen()
    print("\033[96m=== SINGLE REPORT ===\033[0m\n")
    link = input("Enter message link: ").strip()
    if not link:
        print("No link provided.")
        input("\nPress ENTER...")
        return
    try:
        count = int(input("How many times? (1-10): ").strip())
        count = max(1, min(10, count))
    except:
        count = 1
    success, fails = perform_reports(link, loops=count)
    print(f"\n\033[92mCompleted:\033[0m {success} success | {fails} failed")
    input("\nPress ENTER to continue...")

def mass_report():
    if not os.path.exists("links.txt"):
        print("\033[91m[!] links.txt not found!\033[0m")
        input("\nPress ENTER...")
        return
    with open("links.txt", "r", encoding="utf-8") as f:
        links = [l.strip() for l in f if l.strip()]
    if not links:
        print("No links found.")
        input("\nPress ENTER...")
        return
    total_s = 0
    total_f = 0
    for i, link in enumerate(links, 1):
        print(f"\n\033[96m[{i}/{len(links)}]\033[0m {link}")
        s, f = perform_reports(link, 1)
        total_s += s
        total_f += f
    print(f"\n\033[92mMass complete:\033[0m {total_s} success | {total_f} failed")
    input("\nPress ENTER...")

def config_menu():
    while True:
        clear_screen()
        print("\033[96mCONFIGURATION MENU\033[0m\n")
        print("Current values:")
        print(f"  [1] Delay:                {config.delay:.1f}s ± {config.jitter:.1f}s")
        print(f"  [2] Fake error chance:    {config.fake_error_chance:.1%}")
        print(f"  [3] Context typo chance:  {config.context_typo_chance:.1%}")
        print(f"  [4] Normal activity chance: {config.normal_activity_chance:.1%}")
        print(f"  [5] Breathing burst size: {config.breathing_min_reports}–{config.breathing_max_reports}")
        print(f"  [6] Breathing pause:      {config.breathing_pause_min:.0f}–{config.breathing_pause_max:.0f}s")
        print(f"  [7] Session break every:  {config.session_break_every_min}–{config.session_break_every_max} cycles")
        print(f"  [8] Max reports/day/token: {config.max_daily_reports_per_token}")
        print(f"  [9] Thinking chance:      {config.thinking_chance:.1%}")
        print(f"  [10] Selfbot mode:       {'ON' if config.selfbot_enabled else 'OFF'} (token: {'set' if config.selfbot_token else 'not set'})")
        print("  [0] Back to main menu")
        print()

        choice = input("Select setting to change (0-10): ").strip()

        if choice == '0':
            break

        try:
            val = int(choice)
        except ValueError:
            print("\033[91mInvalid choice!\033[0m")
            input("\nPress ENTER...")
            continue

        if val == 1:
            try:
                delay = float(input(f"New delay (current: {config.delay:.1f}): "))
                jitter = float(input(f"New jitter ± (current: {config.jitter:.1f}): "))
                config.delay = max(0.5, delay)
                config.jitter = max(0.0, jitter)
                print("\033[92mUpdated!\033[0m")
            except:
                print("\033[91mInvalid input!\033[0m")

        elif val == 2:
            try:
                chance = float(input(f"New fake error chance (0-1, current: {config.fake_error_chance:.3f}): "))
                config.fake_error_chance = max(0.0, min(1.0, chance))
                print("\033[92mUpdated!\033[0m")
            except:
                print("\033[91mInvalid input!\033[0m")

        elif val == 3:
            try:
                chance = float(input(f"New context typo chance (0-1, current: {config.context_typo_chance:.3f}): "))
                config.context_typo_chance = max(0.0, min(1.0, chance))
                print("\033[92mUpdated!\033[0m")
            except:
                print("\033[91mInvalid input!\033[0m")

        elif val == 4:
            try:
                chance = float(input(f"New normal activity chance (0-1, current: {config.normal_activity_chance:.3f}): "))
                config.normal_activity_chance = max(0.0, min(1.0, chance))
                print("\033[92mUpdated!\033[0m")
            except:
                print("\033[91mInvalid input!\033[0m")

        elif val == 5:
            try:
                min_b = int(input(f"Min burst size (current: {config.breathing_min_reports}): "))
                max_b = int(input(f"Max burst size (current: {config.breathing_max_reports}): "))
                config.breathing_min_reports = max(1, min_b)
                config.breathing_max_reports = max(config.breathing_min_reports, max_b)
                print("\033[92mUpdated!\033[0m")
            except:
                print("\033[91mInvalid input!\033[0m")

        elif val == 6:
            try:
                min_p = float(input(f"Min pause (current: {config.breathing_pause_min:.0f}): "))
                max_p = float(input(f"Max pause (current: {config.breathing_pause_max:.0f}): "))
                config.breathing_pause_min = max(5.0, min_p)
                config.breathing_pause_max = max(config.breathing_pause_min, max_p)
                print("\033[92mUpdated!\033[0m")
            except:
                print("\033[91mInvalid input!\033[0m")

        elif val == 7:
            try:
                min_s = int(input(f"Min cycles before break (current: {config.session_break_every_min}): "))
                max_s = int(input(f"Max cycles before break (current: {config.session_break_every_max}): "))
                config.session_break_every_min = max(1, min_s)
                config.session_break_every_max = max(config.session_break_every_min, max_s)
                print("\033[92mUpdated!\033[0m")
            except:
                print("\033[91mInvalid input!\033[0m")

        elif val == 8:
            try:
                max_rep = int(input(f"Max reports per token per day (current: {config.max_daily_reports_per_token}): "))
                config.max_daily_reports_per_token = max(5, max_rep)
                print("\033[92mUpdated!\033[0m")
            except:
                print("\033[91mInvalid input!\033[0m")

        elif val == 9:
            try:
                chance = float(input(f"New thinking chance (0-1, current: {config.thinking_chance:.3f}): "))
                config.thinking_chance = max(0.0, min(1.0, chance))
                print("\033[92mUpdated!\033[0m")
            except:
                print("\033[91mInvalid input!\033[0m")

        elif val == 10:  
            new_token = input("Enter selfbot user token (empty to disable): ").strip()
            config.selfbot_token = new_token
            config.selfbot_enabled = bool(new_token.strip())
            config.save_config()
            print(f"\033[92mSelfbot {'enabled' if config.selfbot_enabled else 'disabled'}!\033[0m")

        else:
            print("\033[91mInvalid option!\033[0m")

        input("\nPress ENTER to continue...")

def show_stats():
    clear_screen()
    print("\033[96mSTATISTICS:\033[0m\n")
    print(f"Tokens loaded:          {len(config.tokens)}")
    print(f"Proxies loaded:         {len(config.proxies)}")
    print(f"Successful reports:     \033[92m{config.reports_success:,}\033[0m")
    print(f"Failed reports:         \033[91m{config.reports_failed:,}\033[0m")
    print(f"Known invalid tokens:   \033[93m{config.invalid_tokens_count:,}\033[0m")
    print(f"Log file:               reports_log.txt")
    print()
    input("Press ENTER...")

def validate_tokens_menu():
    clear_screen()
    print("\033[96mTOKEN VALIDATOR & CLEANER\033[0m\n")
    print("This checks tokens against Discord API")
    print("\033[93mWarning: visible to Discord - use sparingly!\033[0m\n")
    keep = input("Continue? (y/n): ").strip().lower()
    if keep != 'y':
        print("Cancelled.")
        input("\nPress ENTER...")
        return
    config.validate_and_clean_tokens()
    input("\nPress ENTER...")

def animate_text(text, speed=None):
    speed = speed or config.theme.animation_speed
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def theme_customizer():
    clear_screen()
    animate_text(rgb(*config.theme.accent) + "THEME CUSTOMIZER\n" + "\033[0m", 0.02)
    
    print("Available themes (1-18):")
    keys = list(Themes.keys())
    for i, key in enumerate(keys, 1):
        th = Themes[key]
        color = rgb(*th.accent)
        print(f"{color}[{i}]\033[0m {th.name}")
    print()
    print(f"{rgb(*config.theme.warning)}[19]\033[0m Shuffle colors of selected themes")
    print(f"{rgb(*config.theme.success)}[20]\033[0m Random theme")
    print()

    try:
        sel = input("Select option (1-20, or Enter to cancel): ").strip()
        if not sel:
            print("\nCancelled.")
            input("\nPress ENTER...")
            return

        sel = int(sel)
        if 1 <= sel <= len(keys):
            config.theme = Themes[keys[sel-1]]
            config.save_theme_to_file()
            animate_text(f"\n{rgb(*config.theme.success)}Theme set to: {config.theme.name}\033[0m", 0.03)
        elif sel == 19:
            shuffle_selected_themes()
        elif sel == 20:
            random_theme()
        else:
            animate_text("\n\033[91mInvalid selection\033[0m")
    except ValueError:
        animate_text("\n\033[91mPlease enter a valid number\033[0m")
    except Exception as e:
        animate_text(f"\n\033[91mError: {str(e)}\033[0m")

    input("\nPress ENTER to continue...")

def random_theme():
    keys = list(Themes.keys())
    random_key = random.choice(keys)
    config.theme = Themes[random_key]
    config.save_theme_to_file()
    animate_text(f"\n{rgb(*config.theme.success)}Random theme applied: {config.theme.name}\033[0m", 0.03)
    input("\nPress ENTER...")

def shuffle_selected_themes():
    config.shuffle_colors_enabled = True
    clear_screen()
    animate_text(rgb(*config.theme.accent) + "SHUFFLE / RANDOMIZE Themes\n" + "\033[0m", 0.02)
    
    print("Available Themes:")
    keys = list(Themes.keys())
    for i, key in enumerate(keys, 1):
        print(f"[{i}] {Themes[key].name}")
    print()
    
    print("Enter theme numbers to include in random rotation (comma-separated, e.g. 1,5,10)")
    print("Press Enter without input to cancel.")
    print()

    try:
        user_input = input("Your selection: ").strip()
        if not user_input:
            print("\nCancelled.")
            input("\nPress ENTER...")
            return
        selections = [int(x.strip()) for x in user_input.split(",")]
        selected_keys = []
        for s in selections:
            if 1 <= s <= len(keys):
                selected_keys.append(keys[s-1])
            else:
                print(f"\033[93mWarning: {s} invalid, skipped.\033[0m")
        
        if not selected_keys:
            animate_text("\n\033[91mNo valid Themes selected.\033[0m")
            input("\nPress ENTER...")
            return
        config.selected_shuffle_themes = selected_keys
        with open("shuffle_themes.json", "w") as f:
            json.dump([k for k in selected_keys], f)

        animate_text(f"\n{rgb(*config.theme.success)}Saved {len(selected_keys)} Themes for random rotation on startup!\033[0m", 0.03)
        print("Next time you start the script, one of these will be randomly chosen as active theme.")
        print("(You can always change this in THEME CUSTOMIZER → 19 again)")
        if input("\nApply random one now? (y/n): ").lower() == 'y':
            random_key = random.choice(selected_keys)
            config.theme = Themes[random_key]
            config.save_theme_to_file()
            animate_text(f"\n{rgb(*config.theme.success)}Applied: {config.theme.name}\033[0m", 0.03)
        
    except ValueError:
        animate_text("\n\033[91mInvalid input - use numbers separated by commas\033[0m")
    except Exception as e:
        animate_text(f"\n\033[91mError: {str(e)}\033[0m")

    input("\nPress ENTER to return...")

def reset_to_default():
    clear_screen()
    config.theme = Themes["classic"]
    config.save_theme_to_file()
    animate_text(f"\n{rgb(*config.theme.success)}Theme reset to: Classic\033[0m", 0.03)
    input("\nPress ENTER to continue...")

def get_random_super_properties() -> str:
    props = {"os": random.choice(["Windows", "Mac OS X", "Linux", "Android", "iOS"]),"browser": "Discord Client","release_channel": "stable","client_build_number": random.choice([999999, 420420, 314159, 271828, 1234567, 987654]),"client_event_source": None,"client_version": random.choice(["1.0.9150", "1.0.9164", "1.0.9175"]),"system_locale": random.choice(["en-US", "en-GB", "de-DE"]),"browser_user_agent": random.choice(config.user_agents),"browser_version": "999.0","os_version": "10","referrer": "","client_id": "123456789012345678" }
    json_str = json.dumps(props, separators=(',', ':'))
    return base64.b64encode(json_str.encode()).decode('utf-8')

def profile_report_menu():
    clear_screen()
    print("\033[96m=== PROFILE REPORT (User) ===\033[0m\n")
    print("This reports a Discord user profile using user tokens.")
    print("WARNING: Use sparingly — profile reports are highly visible to Discord.\n")
    if not config.tokens:
        print("\033[91mNo tokens loaded!\033[0m")
        input("\nPress ENTER...")
        return
    target_id = input("Enter target USER ID to report: ").strip()
    if not target_id.isdigit():
        print("\033[91mInvalid user ID (numbers only).\033[0m")
        input("\nPress ENTER...")
        return
    valid_reasons = ["age_restricted_content", "child_endangerment", "child_safety", "harassment","harmful_misinformation", "illegal_content", "impersonation", "malicious_links","malware", "nudity", "phishing", "self_harm", "spam", "threats", "toxicity","underage_user", "violence"]
    print("\nValid reasons:")
    for r in valid_reasons:
        print(f"  - {r}")

    reason = input(f"\nReport reason (must be one of above, default: abuse_or_harassment): ").strip().lower()
    if not reason:
        reason = "abuse_or_harassment"  
    if reason not in valid_reasons:
        print(f"\033[93mWarning: '{reason}' is not an official reason — may fail.\033[0m")
        if input("Continue anyway? (y/n): ").lower() != 'y':
            return
    context = input("Additional context (optional, 1-2 sentences): ").strip()
    count_input = input("\nHow many times to report? (1–10 recommended): ").strip()
    try:
        count = max(1, min(10, int(count_input or 5)))
    except:
        count = 5
    print(f"\nReporting user {target_id} × {count} times | Reason: {reason}")
    print(f"Context: {context[:80]}{'...' if len(context)>80 else ''}\n")
    success = 0
    failed = 0
    async def report_profile(token: str):
        nonlocal success, failed
        url = "https://discord.com/api/v9/reporting/user"
        headers = {"Authorization": token,"Content-Type": "application/json","User-Agent": random.choice(config.user_agents),"X-Discord-Locale": random.choice(["en-US", "en-GB"]),"X-Super-Properties": get_random_super_properties()}
        payload = {"user_id": target_id,"reason": reason,}
        if context:
            payload["additional_context"] = context[:500]  

        proxy = config.get_best_proxy_for_token(token)
        proxy_url = f"http://{proxy}" if proxy else None

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload, proxy=proxy_url, timeout=12) as resp:
                    text = await resp.text()
                    if resp.status in (200, 201, 204):
                        success += 1
                        print(f"\033[92mSuccess ({token[-6:]})\033[0m")
                    else:
                        failed += 1
                        print(f"\033[91mFailed ({resp.status}): {text[:120]}\033[0m")
        except Exception as e:
            failed += 1
            print(f"\033[91mError: {type(e).__name__}\033[0m")

    async def run():
        tasks = []
        selected_tokens = random.sample(config.tokens, min(count, len(config.tokens)))
        for token in selected_tokens:
            tasks.append(report_profile(token))
            await asyncio.sleep(random.uniform(2.5, 7.0)) 
        await asyncio.gather(*tasks, return_exceptions=True)

    asyncio.run(run())

    print(f"\n\033[96mDone:\033[0m {success} success | {failed} failed")
    input("\nPress ENTER to return...")

def test_proxy(proxy: str, timeout: int = 8) -> bool:
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    test_url = "https://discord.com/api/v9/users/@me"  
    
    try:
        r = requests.get(test_url, proxies=proxies, timeout=timeout)
        return r.status_code in (401, 403, 429)
    except:
        return False

def scrape_proxies():
    sources = ["https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt","https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http,socks5&timeout=12000","https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt","https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt","https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt",]
    
    all_proxies = set()
    print("\033[96m[SCRAPER] Collecting proxies from sources...\033[0m")
    
    for url in sources:
        try:
            resp = requests.get(url, timeout=12)
            if resp.status_code == 200:
                lines = resp.text.strip().splitlines()
                cleaned = {line.strip() for line in lines if ':' in line and not line.startswith('#')}
                all_proxies.update(cleaned)
                print(f"  + {len(cleaned)} from {url.split('/')[-1]}")
        except Exception as e:
            print(f"  Failed {url.split('/')[-1]} → {str(e)[:60]}")
    
    print(f"\n\033[93mTotal unique proxies collected: {len(all_proxies):,}\033[0m")
    
    if not all_proxies:
        print("\033[91mNo proxies collected. Check internet/sources.\033[0m")
        return
    
    print("\033[96m[TESTING] Checking connectivity to Discord (this will take a while)...\033[0m")
    working = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
        future_to_proxy = {executor.submit(test_proxy, p): p for p in all_proxies}
        done_count = 0
        total = len(all_proxies)
        
        for future in concurrent.futures.as_completed(future_to_proxy):
            done_count += 1
            proxy = future_to_proxy[future]
            try:
                if future.result():
                    working.append(proxy)
                    print(f"\033[92m[+] WORKING  {proxy} ({done_count}/{total})\033[0m", end="\r")
                else:
                    print(f"\033[90m[-] DEAD     {proxy} ({done_count}/{total})\033[0m", end="\r")
            except:
                print(f"\033[90m[-] ERROR    {proxy} ({done_count}/{total})\033[0m", end="\r")
    
    print(f"\n\n\033[92mFound {len(working)} WORKING proxies!\033[0m")
    
    if working:
        mode = input("\nOverwrite proxies.txt (o) or Append (a)? [o/a]: ").lower()
        if mode == 'o':
            with open("proxies.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(working) + "\n")
        else:
            with open("proxies.txt", "a", encoding="utf-8") as f:
                f.write("\n".join(working) + "\n")
        
        config.load_proxies()  
        print(f"\033[92mSaved {len(working)} proxies to proxies.txt\033[0m")
    else:
        print("\033[91mNo working proxies found this time.\033[0m")

def log_toxxable_message(message, keyword_matched, reported=False):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    guild = message.guild.name if message.guild else "DM"
    guild_id = message.guild.id if message.guild else "@me"
    channel = getattr(message.channel, 'name', 'DM')
    channel_id = message.channel.id
    author = f"{message.author} ({message.author.id})"
    content_preview = message.content.replace('\n', ' ').strip()[:200] + ("..." if len(message.content) > 200 else "")
    jump_link = f"https://discord.com/channels/{guild_id}/{channel_id}/{message.id}"
    status = "REPORTED" if reported else "TOXXABLE"

    entry = (
        f"[{ts}] [{status}] {keyword_matched.upper()}\n"
        f"Author: {author}\n"
        f"Guild: {guild} (ID: {guild_id})\n"
        f"Channel: #{channel} (ID: {channel_id})\n"
        f"Message ID: {message.id}\n"
        f"Jump Link: {jump_link}\n"
        f"Content: {content_preview}\n"
        f"{'-' * 80}\n"
    )

    try:
        with open("toxxable_messages.log", "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        print(f"\033[91mLog failed: {e}\033[0m")

    color = "\033[92m" if reported else "\033[93m"
    print(f"{color}[TOXX] {status} | {keyword_matched} | {jump_link[:70]}...\033[0m")

sb_rl = {}
sb_rl_sec = 5

def sb_ratelimit(uid):
    now = time.time()
    if now - sb_rl.get(uid, 0) < sb_rl_sec:
        return True
    sb_rl[uid] = now
    return False

async def sb_fetch(url, json_mode=True, timeout=12):
    hdrs = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession() as s:
        try:
            async with s.get(url, headers=hdrs, timeout=timeout) as r:
                if r.status == 200:
                    return await r.json(content_type=None) if json_mode else await r.text()
        except:
            pass
    return None

async def run_selfbot():
    if not discord or not config.selfbot_enabled or not config.selfbot_token:
        print("\033[93m[Selfbot] Disabled or no token configured\033[0m")
        return

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=".", self_bot=True, intents=intents, help_command=None)
    
    stats = {
        "scanned": 0,
        "detected": 0,
        "reported": 0,
        "failed": 0,
        "started": None
    }

    @bot.event
    async def on_connect():
        config.selfbot_user = bot.user.name
        config.selfbot_guilds = len(bot.guilds)                                                                                                      
        try:
            friends = await bot.fetch_friends()
            config.selfbot_friends = len(friends)
        except:
            config.selfbot_friends = 0

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        
        if message.author.id == bot.user.id:
            await bot.process_commands(message)
            return
        
        stats["scanned"] += 1
        cl = message.content.lower()
        for kw in config.report_keywords:
            if kw.lower() in cl:
                stats["detected"] += 1
                ok = False
                try:
                    await message.report(reason="abuse_or_harassment")
                    stats["reported"] += 1
                    ok = True
                except Exception as e:
                    stats["failed"] += 1
                    print(f"\033[91m[Selfbot] Report fail: {e}\033[0m")
                log_toxxable_message(message, kw, reported=ok)
                break

    @bot.command(name="help")
    async def c_help(ctx):
        txt = """
OSINT Commands:
.email <email>     - Breach/rep check
.breach <email>    - HIBP lookup
.ip <ip>           - Geolocation
.revip <ip>        - Reverse IP
.ipwhois <ip>      - IP WHOIS
.port <ip> [ports] - Port scan
.user <name>       - Username search
.domain <dom>      - WHOIS
.sub <dom>         - Subdomains
.web <url>         - Website info
.phone <num>       - Phone lookup
.addr <address>    - Geocode
.btc <addr>        - BTC info
.hash <hash>       - Hash type
.paste <kw>        - Paste search
.leak <target>     - Leak check

Toxxer:
.lasttoxx          - Display toxxable msgs
.addkw <word>      - Add keyword
.rmkw <word>       - Remove keyword
.kws               - List keywords
.log               - Recent toxx msgs
.stats             - Selfbot stats
"""
        await ctx.send(f"```{txt}```")

    @bot.command(name="stats")
    async def c_stats(ctx):
        up = str(datetime.now() - stats["started"]).split(".")[0] if stats["started"] else "N/A"
        await ctx.send(f"```Scanned: {stats['scanned']}\nDetected: {stats['detected']}\nReported: {stats['reported']}\nFailed: {stats['failed']}\nUptime: {up}```")

    @bot.command(name="addkw")
    async def c_addkw(ctx, *, kw=None):
        if not kw:
            return await ctx.send("```.addkw <keyword>```")
        if kw.lower() not in [k.lower() for k in config.report_keywords]:
            config.report_keywords.append(kw.lower())
        await ctx.send(f"```Added: {kw}```")

    @bot.command(name="rmkw")
    async def c_rmkw(ctx, *, kw=None):
        if not kw:
            return await ctx.send("```.rmkw <keyword>```")
        config.report_keywords = [k for k in config.report_keywords if k.lower() != kw.lower()]
        await ctx.send(f"```Removed: {kw}```")

    @bot.command(name="kws")
    async def c_kws(ctx):
        kl = ", ".join(config.report_keywords) if config.report_keywords else "None"
        await ctx.send(f"```Keywords: {kl}```")

    @bot.command(name="log")
    async def c_log(ctx):
        try:
            if os.path.exists("toxxable_messages.log"):
                with open("toxxable_messages.log", "r", encoding="utf-8") as f:
                    lines = f.readlines()[-40:]
                txt = "".join(lines)[-1800:]
                await ctx.send(f"```{txt}```")
            else:
                await ctx.send("```No log yet```")
        except:
            await ctx.send("```Error reading log```")

    @bot.command(name="email")
    async def c_email(ctx, *, em=None):
        if not em:
            return await ctx.send("```.email someone@mail.com```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"Email: {em}"]
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{em}?truncateResponse=true", headers={"User-Agent": "sb"}) as r:
                    if r.status == 200:
                        br = await r.json()
                        out.append(f"HIBP: {len(br)} breaches")
                        if br:
                            out.append("Sites: " + ", ".join(b['Name'] for b in br[:8]))
                    elif r.status == 404:
                        out.append("HIBP: Clean")
        except:
            out.append("HIBP: Error")
        data = await sb_fetch(f"https://emailrep.io/{em}")
        if data:
            out.append(f"Rep: {data.get('reputation', '?')}")
        disp = ["tempmail", "mailinator", "guerrillamail", "10minutemail", "yopmail", "throwawaymail", "temp-mail", "disposablemail", "maildrop", "sharklasers", "guerrillamailblock", "spam4", "binkmail", "trashmail", "mailbox92", "dispostable", "mintemail", "getairmail", "tempinbox", "fakemailgenerator", "mailcatch", "tempail", "emailondeck", "mohmal", "mailtm", "tempmailo", "guerrillamail", "mailnesia", "mailguard", "discard.email", "mailbox.com", "inboxbear", "tempmail.plus", "mailpoof", "temp-mail.org", "getnada", "mail7", "temp-mail.ru", "emailfake", "mailforspam", "disposableinbox", "spamgourmet", "filzmail", "mailtothis", "my10minutemail", "tempmailaddress", "emailtemp", "tempemail", "temporarymail", "disposable.email"]
        dom = em.split("@")[-1].lower()
        out.append(f"Disposable: {'Yes' if any(d in dom for d in disp) else 'No'}")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.command(name="breach")
    async def c_breach(ctx, *, em=None):
        if not em:
            return await ctx.send("```.breach someone@mail.com```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"Breach: {em}"]
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{em}?truncateResponse=true", headers={"User-Agent": "sb"}) as r:
                    if r.status == 200:
                        br = await r.json()
                        out.append(f"Found: {len(br)}")
                        for b in br[:12]:
                            out.append(f"- {b['Name']}")
                    elif r.status == 404:
                        out.append("No breaches")
        except:
            out.append("Error")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.command(name="leak")
    async def c_leak(ctx, *, tgt=None):
        if not tgt:
            return await ctx.send("```.leak email@example.com```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"Leak: {tgt}"]
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{tgt}?truncateResponse=true", headers={"User-Agent": "sb"}) as r:
                    if r.status == 200:
                        br = await r.json()
                        out.append(f"HIBP: {len(br)} breaches")
                    else:
                        out.append("HIBP: None")
        except:
            out.append("HIBP: Error")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.command(name="lasttoxx")
    async def c_lasttoxx(ctx):
        try:
            with open("toxxable_messages.log", "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in reversed(lines):
                if "Jump Link:" in line:
                    link = line.split("Jump Link: ")[1].strip()
                    await ctx.send(f"Latest toxxable link: {link}")
                    return
            await ctx.send("No toxxable links found in log yet.")
        except:
            await ctx.send("Error reading log.")

    @bot.command(name="ip")
    async def c_ip(ctx, ip=None):
        if not ip:
            return await ctx.send("```.ip 8.8.8.8```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"IP: {ip}"]
        data = await sb_fetch(f"http://ip-api.com/json/{ip}")
        if data and data.get("status") == "success":
            out.extend([
                f"Country: {data.get('country', '?')} ({data.get('countryCode', '')})",
                f"City: {data.get('city', '?')}",
                f"Region: {data.get('regionName', '?')}",
                f"ISP: {data.get('isp', '?')}",
                f"Org: {data.get('org', '?')}",
                f"ASN: {data.get('as', '?')}",
                f"TZ: {data.get('timezone', '?')}",
                f"Coords: {data.get('lat', '?')}, {data.get('lon', '?')}",
                f"Proxy: {data.get('proxy', '?')}",
                f"Hosting: {data.get('hosting', '?')}"
            ])
        else:
            out.append("No data")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.event
    async def on_ready():
        stats["started"] = datetime.now()
        config.selfbot_user = bot.user.name
        config.selfbot_guilds = len(bot.guilds)
        try:
            friends = await bot.fetch_friends()
            config.selfbot_friends = len(friends)
        except:
            pass
        try:
            stream = discord.Streaming(name="FANTOXXER", url="https://twitch.tv")
            await bot.change_presence(activity=stream, status=discord.Status.dnd)
        except:
            pass

    @bot.command(name="revip")
    async def c_revip(ctx, ip=None):
        if not ip:
            return await ctx.send("```.revip 8.8.8.8```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"Reverse IP: {ip}"]
        txt = await sb_fetch(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", json_mode=False)
        if txt:
            doms = txt.splitlines()
            out.append(f"Found: {len(doms)}")
            for d in doms[:15]:
                out.append(f"- {d}")
            if len(doms) > 15:
                out.append("...")
        else:
            out.append("No data")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.command(name="ipwhois")
    async def c_ipwhois(ctx, ip=None):
        if not ip:
            return await ctx.send("```.ipwhois 8.8.8.8```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"IP WHOIS: {ip}"]
        data = await sb_fetch(f"https://ipwhois.app/json/{ip}")
        if data and data.get("success", False):
            out.extend([
                f"Country: {data.get('country', '?')}",
                f"Region: {data.get('region', '?')}",
                f"City: {data.get('city', '?')}",
                f"ISP: {data.get('isp', '?')}",
                f"Org: {data.get('org', '?')}",
                f"ASN: {data.get('asn', '?')}",
                f"TZ: {data.get('timezone', '?')}"
            ])
        else:
            out.append("No data")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.command(name="port")
    async def c_port(ctx, *, args=None):
        if not args:
            return await ctx.send("```.port 8.8.8.8 80,443```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        parts = args.split()
        ip = parts[0]
        ports = [80, 443, 22, 21, 25, 3389] if len(parts) == 1 else [int(p) for p in parts[1].split(",")]
        out = [f"Port scan: {ip}"]
        for p in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            res = sock.connect_ex((ip, p))
            out.append(f"  {p}: {'OPEN' if res == 0 else 'closed'}")
            sock.close()
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.command(name="user")
    async def c_user(ctx, uname=None):
        if not uname:
            return await ctx.send("```.user username```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        await ctx.send(f"```Searching '{uname}'...```")
        sites = {"GitHub":"https://github.com/{}", "Twitter/X":"https://x.com/{}", "Instagram":"https://www.instagram.com/{}/", "Reddit":"https://www.reddit.com/user/{}", "TikTok":"https://www.tiktok.com/@{}", "Twitch":"https://www.twitch.tv/{}", "YouTube":"https://www.youtube.com/@{}", "Steam":"https://steamcommunity.com/id/{}", "GitLab":"https://gitlab.com/{}", "Telegram":"https://t.me/{}", "Spotify":"https://open.spotify.com/user/{}", "SoundCloud":"https://soundcloud.com/{}", "Medium":"https://medium.com/@{}", "Patreon":"https://www.patreon.com/{}", "Pinterest":"https://www.pinterest.com/{}/", "Behance":"https://www.behance.net/{}", "DeviantArt":"https://www.deviantart.com/{}", "Vimeo":"https://vimeo.com/{}", "Flickr":"https://www.flickr.com/people/{}", "500px":"https://500px.com/{}", "About.me":"https://about.me/{}", "Roblox":"https://www.roblox.com/users/profile?username={}", "CashApp":"https://cash.app/${}", "Venmo":"https://venmo.com/{}", "PayPal":"https://www.paypal.com/paypalme/{}"}
        found = []
        async with aiohttp.ClientSession() as s:
            for site, url in sites.items():
                try:
                    async with s.head(url, allow_redirects=True, timeout=4) as r:
                        if r.status == 200:
                            found.append(f"{site}: {url}")
                except:
                    pass
        out = [f"User: {uname}"]
        if found:
            out.extend(found)
        else:
            out.append("None found")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

    @bot.command(name="domain")
    async def c_domain(ctx, dom=None):
        if not dom:
            return await ctx.send("```.domain example.com```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"Domain: {dom}"]
        try:
            w = whois.whois(dom)
            out.extend([
                f"Registrar: {w.registrar}",
                f"Created: {w.creation_date}",
                f"Expires: {w.expiration_date}",
                f"NS: {', '.join(w.name_servers) if w.name_servers else 'N/A'}",
                f"Org: {w.org}",
                f"Country: {w.country}"
            ])
        except Exception as e:
            out.append(f"Error: {str(e)[:80]}")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.command(name="sub")
    async def c_sub(ctx, dom=None):
        if not dom:
            return await ctx.send("```.sub example.com```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"Subdomains: {dom}"]
        data = await sb_fetch(f"https://crt.sh/?q=%.{dom}&output=json")
        if data:
            subs = set()
            for e in data:
                n = e.get('name_value')
                if n:
                    subs.add(n.strip('*').strip('.'))
            out.append(f"Found: {len(subs)}")
            for s in list(subs)[:25]:
                out.append(f"- {s}")
            if len(subs) > 25:
                out.append("...")
        else:
            out.append("No data")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.command(name="web")
    async def c_web(ctx, url=None):
        if not url:
            return await ctx.send("```.web https://example.com```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"Web: {url}"]
        try:
            r = requests.get(url, timeout=8)
            out.append(f"Status: {r.status_code}")
            if r.status_code == 200:
                out.append(f"Length: {len(r.text)}")
                m = re.search('<title>(.*?)</title>', r.text, re.IGNORECASE)
                if m:
                    out.append(f"Title: {m.group(1)[:80]}")
                out.append(f"Server: {r.headers.get('Server', 'N/A')}")
        except Exception as e:
            out.append(f"Error: {str(e)[:60]}")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.command(name="phone")
    async def c_phone(ctx, num=None):
        if not num:
            return await ctx.send("```.phone +12025550123```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"Phone: {num}"]
        try:
            pn = phonenumbers.parse(num)
            if phonenumbers.is_valid_number(pn):
                    out.extend(["Valid: Yes",f"Country: {geocoder.description_for_number(pn, 'en')}",f"Carrier: {carrier.name_for_number(pn, 'en') or '?'}",f"Type: {'Mobile' if number_type(pn) == PhoneNumberType.MOBILE else 'Other'}",f"Intl: {phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}"])
            else:
                    out.append("Valid: No")
        except Exception as e:
            out.append(f"Error: {str(e)[:60]}")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.command(name="addr")
    async def c_addr(ctx, *, addr=None):
        if not addr:
            return await ctx.send("```.addr 1600 Pennsylvania Ave```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"Address: {addr}"]
        data = await sb_fetch(f"https://nominatim.openstreetmap.org/search?q={addr}&format=json&limit=1")
        if data:
            loc = data[0]
            out.extend([
                f"Display: {loc.get('display_name', '?')[:100]}",
                f"Coords: {loc.get('lat')}, {loc.get('lon')}",
                f"Type: {loc.get('type', '?')}"
            ])
        else:
            out.append("No data")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.command(name="btc")
    async def c_btc(ctx, addr=None):
        if not addr:
            return await ctx.send("```.btc 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"BTC: {addr}"]
        data = await sb_fetch(f"https://blockchain.info/rawaddr/{addr}")
        if data:
            out.extend([
                f"Received: {data['total_received'] / 1e8:.8f} BTC",
                f"Sent: {data['total_sent'] / 1e8:.8f} BTC",
                f"Balance: {data['final_balance'] / 1e8:.8f} BTC",
                f"Tx: {data['n_tx']}"
            ])
        else:
            out.append("No data")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    @bot.command(name="hash")
    async def c_hash(ctx, h=None):
        if not h:
            return await ctx.send("```.hash 5f4dcc3b5aa765d61d8327deb882cf99```")
        hl = len(h)
        types = {32: "MD5/NTLM", 40: "SHA1", 64: "SHA256", 128: "SHA512"}
        await ctx.send(f"```Hash: {h}\nLength: {hl}\nType: {types.get(hl, 'Unknown')}```")

    @bot.event
    async def on_message_edit(before, after):
        if after.author.bot or after.author.id == bot.user.id:
            return
        cl = after.content.lower()
        for kw in config.report_keywords:
            if kw.lower() in cl:
                stats["detected"] += 1
                ok = False
                try:
                    await after.report(reason="abuse_or_harassment")
                    stats["reported"] += 1
                    ok = True
                except:
                    stats["failed"] += 1
                log_toxxable_message(after, kw + " [EDIT]", reported=ok)
                break

    @bot.command(name="paste")
    async def c_paste(ctx, *, kw=None):
        if not kw:
            return await ctx.send("```.paste keyword```")
        if sb_ratelimit(ctx.author.id):
            return await ctx.send("```Rate limited```")
        out = [f"Paste: {kw}"]
        data = await sb_fetch(f"https://psbdmp.cc/api/search/{kw}")
        if data and len(data) > 0:
            out.append(f"Found: {len(data)}")
            for p in data[:5]:
                out.append(f"ID: {p.get('id')} - {p.get('text', '')[:35]}...")
        else:
            out.append("None found")
        await ctx.send("```\n" + "\n".join(out) + "\n```")

    try:
        await bot.start(config.selfbot_token, bot=False)
    except discord.LoginFailure:
        print("\033[91m[Selfbot] Invalid token\033[0m")
    except discord.HTTPException as e:
        print(f"\033[91m[Selfbot] HTTP error: {e}\033[0m")
    except Exception as e:
        print(f"\033[91m[Selfbot] Failed: {e}\033[0m")

def start_self():
    def run_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(run_selfbot())
        except Exception as e:
            print(f"\033[91m[Selfbot] Thread error: {e}\033[0m")
        finally:
            loop.close()
    selfbot_thread = threading.Thread(target=run_in_thread, daemon=True)
    selfbot_thread.start()
    print("\033[96m[Selfbot] Started in background thread\033[0m")
    return selfbot_thread

def toxxable_scraper_menu():
    clear_screen()
    print("\033[96m=== TOXXABLE MESSAGES SCRAPER ===\033[0m\n")
    print("This uses the selfbot to scan recent messages in visible channels.")
    print("It logs messages matching keywords to toxxable_scraped.log")
    print("WARNING: Only use on servers you own/control — mass scanning is detectable.\n")

    if not config.selfbot_enabled or not config.selfbot_token:
        print("\033[91mSelfbot is not enabled or no token set.\033[0m")
        print("Enable it in [5] CONFIGURATION MENU first.\n")
        input("Press ENTER to return...")
        return

    mode = input("Scan mode? (c=channel / g=guild / k=keyword search / q=quit): ").lower().strip()
    if mode == 'q':
        return

    limit = input("How many recent messages per channel? (default 100, max 500): ").strip()
    try:
        limit = min(500, max(50, int(limit or 100)))
    except:
        limit = 100

    print(f"\nScanning with limit {limit} messages per channel...\n")

    async def scrape_toxxables():
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True

        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print(f"\033[92m[Scraper] Connected as {client.user}\033[0m")
            found = 0

            if mode == 'c':
                channel_id = input("Enter channel ID: ").strip()
                try:
                    channel = await client.fetch_channel(int(channel_id))
                    print(f"Scanning #{channel.name}...")
                    async for msg in channel.history(limit=limit):
                        if any(kw.lower() in msg.content.lower() for kw in config.report_keywords):
                            log_toxxable_message(msg, "SCRAPED", reported=False)
                            found += 1
                except Exception as e:
                    print(f"\033[91mError: {e}\033[0m")

            elif mode == 'g':
                guild_id = input("Enter guild/server ID: ").strip()
                try:
                    guild = await client.fetch_guild(int(guild_id))
                    print(f"Scanning guild: {guild.name} ({len(guild.text_channels)} text channels)...")
                    for channel in guild.text_channels:
                        if not channel.permissions_for(guild.me).read_messages:
                            continue
                        print(f" → #{channel.name}")
                        try:
                            async for msg in channel.history(limit=limit//10):  
                                if any(kw.lower() in msg.content.lower() for kw in config.report_keywords):
                                    log_toxxable_message(msg, "SCRAPED", reported=False)
                                    found += 1
                        except:
                            pass
                except Exception as e:
                    print(f"\033[91mError: {e}\033[0m")

            elif mode == 'k':
                custom_kw = input("Enter custom keyword to search: ").strip()
                if not custom_kw:
                    print("No keyword entered.")
                    return
                print(f"Searching for '{custom_kw}' across visible channels...")
                for guild in client.guilds:
                    for channel in guild.text_channels:
                        if not channel.permissions_for(guild.me).read_messages:
                            continue
                        try:
                            async for msg in channel.history(limit=limit//20):
                                if custom_kw.lower() in msg.content.lower():
                                    log_toxxable_message(msg, custom_kw, reported=False)
                                    found += 1
                        except:
                            pass

            print(f"\n\033[92mScan complete. Found {found} matching messages.\033[0m")
            print("Logged to: toxxable_scraped.log")
            await client.close()

        try:
            await client.start(config.selfbot_token, bot=False)
        except Exception as e:
            print(f"\033[91mScraper failed: {e}\033[0m")

    asyncio.run(scrape_toxxables())
    input("\nPress ENTER to return to main menu...")

def log_toxxable_scraped(message, keyword, reported=False):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "REPORTED" if reported else "SCRAPED"
    guild = message.guild.name if message.guild else "DM"
    channel = getattr(message.channel, 'name', 'DM')
    author = f"{message.author} ({message.author.id})"
    content = message.content.replace('\n', ' ').strip()[:300] + ('...' if len(message.content) > 300 else '')
    jump = f"https://discord.com/channels/{message.guild.id if message.guild else '@me'}/{message.channel.id}/{message.id}"
    
    entry = f"[{ts}] [{status}] {keyword} | Guild: {guild} | Ch: #{channel} | Author: {author} | MsgID: {message.id} | Content: {content} | Link: {jump}\n{'-'*100}\n"
    
    with open("toxxable_scraped.log", "a", encoding="utf-8") as f:
        f.write(entry)

def main():
    config.load_tokens()
    config.load_proxies()
    
    selfbot_thread = None
    if config.selfbot_enabled:
        selfbot_thread = start_self()

    while True:
        print_header(
            len(config.tokens),
            config.reports_success + config.reports_failed,
            config.current_reason
        )

        try:
            choice = input().strip().lower()
        except KeyboardInterrupt:
            print("\n\033[91mEXITING...\033[0m")
            sys.exit(0)

        if choice in ('q', 'quit', 'exit'):
            clear_screen()
            print("\n" * 5)
            print(" " * 28 + rgb(*config.theme.accent) + "SHUTTING DOWN...\033[0m")
            time.sleep(1.2)
            clear_screen()
            break

        elif choice == '1':
            single_report_classic()
        elif choice == '2':
            mass_report()
        elif choice == '3':
            config.load_tokens()
        elif choice == '4':
            config.load_proxies()
        elif choice == '5':
            config_menu()
        elif choice == '6':
            show_stats()
        elif choice == '7':
            validate_tokens_menu()
        elif choice == '8':
            theme_customizer()
        elif choice == '9':
            clear_screen()
            print("\033[96m=== PROXY SCRAPER & TESTER ===\033[0m\n")
            print("This will:")
            print("  • Scrape from public sources (HTTP + SOCKS5)")
            print("  • Test against Discord API")
            print("  • Save working ones to proxies.txt\n")
            if input("Start scraping? (y/n): ").lower() == 'y':
                scrape_proxies()
            input("\nPress ENTER to continue...")
        elif choice == '10':
            toxxable_scraper_menu()
        elif choice == '12':
            profile_report_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[91mForced exit\033[0m")
