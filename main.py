┏━「 ⚡ KASHYAP USERBOT — ALL COMMANDS ⚡ 」━┓
┃
┃ [ BOT & HOSTING ]
┃ • /start • /login • /welcome [text]
┃
┃ [ RAID & SPAM ]
┃ • .raid [count] • .oneraid [count] • .rraid • .drraid
┃ • .spam [count] [text] • .fastspam [count] [text] • .flood [count] [text]
┃ • .engraid [count] • .praid [count] • .braid [count]
┃ • .araid • .saraid • .oaraid • .faraid • .earaid
┃ • .dmraid [count] • .mraid [count] • .delayraid [sec] [count]
┃ • .emoraid [count] • .emojispam [count] [emoji] [text]
┃ • .mixraid [1-50] • .tagraid [1-50] • .capsraid [1-50] • .slowraid [1-50]
┃ • .badaid [count] • .saraid2 [count] • .ultraid [count]
┃
┃ [ HACK & ANIMATION ]
┃ • .hack • .matrix • .scan
┃ • .bruteforce [1-50] • .packetflood [1-50] • .sysbreach [1-50]
┃ • .loading • .boom • .fbi
┃ • .pulse [1-50] • .countanim [1-50] • .glitch [1-50]
┃
┃ [ GROUP, ADMIN & AUTOPIN ]
┃ • .ban • .unban • .kick • .mute • .unmute
┃ • .pin • .unpin • .del • .invite
┃ • .autopin on <id> • .autopin off <id>
┃ • .dmautopin on <t> • .dmautopin off <t>
┃ • .tagall [text] • .admins • .bots
┃
┃ [ DM, REACT & CONTROL ]
┃ • .dmblock on|off • .dmmute • .undmmute
┃ • .ar [emoji] • .dar • .uar • .duar • .rar [emojis...] • .drar
┃ • .stop • .stopall • .clear • .restart • .help
┃
┃ [ FUN, TEXT & UTILITY ]
┃ • .roast • .iq • .love • .toss • .dice • .coin • .rate [topic]
┃ • .calc [expr] • .type [text] • .mock [text]
┃ • .reverse [text] • .clap [text] • .vapor [text]
┃ • .trim [text] • .caps [text] • .lower [text] • .title [text]
┃ • .ship • .slap • .hug • .8ball [question] • .fact • .shayari
┃ • .ping • .alive • .id • .info • .whois • .chatinfo • .stats
┃ • .time • .date • .afk [reason] • .save
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
➤ POWERED BY » KASHYAP USERBOT
```[cite: 2, 7, 8]

---

### Poora Updated `main.py` (Sabhi Commands & Features Ke Saath)

```python
import os
import sys
import json
import time
import asyncio
import random
import re
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"KASHYAP USERBOT is Live!")
    def log_message(self, *a):
        pass

def run_web():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), H).serve_forever()

threading.Thread(target=run_web, daemon=True).start()

# ==========================================
# KASHYAP USERBOT & HOSTING BOT (FULL STATIC EDITION)
# OWNER: KASHYAP (9239452757)
# ==========================================

try:
    import telethon
except ImportError:
    os.system(f"{sys.executable} -m pip install telethon")
    import telethon

from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PhoneNumberInvalidError, FloodWaitError
from telethon.tl.functions.messages import SendReactionRequest, ExportChatInviteRequest
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.types import ReactionEmoji, ChannelParticipantsAdmins, ChannelParticipantsBots

# CONFIGURATION
API_ID = 39105091
API_HASH = "257594e70a9926b6bb44644e17be94a9"
BOT_TOKEN = "9241124031:AAFa6bpjJSq_gGhYgRDqrxjEbFcvsZiYcl4"
OWNER_ID = 9239452757
OWNER_NAME = "KASHYAP"
BOT_BRAND = "KASHYAP USERBOT"
START_TIME = time.time()
SESSIONS_FILE = "sessions.json"
START_BANNER_PATH = "photo_2026-11-25_14-19-14.jpg"

def format_uptime():
    sec = int(time.time() - START_TIME)
    days, sec = divmod(sec, 86400)
    hours, sec = divmod(sec, 3600)
    mins, secs = divmod(sec, 60)
    return f"{days}d {hours:02d}:{mins:02d}:{secs:02d}"

# STATIC COMMANDS MENU (FIXED LAYOUT — ALL COMMANDS INCLUDED)
STATIC_COMMANDS_TEXT = (
    "┏━「 ⚡ **KASHYAP USERBOT — ALL COMMANDS** ⚡ 」━┓\n"
    "┃\n"
    "┃ **[ BOT & HOSTING ]**\n"
    "┃ • `/start` • `/login` • `/welcome [text]`\n"
    "┃\n"
    "┃ **[ RAID & SPAM ]**\n"
    "┃ • `.raid [count]` • `.oneraid [count]` • `.rraid` • `.drraid`\n"
    "┃ • `.spam [count] [text]` • `.fastspam [count] [text]` • `.flood [count] [text]`\n"
    "┃ • `.engraid [count]` • `.praid [count]` • `.braid [count]`\n"
    "┃ • `.araid` • `.saraid` • `.oaraid` • `.faraid` • `.earaid`\n"
    "┃ • `.dmraid [count]` • `.mraid [count]` • `.delayraid [sec] [count]`\n"
    "┃ • `.emoraid [count]` • `.emojispam [count] [emoji] [text]`\n"
    "┃ • `.mixraid [1-50]` • `.tagraid [1-50]` • `.capsraid [1-50]` • `.slowraid [1-50]`\n"
    "┃ • `.badaid [count]` • `.saraid2 [count]` • `.ultraid [count]`\n"
    "┃\n"
    "┃ **[ HACK & ANIMATION ]**\n"
    "┃ • `.hack` • `.matrix` • `.scan`\n"
    "┃ • `.bruteforce [1-50]` • `.packetflood [1-50]` • `.sysbreach [1-50]`\n"
    "┃ • `.loading` • `.boom` • `.fbi`\n"
    "┃ • `.pulse [1-50]` • `.countanim [1-50]` • `.glitch [1-50]`\n"
    "┃\n"
    "┃ **[ GROUP, ADMIN & AUTOPIN ]**\n"
    "┃ • `.ban` • `.unban` • `.kick` • `.mute` • `.unmute`\n"
    "┃ • `.pin` • `.unpin` • `.del` • `.invite`\n"
    "┃ • `.autopin on <id>` • `.autopin off <id>`\n"
    "┃ • `.dmautopin on <t>` • `.dmautopin off <t>`\n"
    "┃ • `.tagall [text]` • `.admins` • `.bots`\n"
    "┃\n"
    "┃ **[ DM, REACT & CONTROL ]**\n"
    "┃ • `.dmblock on|off` • `.dmmute` • `.undmmute`\n"
    "┃ • `.ar [emoji]` • `.dar` • `.uar` • `.duar` • `.rar [emojis...]` • `.drar`\n"
    "┃ • `.stop` • `.stopall` • `.clear` • `.restart` • `.help`\n"
    "┃\n"
    "┃ **[ FUN, TEXT & UTILITY ]**\n"
    "┃ • `.roast` • `.iq` • `.love` • `.toss` • `.dice` • `.coin` • `.rate [topic]`\n"
    "┃ • `.calc [expr]` • `.type [text]` • `.mock [text]`\n"
    "┃ • `.reverse [text]` • `.clap [text]` • `.vapor [text]`\n"
    "┃ • `.trim [text]` • `.caps [text]` • `.lower [text]` • `.title [text]`\n"
    "┃ • `.ship` • `.slap` • `.hug` • `.8ball [question]` • `.fact` • `.shayari`\n"
    "┃ • `.ping` • `.alive` • `.id` • `.info` • `.whois` • `.chatinfo` • `.stats`\n"
    "┃ • `.time` • `.date` • `.afk [reason]` • `.save`\n"
    "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
    "➤ **POWERED BY » KASHYAP USERBOT**"
)

# ONE-WORD HEAVY GAALI & INSULT DATABASE
RAW_BASE_GAALIS = [
    "MADARCHOD", "GAANDU", "CHUTIYA", "BHADWA", "RANDI",
    "LUND", "HIJDA", "CHHAKKA", "SUAR", "KAMINEY",
    "KANJAR", "HARAMKHOR", "BESHARM", "CHUTMARIKE", "LODU",
    "CHHINAR", "KAMJAT", "BHAND", "TAPORI", "GADDAR",
    "LAVDE", "KUTTA", "BALLU", "DHakkan", "CHUTMARIKA",
    "BAYMAN", "NALAYAK", "ULRAG", "FARIA", "CHAMPAN",
    "BEGHARAT", "KAMINE", "CHALBAZ", "KASAI", "GHATIYA"
]

SINGLE_GAALIS = [
    "MADARCHOD", "BHOOTNIKE", "CHUTIYE", "GANDU", "RANDI",
    "LODE", "BHOSDIKE", "LAWDE", "HIJRA", "MC", "BC",
    "TERIMA", "CHUT", "HRAMKHOR", "NALAYAK", "BAKKANCHOD"
]

ENGLISH_RAIDS = [
    "YOU ARE A TOTAL CLOWN KNOW YOUR PLACE BEFORE SPEAKING",
    "SIT DOWN KID YOUR WHOLE ARGUMENT IS PURE TRASH",
    "STOP BARKING LIKE A STRAY DOG NOBODY CARES ABOUT YOU",
    "YOU EMBARRASS YOURSELF EVERY TIME YOU OPEN YOUR MOUTH",
    "HOLD THIS L AND WALK AWAY QUIETLY FOOL",
    "PURE JOKE ENERGY FROM START TO FINISH"
]

PUNJABI_RAIDS = [
    "TERI MAA DI LUN VICH SOOTA PA DU MADARCHODA AUKAT CH REH",
    "BHOSDIKEYA TERI BHEN DI LUN VICH RICKSHAW CHALA DU KUTTEYA",
    "RANDI DE PUTTAR TERE PYO NU DASSDA AA TERI MAA DI LUN VICH DANDA",
    "CHUTIYA SALEYA APNI AUKAT VEKH LE TERI MAA DI LUN CH PAANI PA DU",
    "KUTTEY DE BACCHEYA TERA KHANDAN HI NALAYAK AA BHOSDIKEYA",
    "TERI MAA DI LUN VICH GARM LOHA PA DU MADARCHOD SALEYA",
    "BHOSDIKEYA BHAJJA YAHA TON TERI BHEN DI LUN VICH PHATAKA PA DU"
]

BENGALI_RAIDS = [
    "TOR PAYA KHA BOKACHODA NIZZER AUKAT BUJHE KATHA BOL",
    "MAGIR PO BESHYA TOR BUKER UPOR DIYE GARI CHALIYE DEBO",
    "CHODNA TOR MUKH BANDH RAKH KUKURER MOTO GHEU GHEU KORIS NA",
    "KHANKIR CHELE TOR BHAAT CHOR AUKAT SOBEI JANE",
    "TOR GAND MERE LAL KORE DEBO BOKACHODA SALA",
    "BESHYAR BACCHA BESHI PAKAMI KORIS NA EKHANE"
]

MULTI_LINE_RAIDS = [
    "TERI AUKAT ZERO HAI BHAI\nPEHLE APNE LEVEL PAR AA\nFIR BAAT KARNA",
    "SHOR KAM KAR AUR KAAM DEKH\nTERI HAR BAAT ME DAM NAHI\nNIKAL LE YAHA SE"
]

SCREENSHOT_AND_EXTRA_RAIDS = [
    "TERI VAHEN KE BHOSDIKE MEI BESAN KE LADDU",
    "ACE TERII MUMMY KE BOSHDE KI HADIYAA TOD DUNGAA",
    "TERI MAA KE SATH SUAR KA SEX KARWA DUNGAA EK SATH 6-6 BACHE DEGI 💰 🔥 😱",
    "TOHAR BAHIN CHODU BBAHEN KE LAWDE USME MITTI DAL KE CEMENT SE BHAR DU 🏠 🤢 😡 💥",
    "TERI MAA KE BHOSDE MEI GITHUB DAL KE APNA BOT HOST KARUNGAA 😂 👊 🙎 😍",
    "TERI MUMMY AUR BAHEN KO DAUDA DAUDA NE CHODUNGA UNKE NO BOLNE PE BHI LAND GHUSA DUNGA ANDER TAK 😎 😎 😂 🔥",
    "TERI HAR BAKWAS KA JAWAB SEEDHA MUH PAR MILEGA AUKAT ME REH",
    "ITNA BOLNE SE PEHLE APNI VALUE DEKH LE JO ZERO HAI",
    "SHOR MACHANE SE KUCH NAHI HOGA APNE LEVEL PAR AA PEHLE",
    "TERI AUKAT SIRF SUNNE KI HAI BOLNE KI NAHI",
    "HAR BAAR KHARED KAR BECH DENGE TERE JAISE NAAMON KO",
    "APNI HAD ME REH KAR BAAT KAR WARNA ZAMEEN ME MIL JAYEGA",
    "TERA PURA GROUP MIL KAR BHI MUQABLA NAHI KAR SAKTA",
    "BAKWAAS BAND KAR AUR APNA RASTA NAAP",
    "TERE JAISE LOG ROZ AATE HAIN AUR ROZ DHUL CHAAT TE HAIN",
    "AWAZ NEECHI RAKH AUR APNI AUKAT YAAD RAKH"
]

ROAST_LINES = [
    "Baatein aisi kar rahe ho jaise signal 1 bar pe atka ho.",
    "Confidence solid hai, bas points thode aur le aao.",
    "Aapki argument bilkul zero-watt bulb jaisi lag rahi hai.",
    "Bolne se pehle ek baar mic check kar liya karo."
]

RAID_EMOJIS = ["💀", "🔥", "🤡", "⚡", "😈", "💣", "🧨", "👁️"]

# Expanding dynamically to 1000+ heavy single-word variants
GAALIS = []
modifiers = ["VALA", "SALE", "KAMINEY", "BHADWE", "MADARCHOD", "GAANDU", "CHUTIYE", "HARAMKHOR", "KAMJAT", "CHHINAR"]
for g in RAW_BASE_GAALIS:
    GAALIS.append(g)
    for m in modifiers:
        GAALIS.append(f"{g} {m}")
        GAALIS.append(f"{m} {g}")
GAALIS.extend(ENGLISH_RAIDS)
GAALIS.extend(PUNJABI_RAIDS)
GAALIS.extend(BENGALI_RAIDS)
GAALIS.extend(SCREENSHOT_AND_EXTRA_RAIDS)
while len(GAALIS) < 1200:
    GAALIS.extend(RAW_BASE_GAALIS)

EARAID_LIST = [
    "💀MADARCHOD", "🔥GAANDU", "🤡CHUTIYA", "⚡BHADWA", "😈RANDI",
    "💣LUND", "🧨HIJDA", "💀CHHAKKA", "🔥SUAR", "🤡KAMINEY", "⚡KANJAR"
] * 100

# SESSION PERSISTENCE HELPERS
def load_saved_sessions():
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}

def save_sessions_to_disk(data: dict):
    try:
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving sessions: {e}")

# FONT FORMATTERS
def format_araid(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    bold = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"
    return text.upper().translate(str.maketrans(normal, bold))

def format_saraid(word):
    emojis = ["💀", "🔥", "🤡", "⚡", "😈", "💣", "🧨", "👁️", "💢", "🖤", "🌪️"]
    res = []
    for char in word.upper():
        if char.isalpha():
            rep = "".join([char for _ in range(5)])
            res.append(f"*{rep}{random.choice(emojis)}*")
        else:
            res.append(char)
    return "".join(res)

def format_oaraid(text):
    mapping = {'A':'🅐','B':'🅑','C':'C','D':'🅓','E':'🅔','F':'🅕','G':'🅖','H':'H','I':'🅘','J':'🅙','K':'🅚','L':'🅛','M':'🅜','N':'N','O':'🅞','P':'P','Q':'Q','R':'R','S':'🅢','T':'🅣','U':'🅤','V':'🅥','W':'🅦','X':'🅧','Y':'🅨','Z':'Z'}
    return "".join([mapping.get(c, c) for c in text.upper()])

def format_faraid(text):
    res = []
    for c in text.upper():
        if 'A' <= c <= 'Z':
            code = ord(c) - ord('A')
            res.append(chr(0x1F1E6 + code) + '\u034f')
        else:
            res.append(c)
    return "".join(res)

# IN-MEMORY STATES
user_sessions = load_saved_sessions()
active_logins = set()
active_raids = set()
active_raid_tasks = {}       # chat_id: asyncio.Task
rraid_targets = set()        # (chat_id, user_id)
self_reacts = {}             # chat_id: emoji (for .ar)
user_react_targets = {}      # chat_id: set of user_ids (for .uar)
all_reacts = {}              # chat_id: [emojis] (for .rar)
chat_welcomes = {}           # chat_id: {'text': str, 'media': file}
dm_block_enabled = {}        # owner_id: bool
dm_muted_users = {}          # owner_id: set of user_ids
afk_status = {}              # owner_id: str (reason)
autopin_chats = set()        # chat_id jahan group/chat auto-pin on hai
dm_autopin_targets = set()   # user_id jahan DM auto-pin on hai

# INITIALIZE BOT CLIENT (HOSTING PANEL)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
bot = TelegramClient('host_bot_session', API_ID, API_HASH, loop=loop).start(bot_token=BOT_TOKEN)

def build_home_card():
    text = (
        "┏━「 ⚡ **INFORMATION** ⚡ 」━┓\n"
        f"┃ • **HEY, {BOT_BRAND} IS LIVE!**\n"
        f"┃ • **OWNER: {OWNER_NAME}**\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"➤ **UPTIME:** `{format_uptime()}`\n"
        "➤ **SERVER STATUS:** `ONLINE / STATIC`\n"
        f"➤ **POWERED BY » {BOT_BRAND}**"
    )
    buttons = [
        [Button.inline("「 HELP & COMMAND 」", b"help_cmd")],
        [Button.inline("「 WEBSITE 」", b"about"), Button.inline("「 SUPPORT 」", b"guide")],
        [Button.inline("「 HELP 」", b"source"), Button.inline("「 MY HOME 」", b"my_home")],
        [Button.inline("「 LOGIN USERBOT 」", b"host_login")]
    ]
    return text, buttons

async def send_home_card(event):
    text, buttons = build_home_card()
    if START_BANNER_PATH and os.path.exists(START_BANNER_PATH):
        await event.respond(text, file=START_BANNER_PATH, buttons=buttons)
    else:
        await event.respond(text, buttons=buttons)

@bot.on(events.NewMessage(pattern=r'^/(start|login)$'))
async def start_handler(event):
    if event.raw_text.strip().lower() == "/login":
        await host_login_cb(event)
        return
    await send_home_card(event)

@bot.on(events.CallbackQuery(data=b'my_home'))
async def my_home_cb(event):
    await event.answer("Home panel refreshed.", alert=False)
    await send_home_card(event)

@bot.on(events.CallbackQuery(data=b'about'))
async def about_cb(event):
    await event.answer(f"{BOT_BRAND} — Clean Static Commands & Hosting Panel", alert=True)

@bot.on(events.CallbackQuery(data=b'owner'))
async def owner_cb(event):
    await event.answer(f"Owner: {OWNER_NAME}\nUser ID: {OWNER_ID}", alert=True)

@bot.on(events.CallbackQuery(data=b'guide'))
async def guide_cb(event):
    await event.answer(
        "1. 「 LOGIN USERBOT 」 dabayein\n"
        "2. Phone number (+91...) bhejein\n"
        "3. OTP aur 2FA (agar ho) daalein",
        alert=True
    )

@bot.on(events.CallbackQuery(data=b'source'))
async def source_cb(event):
    await event.answer(f"{BOT_BRAND} — Private Static Edition", alert=True)

@bot.on(events.CallbackQuery(data=b'help_cmd'))
async def help_cb(event):
    sender_id = event.sender_id
    is_hosted = (str(sender_id) in user_sessions) or (sender_id in user_sessions) or (sender_id == OWNER_ID)

    if not is_hosted:
        await event.answer("🔒 Pehle LOGIN USERBOT se apna account host karein!", alert=True)
        await event.respond(
            "┏━「 🔒 **ACCESS LOCKED** 」━┓\n"
            "┃ • **COMMANDS LOCKED HAIN!**\n"
            "┃ • **PEHLE LOGIN USERBOT KAREIN**\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
        )
        return

    await event.answer("Static commands list ready.", alert=False)
    await event.respond(STATIC_COMMANDS_TEXT)

@bot.on(events.CallbackQuery(data=b'host_login'))
async def host_login_cb(event):
    sender_id = event.sender_id
    if sender_id in active_logins:
        if hasattr(event, "answer"):
            await event.answer("⚠️ Ek login process pehle se chal raha hai!", alert=True)
        await event.respond(
            "┏━「 ⚠️ **ALREADY ACTIVE** 」━┓\n"
            "┃ • ❌ **EK LOGIN PROCESS PEHLE SE CHAL RAHA HAI!**\n"
            "┃ • ⏳ **KRIPYA USE PURA KAREIN YA KUCH DER BAAD TRY KAREIN.**\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
        )
        return

    active_logins.add(sender_id)
    if hasattr(event, "answer"):
        await event.answer("Secure login panel opened.", alert=False)

    try:
        async with bot.conversation(sender_id, timeout=180) as conv:
            await conv.send_message(
                "┏━「 🔐 **SECURE LOGIN PANEL** 」━┓\n"
                "┃ • 📱 **SEND YOUR PHONE NUMBER**\n"
                "┃ • ➤ `+91XXXXXXXXXX`\n"
                "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
            )
            phone_msg = await conv.get_response()
            phone = phone_msg.text.strip()

            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()

            try:
                sent = await client.send_code_request(phone)
            except Exception as e:
                await conv.send_message(f"❌ **Code bhejne mein dikkat aayi:** `{e}`")
                await client.disconnect()
                return

            await conv.send_message("📩 **OTP bhej diya gaya hai.** Kripya Telegram par aaya OTP code bhejein:")
            code_msg = await conv.get_response()
            code = "".join(code_msg.text.split())

            try:
                await client.sign_in(phone, code, phone_code_hash=sent.phone_code_hash)
            except SessionPasswordNeededError:
                await conv.send_message("🔐 **2-Step Verification active hai.** Kripya apna password bhejein:")
                pwd_msg = await conv.get_response()
                password = pwd_msg.text.strip()
                try:
                    await client.sign_in(password=password)
                except Exception as e:
                    await conv.send_message(f"❌ **2FA password galat hai:** `{e}`")
                    await client.disconnect()
                    return
            except Exception as e:
                await conv.send_message(f"❌ **Login safal nahi ho saka:** `{e}`")
                await client.disconnect()
                return

            session_str = client.session.save()
            user_sessions[str(sender_id)] = session_str
            save_sessions_to_disk(user_sessions)

            asyncio.create_task(start_userbot_session(session_str, sender_id))

            await conv.send_message(
                "┏━「 ✅ **HOSTING COMPLETE** 」━┓\n"
                f"┃ • **BOT: {BOT_BRAND}**\n"
                f"┃ • **OWNER: {OWNER_NAME}**\n"
                "┃ • **HELP & COMMAND UNLOCKED!**\n"
                "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
            )
    except asyncio.TimeoutError:
        await bot.send_message(
            sender_id,
            "┏━「 ⏱️ **SESSION EXPIRED** 」━┓\n"
            "┃ • ⚠️ **LOGIN SESSION EXPIRE HO GAYA!**\n"
            "┃ • 📌 **AAPNE SAMAY PAR NUMBER YA OTP NAHI BHEJA.**\n"
            "┃ • 🔄 **DOBARA LOGIN KARNE KE LIYE /LOGIN DALEIN.**\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
        )
    finally:
        active_logins.discard(sender_id)

# DYNAMIC USERBOT SESSION RUNNER
async def start_userbot_session(session_string, owner_id):
    ubot = TelegramClient(StringSession(session_string), API_ID, API_HASH)
    dm_muted_users.setdefault(owner_id, set())

    # WELCOME FEATURE: SET WELCOME WITH PIC & TEXT
    @ubot.on(events.NewMessage(outgoing=True, pattern=r'^\/welcome'))
    async def set_welcome_handler(event):
        chat_id = event.chat_id
        text_arg = event.raw_text.replace('/welcome', '').strip()

        if event.is_reply:
            reply = await event.get_reply_message()
            text = text_arg or (reply.text if reply and reply.text else "Swagat hai! 👋")
            if reply and reply.media:
                chat_welcomes[chat_id] = {'text': text, 'media': reply.media}
                await event.edit("✅ **Welcome photo aur message set ho gaya hai.**")
            else:
                chat_welcomes[chat_id] = {'text': text, 'media': None}
                await event.edit("✅ **Welcome message set ho gaya hai.**")
        elif event.media:
            text = text_arg or "Swagat hai! 👋"
            chat_welcomes[chat_id] = {'text': text, 'media': event.media}
            await event.edit("✅ **Welcome photo aur message set ho gaya hai.**")
        else:
            await event.edit("ℹ️ **Istemaal:** Photo ke saath `/welcome [text]` bhejein ya photo par reply karein.")

    # WELCOME TRIGGER ON NEW MEMBER
    @ubot.on(events.ChatAction)
    async def welcome_new_member(event):
        if event.user_joined or event.user_added:
            chat_id = event.chat_id
            if chat_id in chat_welcomes:
                w_data = chat_welcomes[chat_id]
                try:
                    if w_data['media']:
                        await ubot.send_file(chat_id, w_data['media'], caption=w_data['text'])
                    else:
                        await ubot.send_message(chat_id, w_data['text'])
                except Exception:
                    pass

    # 1. AUTO-REACT (A): Self Messages Auto-React
    @ubot.on(events.NewMessage(outgoing=True))
    async def self_react_handler(event):
        if owner_id in afk_status and not event.raw_text.startswith(".afk"):
            afk_status.pop(owner_id, None)
        chat_id = event.chat_id
        if chat_id in self_reacts:
            try:
                await event.react(self_reacts[chat_id])
            except Exception:
                pass
