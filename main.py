import os
import sys
import json
import time
import asyncio
import random
import re
import threading
import tempfile
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
# KASHYAP USERBOT & HOSTING BOT (FULL FIXED EDITION)
# OWNER: KASHYAP (9239452757)
# ==========================================

try:
    import telethon
except ImportError:
    os.system(f"{sys.executable} -m pip install telethon")
    import telethon

from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from telethon.tl.functions.messages import ExportChatInviteRequest, SendReactionRequest
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantsBots, ReactionEmoji

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
    "╔═════════════════════════════════════════════════╗\n"
    "║        ⚡ **KASHYAP USERBOT — COMMANDS** ⚡        ║\n"
    "╚═════════════════════════════════════════════════╝\n\n"
    "▸ **BOT & HOSTING**\n"
    "  `/start` • `/login` • `/welcome [text]`\n\n"
    "▸ **RAID & SPAM**\n"
    "  `.raid [count]` • `.oneraid [count]` • `.rraid` • `.drraid`\n"
    "  `.spam [count] [text]` • `.fastspam [count] [text]` • `.flood [count] [text]`\n"
    "  `.engraid [count]` • `.praid [count]` • `.braid [count]`\n"
    "  `.araid` • `.saraid` • `.oaraid` • `.faraid` • `.earaid`\n"
    "  `.dmraid [count]` • `.mraid [count]` • `.delayraid [sec] [count]`\n"
    "  `.emoraid [count]` • `.emojispam [count] [emoji] [text]`\n"
    "  `.mixraid [1-50]` • `.tagraid [1-50]` • `.capsraid [1-50]` • `.slowraid [1-50]`\n"
    "  `.badaid [count]` • `.saraid2 [count]` • `.ultraid [count]`\n"
    "  `.auto [link] [count]` • `.chup` • `.bol`\n\n"
    "▸ **HACK & ANIMATION**\n"
    "  `.hack` • `.matrix` • `.scan`\n"
    "  `.bruteforce [1-50]` • `.packetflood [1-50]` • `.sysbreach [1-50]`\n"
    "  `.loading` • `.boom` • `.fbi`\n"
    "  `.pulse [1-50]` • `.countanim [1-50]` • `.glitch [1-50]`\n"
    "  `.fuck` • `.type [text]`\n\n"
    "▸ **GROUP, ADMIN & AUTOPIN**\n"
    "  `.ban` • `.unban` • `.kick` • `.mute` • `.unmute`\n"
    "  `.pin` • `.unpin` • `.del` • `.invite` • `.purge [count]`\n"
    "  `.autopin on <id>` • `.autopin off <id>`\n"
    "  `.dmautopin on <t>` • `.dmautopin off <t>`\n"
    "  `.tagall [text]` • `.admins` • `.bots` • `.pingall`\n\n"
    "▸ **DM, REACT & CONTROL**\n"
    "  `.dmblock on|off` • `.dmmute` • `.undmmute`\n"
    "  `.ar [emoji]` • `.dar` • `.uar` • `.duar` • `.rar [emojis...]` • `.drar`\n"
    "  `.stop` • `.stopall` • `.clear` • `.restart` • `.help`\n\n"
    "▸ **FUN, TEXT & UTILITY**\n"
    "  `.roast` • `.iq` • `.love` • `.toss` • `.dice` • `.coin` • `.rate [topic]`\n"
    "  `.calc [expr]` • `.calc2 [expr]` • `.mock [text]` • `.mock2 [text]`\n"
    "  `.reverse [text]` • `.clap [text]` • `.vapor [text]`\n"
    "  `.trim [text]` • `.caps [text]` • `.lower [text]` • `.title [text]`\n"
    "  `.ship` • `.slap` • `.hug` • `.8ball [question]` • `.fact` • `.shayari` • `.tts [text]`\n"
    "  `.ping` • `.alive` • `.alive2` • `.id` • `.id2` • `.info` • `.info2`\n"
    "  `.whois` • `.whois2` • `.chatinfo` • `.chatinfo2` • `.stats` • `.stats2`\n"
    "  `.time` • `.date` • `.afk [reason]` • `.timebio on|off` • `.save` • `.save2`\n\n"
    "✦ **POWERED BY » KASHYAP USERBOT** ✦"
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
    timebio_tasks = {}
    chup_muted_users = set()

    async def send_tg_reaction(target_chat, msg_id, emoji):
        try:
            await ubot(SendReactionRequest(
                peer=target_chat,
                msg_id=msg_id,
                reaction=[ReactionEmoji(emoticon=emoji)]
            ))
            return True
        except Exception:
            try:
                await ubot(SendReactionRequest(
                    peer=target_chat,
                    msg_id=msg_id,
                    reaction=[ReactionEmoji(emoticon=emoji)],
                    big=True
                ))
                return True
            except Exception:
                return False

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
        raw = (event.raw_text or "").strip()
        if raw.startswith(".") or raw.startswith("/"):
            return
        chat_id = event.chat_id
        if chat_id in self_reacts:
            await send_tg_reaction(chat_id, event.id, self_reacts[chat_id])

    @ubot.on(events.NewMessage(pattern=r'^\.ar\b', outgoing=True))
    async def ar_command(event):
        args = event.raw_text.split(maxsplit=1)
        chat_id = event.chat_id
        if len(args) < 2 or not args[1].strip():
            await event.edit("ℹ️ **Istemaal:** `.ar 🔥`")
            return
        emoji = args[1].strip().split()[0]
        ok = await send_tg_reaction(chat_id, event.id, emoji)
        if ok:
            self_reacts[chat_id] = emoji
            await event.edit(f"✅ **Self Auto-React chalu:** {emoji}")
        else:
            await event.edit(f"❌ **Reaction nahi lag paaya (`{emoji}`). Kisi doosre emoji se try karein.**")

    @ubot.on(events.NewMessage(pattern=r'^\.dar$', outgoing=True))
    async def dar_command(event):
        chat_id = event.chat_id
        if chat_id in self_reacts:
            del self_reacts[chat_id]
            await event.edit("🛑 **Self Auto-React band kar diya gaya hai.**")
        else:
            await event.edit("ℹ️ Yahan Self Auto-React chalu nahi hai.")

    # 2. AUTO-REACT (B): Target User Auto-React with '🔥'
    @ubot.on(events.NewMessage(incoming=True))
    async def uar_incoming_handler(event):
        chat_id = event.chat_id
        sender_id = event.sender_id
        if chat_id in user_react_targets and sender_id in user_react_targets[chat_id]:
            await send_tg_reaction(chat_id, event.id, "🔥")

    @ubot.on(events.NewMessage(pattern=r'^\.uar\b', outgoing=True))
    async def uar_command(event):
        chat_id = event.chat_id
        args = event.raw_text.split()
        target_user = None

        if event.is_reply:
            reply_msg = await event.get_reply_message()
            target_user = reply_msg.sender_id
        elif len(args) > 1:
            username = args[1]
            try:
                user_entity = await ubot.get_entity(username)
                target_user = user_entity.id
            except Exception:
                await event.edit("❌ **User ya username sahi nahi hai.**")
                return

        if target_user:
            if chat_id not in user_react_targets:
                user_react_targets[chat_id] = set()
            user_react_targets[chat_id].add(target_user)
            await event.edit("✅ **Target User Auto-React (`🔥`) chalu ho gaya hai.**")
        else:
            await event.edit("ℹ️ **Istemaal:** Kisi message par reply karein ya `.uar @username` likhein.")

    @ubot.on(events.NewMessage(pattern=r'^\.duar$', outgoing=True))
    async def duar_command(event):
        chat_id = event.chat_id
        if chat_id in user_react_targets:
            del user_react_targets[chat_id]
            await event.edit("🛑 **User Auto-React band kar diya gaya hai.**")
        else:
            await event.edit("ℹ️ Is chat mein koi User Auto-React chalu nahi hai.")

    # 3. AUTO-REACT (C): All Messages Auto-React with selected reactions
    @ubot.on(events.NewMessage(incoming=True))
    async def rar_incoming_handler(event):
        chat_id = event.chat_id
        if chat_id in all_reacts and all_reacts[chat_id]:
            emoji = random.choice(all_reacts[chat_id])
            await send_tg_reaction(chat_id, event.id, emoji)

    @ubot.on(events.NewMessage(pattern=r'^\.rar\b', outgoing=True))
    async def rar_command(event):
        args = event.raw_text.split()
        chat_id = event.chat_id
        emojis = [e.strip() for e in args[1:] if e.strip()]
        if not emojis:
            await event.edit("ℹ️ **Istemaal:** `.rar 🔥 💀 ⚡`")
            return
        ok = await send_tg_reaction(chat_id, event.id, emojis[0])
        if ok:
            all_reacts[chat_id] = emojis
            await event.edit(f"✅ **All-Message Auto-React chalu:** {' '.join(emojis)}")
        else:
            await event.edit(f"❌ **All-Message Auto-React set nahi ho saka (`{emojis[0]}`).**")

    @ubot.on(events.NewMessage(pattern=r'^\.drar$', outgoing=True))
    async def drar_command(event):
        chat_id = event.chat_id
        if chat_id in all_reacts:
            del all_reacts[chat_id]
            await event.edit("🛑 **All-Message Auto-React band kar diya gaya hai.**")
        else:
            await event.edit("ℹ️ Is chat mein All-Message Auto-React chalu nahi hai.")

    # 4. REPLY RAID (.rraid / .drraid)
    @ubot.on(events.NewMessage(pattern=r'^\.rraid$', outgoing=True))
    async def rraid_start_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi message par reply karke `.rraid` likhein.**")
            return
        reply = await event.get_reply_message()
        if not reply.sender_id:
            await event.edit("❌ **Target user ID nahi mil saki.**")
            return
        rraid_targets.add((event.chat_id, reply.sender_id))
        await event.edit(f"✅ **RRAID chalu (`{reply.sender_id}`).**")

    @ubot.on(events.NewMessage(pattern=r'^\.drraid$', outgoing=True))
    async def rraid_stop_cmd(event):
        if event.is_reply:
            reply = await event.get_reply_message()
            rraid_targets.discard((event.chat_id, reply.sender_id))
            await event.edit(f"🛑 **RRAID band (`{reply.sender_id}`).**")
        else:
            for item in [x for x in rraid_targets if x[0] == event.chat_id]:
                rraid_targets.discard(item)
            await event.edit("🛑 **Is chat ke saare RRAID band kar diye gaye hain.**")

    @ubot.on(events.NewMessage(incoming=True))
    async def rraid_watcher(event):
        if event.sender_id and (event.chat_id, event.sender_id) in rraid_targets:
            try:
                await event.reply(random.choice(GAALIS))
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
            except Exception:
                pass

    # 5. SPAM / FASTSPAM / FLOOD
    async def _spam_worker(target_chat, count, text, delay):
        try:
            for _ in range(count):
                if target_chat not in active_raids:
                    break
                try:
                    await ubot.send_message(target_chat, text)
                except FloodWaitError as f:
                    await asyncio.sleep(f.seconds + 0.5)
                except Exception:
                    break
                if delay > 0:
                    await asyncio.sleep(delay)
        finally:
            active_raids.discard(target_chat)
            active_raid_tasks.pop(target_chat, None)

    @ubot.on(events.NewMessage(pattern=r'^\.(spam|fastspam|flood)\b', outgoing=True))
    async def spam_cmd_handler(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split(maxsplit=2)
        if len(parts) < 3 or not parts[1].isdigit():
            await event.edit(f"ℹ️ **Istemaal:** `.{cmd} [count] [text]`")
            return
        count = max(1, min(int(parts[1]), 300))
        text = parts[2]
        delay = 0.05 if cmd == "fastspam" else (0.15 if cmd == "flood" else 0.25)

        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass
        task = asyncio.create_task(_spam_worker(event.chat_id, count, text, delay))
        active_raid_tasks[event.chat_id] = task

    # 6. RAID & ONERAID (.raid / .oneraid)
    async def _basic_raid_worker(target_chat, reply_to, count, single_only=False):
        try:
            for _ in range(count):
                if target_chat not in active_raids:
                    break
                msg = random.choice(SINGLE_GAALIS) if single_only else random.choice(GAALIS)
                try:
                    if reply_to:
                        await ubot.send_message(target_chat, msg, reply_to=reply_to)
                    else:
                        await ubot.send_message(target_chat, msg)
                except FloodWaitError as f:
                    await asyncio.sleep(f.seconds + 0.5)
                except Exception:
                    break
                await asyncio.sleep(0.2)
        finally:
            active_raids.discard(target_chat)
            active_raid_tasks.pop(target_chat, None)

    @ubot.on(events.NewMessage(pattern=r'^\.(raid|oneraid)\b', outgoing=True))
    async def basic_raid_handler(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split(maxsplit=1)
        count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 15
        count = max(1, min(count, 300))

        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass
        task = asyncio.create_task(_basic_raid_worker(event.chat_id, event.reply_to_msg_id, count, single_only=(cmd == "oneraid")))
        active_raid_tasks[event.chat_id] = task

    # 7. LANGUAGE RAIDS (.engraid / .praid / .braid)
    async def _multi_lang_raid_worker(target_chat, reply_to, count, pool):
        try:
            for _ in range(count):
                if target_chat not in active_raids:
                    break
                msg = random.choice(pool)
                try:
                    if reply_to:
                        await ubot.send_message(target_chat, msg, reply_to=reply_to)
                    else:
                        await ubot.send_message(target_chat, msg)
                except FloodWaitError as f:
                    await asyncio.sleep(f.seconds + 0.5)
                except Exception:
                    break
                await asyncio.sleep(0.2)
        finally:
            active_raids.discard(target_chat)
            active_raid_tasks.pop(target_chat, None)

    @ubot.on(events.NewMessage(pattern=r'^\.(engraid|praid|braid)\b', outgoing=True))
    async def multi_lang_raid_handler(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split(maxsplit=1)
        count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 15
        count = max(1, min(count, 300))

        pools = {
            "engraid": ENGLISH_RAIDS,
            "praid": PUNJABI_RAIDS,
            "braid": BENGALI_RAIDS,
        }
        pool = pools[cmd]

        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass
        task = asyncio.create_task(_multi_lang_raid_worker(event.chat_id, event.reply_to_msg_id, count, pool))
        active_raid_tasks[event.chat_id] = task

    # 8. EXTRA RAIDS: DMRAID, MRAID, DELAYRAID, EMORAID, EMOJISPAM & MAX-50 RAIDS
    @ubot.on(events.NewMessage(pattern=r'^\.dmraid\b', outgoing=True))
    async def dmraid_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi message par reply karke `.dmraid [count]` likhein.**")
            return
        reply = await event.get_reply_message()
        if not reply.sender_id:
            await event.edit("❌ **User ID nahi mil saki.**")
            return
        parts = event.raw_text.split()
        count = max(1, min(int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 15, 100))
        await event.edit(f"📩 **DM mein {count} messages bheje ja rahe hain...**")
        for _ in range(count):
            try:
                await ubot.send_message(reply.sender_id, random.choice(GAALIS))
                await asyncio.sleep(0.35)
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
            except Exception:
                break
        await event.edit("✅ **DM Raid poora ho gaya hai.**")

    @ubot.on(events.NewMessage(pattern=r'^\.(mraid|emoraid|mixraid|capsraid|slowraid)\b', outgoing=True))
    async def special_raids_cmd(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split()
        max_cap = 50 if cmd in ("mixraid", "capsraid", "slowraid") else 200
        default_cnt = 15
        count = max(1, min(int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else default_cnt, max_cap))
        delay = 1.6 if cmd == "slowraid" else 0.25

        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass

        async def _worker():
            try:
                for _ in range(count):
                    if event.chat_id not in active_raids:
                        break
                    if cmd == "mraid":
                        msg = random.choice(MULTI_LINE_RAIDS)
                    elif cmd == "emoraid":
                        em = random.choice(RAID_EMOJIS)
                        msg = f"{em} {random.choice(GAALIS)} {em}"
                    elif cmd == "mixraid":
                        msg = random.choice(ENGLISH_RAIDS + PUNJABI_RAIDS + BENGALI_RAIDS + GAALIS)
                    elif cmd == "capsraid":
                        msg = f"🔥 {random.choice(GAALIS).upper()} 🔥"
                    else:
                        msg = random.choice(GAALIS)
                    try:
                        await ubot.send_message(event.chat_id, msg, reply_to=event.reply_to_msg_id)
                    except FloodWaitError as f:
                        await asyncio.sleep(f.seconds + 0.5)
                    except Exception:
                        break
                    await asyncio.sleep(delay)
            finally:
                active_raids.discard(event.chat_id)
                active_raid_tasks.pop(event.chat_id, None)

        active_raid_tasks[event.chat_id] = asyncio.create_task(_worker())

    @ubot.on(events.NewMessage(pattern=r'^\.delayraid\b', outgoing=True))
    async def delayraid_cmd(event):
        parts = event.raw_text.split()
        if len(parts) < 3:
            await event.edit("ℹ️ **Istemaal:** `.delayraid [seconds] [count]`")
            return
        try:
            delay = max(0.2, min(float(parts[1]), 10.0))
            count = max(1, min(int(parts[2]), 200))
        except Exception:
            await event.edit("❌ **Numbers sahi nahi hain.**")
            return
        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass

        async def _worker():
            try:
                for _ in range(count):
                    if event.chat_id not in active_raids:
                        break
                    try:
                        await ubot.send_message(event.chat_id, random.choice(GAALIS), reply_to=event.reply_to_msg_id)
                    except FloodWaitError as f:
                        await asyncio.sleep(f.seconds + 0.5)
                    except Exception:
                        break
                    await asyncio.sleep(delay)
            finally:
                active_raids.discard(event.chat_id)
                active_raid_tasks.pop(event.chat_id, None)

        active_raid_tasks[event.chat_id] = asyncio.create_task(_worker())

    @ubot.on(events.NewMessage(pattern=r'^\.emojispam\b', outgoing=True))
    async def emojispam_cmd(event):
        parts = event.raw_text.split(maxsplit=3)
        if len(parts) < 4 or not parts[1].isdigit():
            await event.edit("ℹ️ **Istemaal:** `.emojispam [count] [emoji] [text]`")
            return
        count = max(1, min(int(parts[1]), 200))
        emoji = parts[2]
        text = parts[3]
        try:
            await event.delete()
        except Exception:
            pass
        for _ in range(count):
            try:
                await ubot.send_message(event.chat_id, f"{emoji} {text} {emoji}")
                await asyncio.sleep(0.15)
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
            except Exception:
                break

    @ubot.on(events.NewMessage(pattern=r'^\.tagraid\b', outgoing=True))
    async def tagraid_cmd(event):
        if not event.is_group and not event.is_channel:
            await event.edit("ℹ️ **Yeh command sirf group mein chalti hai.**")
            return
        parts = event.raw_text.split()
        count = max(1, min(int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10, 50))
        try:
            await event.delete()
        except Exception:
            pass
        members = []
        async for user in ubot.iter_participants(event.chat_id, limit=30):
            if not user.bot and user.first_name:
                members.append(f"[{user.first_name}](tg://user?id={user.id})")
        if not members:
            return
        for _ in range(count):
            tag = random.choice(members)
            try:
                await ubot.send_message(event.chat_id, f"{tag} {random.choice(GAALIS)}")
                await asyncio.sleep(0.5)
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
            except Exception:
                break

    # 9. FANCY DM WELCOME + OFFLINE AUTO-REPLY + DM CONTROL + AFK
    dm_welcomed_users = set()

    @ubot.on(events.NewMessage(pattern=r'^\.dmblock\b', outgoing=True))
    async def dmblock_cmd(event):
        parts = event.raw_text.split()
        if len(parts) < 2 or parts[1].lower() not in ("on", "off"):
            await event.edit("ℹ️ **Istemaal:** `.dmblock on` ya `.dmblock off`")
            return
        dm_block_enabled[owner_id] = (parts[1].lower() == "on")
        await event.edit(f"🛡️ **DM Auto-Block:** `{parts[1].upper()}`")

    @ubot.on(events.NewMessage(pattern=r'^\.dmmute$', outgoing=True))
    async def dmmute_cmd(event):
        target_id = event.chat_id if event.is_private else None
        if event.is_reply:
            r = await event.get_reply_message()
            target_id = r.sender_id
        if not target_id:
            await event.edit("ℹ️ **DM mein istemaal karein ya kisi message par reply karein.**")
            return
        dm_muted_users[owner_id].add(target_id)
        await event.edit(f"🔇 **DM mein mute kar diya gaya (`{target_id}`).**")

    @ubot.on(events.NewMessage(pattern=r'^\.undmmute$', outgoing=True))
    async def undmmute_cmd(event):
        target_id = event.chat_id if event.is_private else None
        if event.is_reply:
            r = await event.get_reply_message()
            target_id = r.sender_id
        if target_id and target_id in dm_muted_users[owner_id]:
            dm_muted_users[owner_id].remove(target_id)
            await event.edit(f"🔊 **DM mein unmute kar diya gaya (`{target_id}`).**")
        else:
            await event.edit("ℹ️ **Yeh user DM mein mute nahi hai.**")

    @ubot.on(events.NewMessage(incoming=True))
    async def dm_guard_and_afk(event):
        if event.is_private and event.sender_id:
            if event.sender_id in dm_muted_users.get(owner_id, set()):
                try:
                    await event.delete()
                except Exception:
                    pass
                return
            if dm_block_enabled.get(owner_id) and event.sender_id != OWNER_ID:
                try:
                    await ubot(BlockRequest(event.sender_id))
                except Exception:
                    pass
                return

        if event.is_private and event.sender_id and event.sender_id != owner_id:
            try:
                me = await ubot.get_me()
                owner_tag = f"@{me.username}" if getattr(me, "username", None) else (getattr(me, "first_name", None) or OWNER_NAME)
            except Exception:
                owner_tag = OWNER_NAME

            is_afk = owner_id in afk_status
            first_time_dm = event.sender_id not in dm_welcomed_users
            dm_welcomed_users.add(event.sender_id)

            lines = []
            if first_time_dm:
                lines.append(
                    "╔════════════════════════════╗\n"
                    "  ✦ 𝐇𝐄𝐘𝐘 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐌𝐘 𝐃𝐌 ✦\n"
                    "╚════════════════════════════╝\n"
                    "✨ 𝐁𝐚𝐚𝐭 𝐤𝐚𝐫𝐧𝐞 𝐤𝐞 𝐥𝐢𝐲𝐞 𝐬𝐡𝐮𝐤𝐫𝐢𝐲𝐚 🫶🌸"
                )
            if is_afk:
                reason = afk_status[owner_id]
                lines.append(
                    f"🌙 **{owner_tag}** 𝐚𝐛𝐡𝐢 𝐨𝐟𝐟𝐥𝐢𝐧𝐞 𝐡𝐚𝐢, 𝐛𝐚𝐚𝐝 𝐦𝐞𝐢𝐧 𝐚𝐚𝐩𝐤𝐞 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐤𝐚 𝐫𝐞𝐩𝐥𝐲 𝐤𝐚𝐫𝐞𝐧𝐠𝐞 💌✨\n"
                    f"🫧 *Note:* `{reason}`"
                )
            elif not first_time_dm:
                lines.append("✦ 𝐇𝐄𝐘𝐘 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐌𝐘 𝐃𝐌 ✦ ✨🫶")

            if lines:
                try:
                    await event.reply("\n\n".join(lines))
                except Exception:
                    pass
            return

        if owner_id in afk_status and event.mentioned:
            try:
                me = await ubot.get_me()
                owner_tag = f"@{me.username}" if getattr(me, "username", None) else (getattr(me, "first_name", None) or OWNER_NAME)
            except Exception:
                owner_tag = OWNER_NAME
            try:
                await event.reply(
                    f"🌙 **{owner_tag}** 𝐚𝐛𝐡𝐢 𝐨𝐟𝐟𝐥𝐢𝐧𝐞 𝐡𝐚𝐢, 𝐛𝐚𝐚𝐝 𝐦𝐞𝐢𝐧 𝐚𝐚𝐩𝐤𝐞 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐤𝐚 𝐫𝐞𝐩𝐥𝐲 𝐤𝐚𝐫𝐞𝐧𝐠𝐞 💌✨"
                )
            except Exception:
                pass

    @ubot.on(events.NewMessage(pattern=r'^\.afk\b', outgoing=True))
    async def afk_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        reason = parts[1] if len(parts) > 1 else "Offline"
        afk_status[owner_id] = reason
        await event.edit(f"🌙 **Offline Mode ON** ✨\n🫧 **Note:** `{reason}`")

    # 10. HACK & ANIMATION COMMANDS (INCLUDING MAX-50 STEPS)
    @ubot.on(events.NewMessage(pattern=r'^\.hack$', outgoing=True))
    async def hack_cmd(event):
        steps = [
            "💻 `Exploit module load ho raha hai...`",
            "🔓 `Firewall bypass ho raha hai... 34%`",
            "📡 `Payload bheja ja raha hai... 78%`",
            "✅ `Access complete (Simulated).`"
        ]
        for s in steps:
            await event.edit(s)
            await asyncio.sleep(0.55)

    @ubot.on(events.NewMessage(pattern=r'^\.matrix$', outgoing=True))
    async def matrix_cmd(event):
        frames = [
            "`01011010 11001010 00110101`",
            "`11100010 01010111 10101100`",
            "`00111100 10100101 11001011`"
        ]
        for f in frames:
            await event.edit(f)
            await asyncio.sleep(0.45)

    @ubot.on(events.NewMessage(pattern=r'^\.scan$', outgoing=True))
    async def scan_cmd(event):
        for pct in (15, 45, 80, 100):
            await event.edit(f"🔍 `Ports scan ho rahe hain... {pct}%`")
            await asyncio.sleep(0.4)

    @ubot.on(events.NewMessage(pattern=r'^\.(bruteforce|packetflood|sysbreach|pulse|countanim|glitch)\b', outgoing=True))
    async def step50_anim_cmd(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split()
        steps = max(1, min(int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 15, 50))
        pulse_icons = ["⚡", "🔥", "💥", "🌀"]
        glitch_chars = ["#", "%", "&", "@", "?", "!"]

        for i in range(1, steps + 1):
            if cmd == "bruteforce":
                txt = f"🔐 `Bruteforce [{i}/{steps}] -> {str(i).zfill(4)}`"
            elif cmd == "packetflood":
                txt = f"📡 `Packet [{i}/{steps}] -> 192.168.1.{i}:443`"
            elif cmd == "sysbreach":
                txt = f"🛡️ `Breach [{i}/{steps}] -> {int((i/steps)*100)}%`"
            elif cmd == "pulse":
                icon = pulse_icons[i % len(pulse_icons)]
                txt = f"{icon} **PULSE [{i}/{steps}]** {icon}"
            elif cmd == "countanim":
                txt = f"🔢 **Count:** `{i} / {steps}`"
            else:
                g = "".join(random.choice(glitch_chars) for _ in range(12))
                txt = f"⚡ `{g}` **[{i}/{steps}]**"
            try:
                await event.edit(txt)
                await asyncio.sleep(0.22)
            except Exception:
                break

    @ubot.on(events.NewMessage(pattern=r'^\.loading$', outgoing=True))
    async def loading_cmd(event):
        for p in range(0, 101, 25):
            bar = "■" * (p // 10) + "□" * (10 - (p // 10))
            await event.edit(f"`[{bar}] {p}%`")
            await asyncio.sleep(0.35)

    @ubot.on(events.NewMessage(pattern=r'^\.boom$', outgoing=True))
    async def boom_cmd(event):
        for n in ("3️⃣", "2️⃣", "1️⃣", "💥 **BOOM!** 💥"):
            await event.edit(n)
            await asyncio.sleep(0.45)

    @ubot.on(events.NewMessage(pattern=r'^\.fbi$', outgoing=True))
    async def fbi_cmd(event):
        for line in ["🚨 **FBI OPEN UP!** 🚨", "🚔 `Perimeter lock...`", "📡 `Signal trace...`"]:
            await event.edit(line)
            await asyncio.sleep(0.5)

    @ubot.on(events.NewMessage(pattern=r'^\.fuck$', outgoing=True))
    async def fuck_anim_cmd(event):
        frames = ["🖕", "🖕🔥", "🖕💥⚡", "🖕👑"]
        for fr in frames:
            await event.edit(fr)
            await asyncio.sleep(0.35)

    # 11. FUN & UTILITY COMMANDS
    @ubot.on(events.NewMessage(pattern=r'^\.roast\b', outgoing=True))
    async def roast_cmd(event):
        line = random.choice(ROAST_LINES)
        if event.is_reply:
            r = await event.get_reply_message()
            await r.reply(line)
            try:
                await event.delete()
            except Exception:
                pass
        else:
            await event.edit(line)

    @ubot.on(events.NewMessage(pattern=r'^\.iq$', outgoing=True))
    async def iq_cmd(event):
        await event.edit(f"🧠 **IQ:** `{random.randint(1, 150)}%`")

    @ubot.on(events.NewMessage(pattern=r'^\.love$', outgoing=True))
    async def love_cmd(event):
        await event.edit(f"❤️ **Match:** `{random.randint(1, 100)}%`")

    @ubot.on(events.NewMessage(pattern=r'^\.toss$', outgoing=True))
    async def toss_cmd(event):
        await event.edit(f"🪙 **Toss:** `{random.choice(['Heads', 'Tails'])}`")

    @ubot.on(events.NewMessage(pattern=r'^\.dice$', outgoing=True))
    async def dice_cmd(event):
        await event.edit(f"🎲 **Dice:** `{random.randint(1, 6)}`")

    @ubot.on(events.NewMessage(pattern=r'^\.ping$', outgoing=True))
    async def ping_cmd(event):
        t0 = time.time()
        msg = await event.edit("🏓 `Check ho raha hai...`")
        ms = int((time.time() - t0) * 1000)
        await msg.edit(f"🏓 **Pong:** `{ms} ms`")

    @ubot.on(events.NewMessage(pattern=r'^\.alive$', outgoing=True))
    async def alive_cmd(event):
        await event.edit(
            f"⚡ **{BOT_BRAND} Active hai**\n"
            f"👑 **Owner:** `{OWNER_NAME}`\n"
            f"⏱️ **Uptime:** `{format_uptime()}`"
        )

    @ubot.on(events.NewMessage(pattern=r'^\.id$', outgoing=True))
    async def id_cmd(event):
        txt = f"💬 **Chat ID:** `{event.chat_id}`\n✉️ **Msg ID:** `{event.id}`"
        if event.is_reply:
            r = await event.get_reply_message()
            txt += f"\n👤 **Reply User ID:** `{r.sender_id}`"
        await event.edit(txt)

    @ubot.on(events.NewMessage(pattern=r'^\.info$', outgoing=True))
    async def info_cmd(event):
        target = event.sender_id
        if event.is_reply:
            r = await event.get_reply_message()
            target = r.sender_id
        try:
            u = await ubot.get_entity(target)
            uname = f"\n• **Username:** `@{u.username}`" if getattr(u, 'username', None) else ""
            await event.edit(
                f"👤 **User Details**\n"
                f"• **ID:** `{u.id}`\n"
                f"• **Naam:** `{getattr(u, 'first_name', '')}`{uname}"
            )
        except Exception as e:
            await event.edit(f"❌ **Jankari nahi mil saki:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.calc\b', outgoing=True))
    async def calc_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2 or not re.fullmatch(r'[0-9+\-*/().%\s]+', parts[1]):
            await event.edit("ℹ️ **Istemaal:** `.calc 25*4`")
            return
        try:
            ans = eval(parts[1], {"__builtins__": None}, {})
            await event.edit(f"🧮 `{parts[1]}` = **`{ans}`**")
        except Exception:
            await event.edit("❌ **Expression sahi nahi hai.**")

    @ubot.on(events.NewMessage(pattern=r'^\.type\b', outgoing=True))
    async def type_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2:
            await event.edit("ℹ️ **Istemaal:** `.type hello`")
            return
        txt = parts[1]
        cur = ""
        for ch in txt:
            cur += ch
            await event.edit(f"`{cur}▌`")
            await asyncio.sleep(0.08)
        await event.edit(txt)

    @ubot.on(events.NewMessage(pattern=r'^\.mock\b', outgoing=True))
    async def mock_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        src = parts[1] if len(parts) > 1 else ""
        if not src and event.is_reply:
            r = await event.get_reply_message()
            src = r.raw_text or ""
        if not src:
            await event.edit("ℹ️ **Text dein ya kisi message par reply karein.**")
            return
        out = "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(src))
        await event.edit(out)

    @ubot.on(events.NewMessage(pattern=r'^\.save$', outgoing=True))
    async def save_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi message ya media par reply karke `.save` likhein.**")
            return
        r = await event.get_reply_message()
        try:
            await ubot.send_message("me", r)
            await event.edit("💾 **Saved Messages mein save ho gaya hai.**")
        except Exception as e:
            await event.edit(f"❌ **Save nahi ho saka:** `{e}`")

    # 12. STYLED RAIDS (.araid / .saraid / .oaraid / .faraid / .earaid) & STOP COMMANDS
    async def raid_worker(target_chat, command, reply_to, count):
        iteration = 0
        while target_chat in active_raids:
            if count is not None and iteration >= count:
                break

            if command == 'earaid':
                base_text = random.choice(EARAID_LIST)
            else:
                gaali = random.choice(GAALIS)
                if command == 'araid':
                    base_text = format_araid(gaali)
                elif command == 'saraid':
                    base_text = format_saraid(gaali)
                elif command == 'oaraid':
                    base_text = format_oaraid(gaali)
                elif command == 'faraid':
                    base_text = format_faraid(gaali)
                else:
                    base_text = gaali

            try:
                if reply_to:
                    await ubot.send_message(target_chat, base_text, reply_to=reply_to)
                else:
                    await ubot.send_message(target_chat, base_text)
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
            except Exception:
                await asyncio.sleep(0.5)

            iteration += 1
            await asyncio.sleep(1.1 / 8)

        active_raids.discard(target_chat)
        active_raid_tasks.pop(target_chat, None)

    @ubot.on(events.NewMessage(pattern=r'^\.(araid|saraid|oaraid|faraid|earaid)', outgoing=True))
    async def raid_handler(event):
        command = event.pattern_match.group(1)
        args = event.raw_text.split()

        target_chat = event.chat_id
        reply_to = event.reply_to_msg_id
        count = None
        target_arg = None

        for arg in args[1:]:
            if arg.isdigit():
                count = int(arg)
            else:
                target_arg = arg

        if target_arg:
            if "t.me/" in target_arg:
                if "/c/" in target_arg:
                    match = re.search(r'/c/(\d+)/(\d+)', target_arg)
                    if match:
                        target_chat = int("-100" + match.group(1))
                        reply_to = int(match.group(2))
                else:
                    match = re.search(r't\.me/([^/]+)(?:/(\d+))?', target_arg)
                    if match:
                        username = match.group(1)
                        msg_id = match.group(2)
                        try:
                            entity = await ubot.get_entity(username)
                            target_chat = entity.id
                            if msg_id:
                                reply_to = int(msg_id)
                        except Exception:
                            pass
            elif target_arg.startswith("@"):
                try:
                    entity = await ubot.get_entity(target_arg)
                    target_chat = entity.id
                except Exception:
                    pass

        if target_chat in active_raid_tasks:
            active_raid_tasks[target_chat].cancel()

        active_raids.add(target_chat)
        try:
            await event.delete()
        except Exception:
            pass

        task = asyncio.create_task(raid_worker(target_chat, command, reply_to, count))
        active_raid_tasks[target_chat] = task

    @ubot.on(events.NewMessage(pattern=r'^\.stop$', outgoing=True))
    async def stop_raid(event):
        chat_id = event.chat_id
        if chat_id in active_raids:
            active_raids.remove(chat_id)
            if chat_id in active_raid_tasks:
                active_raid_tasks[chat_id].cancel()
                del active_raid_tasks[chat_id]
            try:
                await event.edit("🛑 **Is chat mein raid rok di gayi hai.**")
            except Exception:
                pass
        else:
            try:
                await event.edit("ℹ️ **Is chat mein koi raid nahi chal rahi hai.**")
            except Exception:
                pass

    @ubot.on(events.NewMessage(pattern=r'^\.stopall$', outgoing=True))
    async def stop_all_raids(event):
        active_raids.clear()
        for chat_id, task in active_raid_tasks.items():
            task.cancel()
        active_raid_tasks.clear()
        for item in [x for x in rraid_targets if x[0] == event.chat_id]:
            rraid_targets.discard(item)
        try:
            await event.edit("🛑 **Sabhi active raids rok di gayi hain.**")
        except Exception:
            pass

    # 13. GROUP/ADMIN, TEXT/FUN, UTILITY & EXTRA RAID MODES
    async def _extract_target_user(event):
        if event.is_reply:
            r = await event.get_reply_message()
            if r and r.sender_id:
                return r.sender_id
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) > 1:
            target = parts[1].strip().split()[0]
            if target.isdigit():
                return int(target)
            try:
                ent = await ubot.get_entity(target)
                return ent.id
            except Exception:
                return None
        return None

    @ubot.on(events.NewMessage(pattern=r'^\.ban\b', outgoing=True))
    async def ban_cmd(event):
        if not event.is_group and not event.is_channel:
            await event.edit("ℹ️ **Yeh command group ya channel mein chalti hai.**")
            return
        uid = await _extract_target_user(event)
        if not uid:
            await event.edit("ℹ️ **Kisi message par reply karein ya username/ID dein.**")
            return
        try:
            await ubot.edit_permissions(event.chat_id, uid, view_messages=False)
            await event.edit(f"🔨 **User ban kar diya gaya:** `{uid}`")
        except Exception as e:
            await event.edit(f"❌ **Ban nahi ho saka:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.unban\b', outgoing=True))
    async def unban_cmd(event):
        if not event.is_group and not event.is_channel:
            await event.edit("ℹ️ **Yeh command group ya channel mein chalti hai.**")
            return
        uid = await _extract_target_user(event)
        if not uid:
            await event.edit("ℹ️ **Kisi message par reply karein ya username/ID dein.**")
            return
        try:
            await ubot.edit_permissions(event.chat_id, uid, view_messages=True)
            await event.edit(f"✅ **User unban kar diya gaya:** `{uid}`")
        except Exception as e:
            await event.edit(f"❌ **Unban nahi ho saka:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.kick\b', outgoing=True))
    async def kick_cmd(event):
        if not event.is_group and not event.is_channel:
            await event.edit("ℹ️ **Yeh command group ya channel mein chalti hai.**")
            return
        uid = await _extract_target_user(event)
        if not uid:
            await event.edit("ℹ️ **Kisi message par reply karein ya username/ID dein.**")
            return
        try:
            await ubot.kick_participant(event.chat_id, uid)
            await event.edit(f"👢 **User kick kar diya gaya:** `{uid}`")
        except Exception as e:
            await event.edit(f"❌ **Kick nahi ho saka:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.mute\b', outgoing=True))
    async def mute_cmd(event):
        if not event.is_group and not event.is_channel:
            await event.edit("ℹ️ **Yeh command group ya channel mein chalti hai.**")
            return
        uid = await _extract_target_user(event)
        if not uid:
            await event.edit("ℹ️ **Kisi message par reply karein ya username/ID dein.**")
            return
        try:
            await ubot.edit_permissions(event.chat_id, uid, send_messages=False)
            await event.edit(f"🔇 **User mute kar diya gaya:** `{uid}`")
        except Exception as e:
            await event.edit(f"❌ **Mute nahi ho saka:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.unmute\b', outgoing=True))
    async def unmute_cmd(event):
        if not event.is_group and not event.is_channel:
            await event.edit("ℹ️ **Yeh command group ya channel mein chalti hai.**")
            return
        uid = await _extract_target_user(event)
        if not uid:
            await event.edit("ℹ️ **Kisi message par reply karein ya username/ID dein.**")
            return
        try:
            await ubot.edit_permissions(event.chat_id, uid, send_messages=True)
            await event.edit(f"🔊 **User unmute kar diya gaya:** `{uid}`")
        except Exception as e:
            await event.edit(f"❌ **Unmute nahi ho saka:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.pin$', outgoing=True))
    async def pin_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Pin karne ke liye kisi message par reply karein.**")
            return
        r = await event.get_reply_message()
        try:
            await ubot.pin_message(event.chat_id, r.id, notify=False)
            await event.edit("📌 **Message pin kar diya gaya hai.**")
        except Exception as e:
            await event.edit(f"❌ **Pin nahi ho saka:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.unpin$', outgoing=True))
    async def unpin_cmd(event):
        try:
            msg_id = None
            if event.is_reply:
                r = await event.get_reply_message()
                msg_id = r.id
            await ubot.unpin_message(event.chat_id, msg_id)
            await event.edit("📍 **Message unpin kar diya gaya hai.**")
        except Exception as e:
            await event.edit(f"❌ **Unpin nahi ho saka:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.del$', outgoing=True))
    async def del_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Delete karne ke liye kisi message par reply karein.**")
            return
        r = await event.get_reply_message()
        try:
            await r.delete()
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ **Delete nahi ho saka:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.invite$', outgoing=True))
    async def invite_cmd(event):
        if not event.is_group and not event.is_channel:
            await event.edit("ℹ️ **Yeh command group ya channel mein chalti hai.**")
            return
        try:
            invite = await ubot(ExportChatInviteRequest(event.chat_id))
            await event.edit(f"🔗 **Invite Link:** {invite.link}")
        except Exception as e:
            await event.edit(f"❌ **Link nahi ban saka:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.reverse\b', outgoing=True))
    async def reverse_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else ((await event.get_reply_message()).raw_text if event.is_reply else "")
        if not txt:
            await event.edit("ℹ️ **Istemaal:** `.reverse [text]`")
            return
        await event.edit(txt[::-1])

    @ubot.on(events.NewMessage(pattern=r'^\.clap\b', outgoing=True))
    async def clap_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else ((await event.get_reply_message()).raw_text if event.is_reply else "")
        if not txt:
            await event.edit("ℹ️ **Istemaal:** `.clap [text]`")
            return
        await event.edit(" 👏 ".join(txt.split()))

    @ubot.on(events.NewMessage(pattern=r'^\.vapor\b', outgoing=True))
    async def vapor_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else ((await event.get_reply_message()).raw_text if event.is_reply else "")
        if not txt:
            await event.edit("ℹ️ **Istemaal:** `.vapor [text]`")
            return
        wide = "".join(chr(ord(c) + 0xFEE0) if 33 <= ord(c) <= 126 else (" " if c == " " else c) for c in txt)
        await event.edit(wide)

    @ubot.on(events.NewMessage(pattern=r'^\.ship\b', outgoing=True))
    async def ship_cmd(event):
        pct = random.randint(1, 100)
        bar = "❤️" * max(1, pct // 20) + "🤍" * (5 - max(1, pct // 20))
        await event.edit(f"💘 **Compatibility:** `{pct}%`\n{bar}")

    @ubot.on(events.NewMessage(pattern=r'^\.slap$', outgoing=True))
    async def slap_cmd(event):
        msg = "👋💥 *Ek zor ka slap laga!* 😵‍💫"
        if event.is_reply:
            r = await event.get_reply_message()
            await r.reply(msg)
            try:
                await event.delete()
            except Exception:
                pass
        else:
            await event.edit(msg)

    @ubot.on(events.NewMessage(pattern=r'^\.hug$', outgoing=True))
    async def hug_cmd(event):
        msg = "🤗🫶 *Ek warm hug!* ✨"
        if event.is_reply:
            r = await event.get_reply_message()
            await r.reply(msg)
            try:
                await event.delete()
            except Exception:
                pass
        else:
            await event.edit(msg)

    @ubot.on(events.NewMessage(pattern=r'^\.8ball\b', outgoing=True))
    async def eightball_cmd(event):
        answers = [
            "Haan, bilkul pakka hai! ✨",
            "Abhi kuch kehna mushkil hai 🔮",
            "Bilkul nahi ❌",
            "Aage chal kar mauka milega 🌟",
            "100% chances hain 🔥"
        ]
        await event.edit(f"🎱 **8Ball:** {random.choice(answers)}")

    @ubot.on(events.NewMessage(pattern=r'^\.fact$', outgoing=True))
    async def fact_cmd(event):
        facts = [
            "🐙 Octopus ke paas teen dil aur neela khoon hota hai.",
            "🍯 Shahad (honey) kabhi kharab nahi hota.",
            "⚡ Bijli ki garmi suraj ki satah se bhi zyada hoti hai.",
            "🌙 Chand har saal dharti se lagbhag 3.8 cm door ja raha hai."
        ]
        await event.edit(f"💡 **Fact:** {random.choice(facts)}")

    @ubot.on(events.NewMessage(pattern=r'^\.shayari$', outgoing=True))
    async def shayari_cmd(event):
        lines = [
            "✨ *Apni pehchan khud banani padti hai, naam se sirf shor hota hai.* 🔥",
            "🌙 *Khamoshi ko kamzori mat samajhna, toofan aksar shant aata hai.* ⚡",
            "👑 *Bheed mein chalna aasaan hai, apna raasta khud banana alag baat hai.* 💫"
        ]
        await event.edit(random.choice(lines))

    @ubot.on(events.NewMessage(pattern=r'^\.time$', outgoing=True))
    async def time_cmd(event):
        now = datetime.now().strftime("%I:%M:%S %p")
        await event.edit(f"🕒 **Current Time:** `{now}`")

    @ubot.on(events.NewMessage(pattern=r'^\.date$', outgoing=True))
    async def date_cmd(event):
        today = datetime.now().strftime("%A, %d %B %Y")
        await event.edit(f"📅 **Today's Date:** `{today}`")

    @ubot.on(events.NewMessage(pattern=r'^\.whois\b', outgoing=True))
    async def whois_cmd(event):
        uid = await _extract_target_user(event) or event.sender_id
        try:
            u = await ubot.get_entity(uid)
            uname = f"@{u.username}" if getattr(u, "username", None) else "None"
            dc = getattr(u, "photo", None)
            dc_id = getattr(dc, "dc_id", "N/A") if dc else "N/A"
            await event.edit(
                f"🪪 **Whois Profile**\n"
                f"• **ID:** `{u.id}`\n"
                f"• **First Name:** `{getattr(u, 'first_name', '')}`\n"
                f"• **Username:** `{uname}`\n"
                f"• **DC:** `{dc_id}`"
            )
        except Exception as e:
            await event.edit(f"❌ **Whois nahi mil saka:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.chatinfo$', outgoing=True))
    async def chatinfo_cmd(event):
        try:
            chat = await event.get_chat()
            title = getattr(chat, "title", None) or getattr(chat, "first_name", "Private Chat")
            await event.edit(
                f"💬 **Chat Info**\n"
                f"• **Title:** `{title}`\n"
                f"• **Chat ID:** `{event.chat_id}`\n"
                f"• **Type:** `{'Group/Channel' if (event.is_group or event.is_channel) else 'Private'}`"
            )
        except Exception as e:
            await event.edit(f"❌ **Chat info nahi mil saki:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.stats$', outgoing=True))
    async def stats_cmd(event):
        await event.edit(
            f"📊 **{BOT_BRAND} Stats**\n"
            f"• **Hosted Sessions:** `{len(user_sessions)}`\n"
            f"• **Active Raids:** `{len(active_raids)}`\n"
            f"• **RRAID Targets:** `{len(rraid_targets)}`\n"
            f"• **AutoPin Chats:** `{len(autopin_chats)}`\n"
            f"• **DM AutoPin Targets:** `{len(dm_autopin_targets)}`\n"
            f"• **Uptime:** `{format_uptime()}`"
        )

    @ubot.on(events.NewMessage(pattern=r'^\.help$', outgoing=True))
    async def ubot_help_cmd(event):
        await event.edit(STATIC_COMMANDS_TEXT)

    @ubot.on(events.NewMessage(pattern=r'^\.restart$', outgoing=True))
    async def restart_cmd(event):
        await event.edit("🔄 **Session restart ho raha hai...**")
        asyncio.create_task(start_userbot_session(session_string, owner_id))
        await asyncio.sleep(0.5)
        raise events.StopPropagation

    @ubot.on(events.NewMessage(pattern=r'^\.(badaid|saraid2|ultraid)\b', outgoing=True))
    async def extra_28_raids_cmd(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split()
        count = max(1, min(int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 15, 100))

        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass

        async def _worker():
            try:
                for _ in range(count):
                    if event.chat_id not in active_raids:
                        break
                    base = random.choice(GAALIS)
                    if cmd == "badaid":
                        msg = f"🔥 {base.upper()} 🔥"
                    elif cmd == "saraid2":
                        msg = format_saraid(base)
                    else:
                        msg = f"⚡ {format_araid(base)} 💀"
                    try:
                        await ubot.send_message(event.chat_id, msg, reply_to=event.reply_to_msg_id)
                    except FloodWaitError as f:
                        await asyncio.sleep(f.seconds + 0.5)
                    except Exception:
                        break
                    await asyncio.sleep(0.2)
            finally:
                active_raids.discard(event.chat_id)
                active_raid_tasks.pop(event.chat_id, None)

        active_raid_tasks[event.chat_id] = asyncio.create_task(_worker())

    # 14. AUTOPIN + DMAUTOPIN + TAGALL / ADMINS / BOTS / TEXT / COIN / RATE / CLEAR
    async def _resolve_chat_target(raw_arg, fallback_id):
        if not raw_arg:
            return fallback_id
        token = raw_arg.strip()
        if token.lstrip("-").isdigit():
            return int(token)
        try:
            ent = await ubot.get_entity(token)
            return ent.id
        except Exception:
            return None

    @ubot.on(events.NewMessage(pattern=r'^\.autopin\b', outgoing=True))
    async def autopin_cmd(event):
        parts = event.raw_text.split()
        if len(parts) < 2 or parts[1].lower() not in ("on", "off"):
            await event.edit("ℹ️ **Istemaal:** `.autopin on <id>` ya `.autopin off <id>`")
            return

        mode = parts[1].lower()
        target_arg = parts[2] if len(parts) > 2 else None
        target_chat = await _resolve_chat_target(target_arg, event.chat_id)
        if not target_chat:
            await event.edit("❌ **Chat ID ya target sahi nahi hai.**")
            return

        if mode == "on":
            autopin_chats.add(target_chat)
            await event.edit(f"📌 **AutoPin ON** ho gaya hai chat `{target_chat}` ke liye.")
        else:
            autopin_chats.discard(target_chat)
            await event.edit(f"📍 **AutoPin OFF** ho gaya hai chat `{target_chat}` ke liye.")

    @ubot.on(events.NewMessage(incoming=True))
    async def autopin_incoming_handler(event):
        if event.is_private:
            if event.sender_id and event.sender_id in dm_autopin_targets:
                try:
                    await ubot.pin_message(event.sender_id, event.id, notify=False)
                except Exception:
                    pass
            return

        if event.chat_id in autopin_chats:
            try:
                await ubot.pin_message(event.chat_id, event.id, notify=False)
            except Exception:
                pass

    @ubot.on(events.NewMessage(pattern=r'^\.dmautopin\b', outgoing=True))
    async def dmautopin_cmd(event):
        parts = event.raw_text.split()
        if len(parts) < 2 or parts[1].lower() not in ("on", "off"):
            await event.edit("ℹ️ **Istemaal:** `.dmautopin on <t>` ya `.dmautopin off <t>`")
            return

        mode = parts[1].lower()
        target_arg = parts[2] if len(parts) > 2 else (str(event.chat_id) if event.is_private else None)
        if not target_arg and event.is_reply:
            r = await event.get_reply_message()
            if r and r.sender_id:
                target_arg = str(r.sender_id)

        target_uid = await _resolve_chat_target(target_arg, None)
        if not target_uid:
            await event.edit("ℹ️ **DM target (`<t>` = user ID / `@username` / DM chat) dein.**")
            return

        if mode == "on":
            dm_autopin_targets.add(target_uid)
            await event.edit(f"📌 **DM AutoPin ON** ho gaya hai target `{target_uid}` ke liye.")
        else:
            dm_autopin_targets.discard(target_uid)
            await event.edit(f"📍 **DM AutoPin OFF** ho gaya hai target `{target_uid}` ke liye.")

    @ubot.on(events.NewMessage(pattern=r'^\.tagall\b', outgoing=True))
    async def tagall_cmd(event):
        if not event.is_group and not event.is_channel:
            await event.edit("ℹ️ **Yeh command group mein chalti hai.**")
            return
        parts = event.raw_text.split(maxsplit=1)
        extra = parts[1].strip() if len(parts) > 1 else "Attention!"
        mentions = []
        async for user in ubot.iter_participants(event.chat_id, limit=25):
            if not user.bot and user.first_name:
                mentions.append(f"[{user.first_name}](tg://user?id={user.id})")
        if not mentions:
            await event.edit("ℹ️ **Koi member tag karne ke liye nahi mila.**")
            return
        await event.edit(f"📣 **{extra}**\n" + " • ".join(mentions))

    @ubot.on(events.NewMessage(pattern=r'^\.admins$', outgoing=True))
    async def admins_cmd(event):
        if not event.is_group and not event.is_channel:
            await event.edit("ℹ️ **Yeh command group mein chalti hai.**")
            return
        adm_list = []
        async for user in ubot.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
            name = user.first_name or "Admin"
            adm_list.append(f"👑 [{name}](tg://user?id={user.id})")
        await event.edit("🛡️ **Group Admins**\n" + ("\n".join(adm_list) if adm_list else "Koi admin list nahi mili."))

    @ubot.on(events.NewMessage(pattern=r'^\.bots$', outgoing=True))
    async def bots_cmd(event):
        if not event.is_group and not event.is_channel:
            await event.edit("ℹ️ **Yeh command group mein chalti hai.**")
            return
        bot_list = []
        async for b in ubot.iter_participants(event.chat_id, filter=ChannelParticipantsBots):
            uname = f"@{b.username}" if getattr(b, "username", None) else str(b.id)
            bot_list.append(f"🤖 `{b.first_name or 'Bot'}` ({uname})")
        await event.edit("🤖 **Group Bots**\n" + ("\n".join(bot_list) if bot_list else "Koi bot nahi mila."))

    @ubot.on(events.NewMessage(pattern=r'^\.trim\b', outgoing=True))
    async def trim_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else ((await event.get_reply_message()).raw_text if event.is_reply else "")
        if not txt:
            await event.edit("ℹ️ **Istemaal:** `.trim [text]`")
            return
        await event.edit(" ".join(txt.split()))

    @ubot.on(events.NewMessage(pattern=r'^\.caps\b', outgoing=True))
    async def caps_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else ((await event.get_reply_message()).raw_text if event.is_reply else "")
        if not txt:
            await event.edit("ℹ️ **Istemaal:** `.caps [text]`")
            return
        await event.edit(txt.upper())

    @ubot.on(events.NewMessage(pattern=r'^\.lower\b', outgoing=True))
    async def lower_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else ((await event.get_reply_message()).raw_text if event.is_reply else "")
        if not txt:
            await event.edit("ℹ️ **Istemaal:** `.lower [text]`")
            return
        await event.edit(txt.lower())

    @ubot.on(events.NewMessage(pattern=r'^\.title\b', outgoing=True))
    async def title_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else ((await event.get_reply_message()).raw_text if event.is_reply else "")
        if not txt:
            await event.edit("ℹ️ **Istemaal:** `.title [text]`")
            return
        await event.edit(txt.title())

    @ubot.on(events.NewMessage(pattern=r'^\.coin$', outgoing=True))
    async def coin_cmd(event):
        await event.edit("🪙 `Coin toss ho raha hai...`")
        await asyncio.sleep(0.35)
        await event.edit(f"🪙 **Result:** `{random.choice(['HEADS', 'TAILS'])}`")

    @ubot.on(events.NewMessage(pattern=r'^\.rate\b', outgoing=True))
    async def rate_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        topic = parts[1].strip() if len(parts) > 1 else "Yeh"
        score = random.randint(1, 10)
        stars = "⭐" * max(1, min(score // 2, 5))
        await event.edit(f"🎯 **Rating for {topic}:** `{score}/10` {stars}")

    @ubot.on(events.NewMessage(pattern=r'^\.clear$', outgoing=True))
    async def clear_states_cmd(event):
        autopin_chats.discard(event.chat_id)
        if event.is_private and event.chat_id:
            dm_autopin_targets.discard(event.chat_id)
        await event.edit(
            "🧹 **Chat States Cleared**\n"
            f"• **AutoPin Chats:** `{len(autopin_chats)}`\n"
            f"• **DM AutoPin Targets:** `{len(dm_autopin_targets)}`"
        )

    # 15. SCREENSHOT COMMANDS (.purge, .timebio, .tts, .auto, .chup, .bol) + 10 EXTRA COMMANDS
    @ubot.on(events.NewMessage(pattern=r'^\.purge\b', outgoing=True))
    async def purge_cmd(event):
        parts = event.raw_text.split()
        limit = max(1, min(int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 20, 100))
        msg_ids = []
        if event.is_reply:
            r = await event.get_reply_message()
            async for m in ubot.iter_messages(event.chat_id, min_id=max(0, r.id - 1), max_id=event.id + 1, limit=limit):
                msg_ids.append(m.id)
        else:
            async for m in ubot.iter_messages(event.chat_id, limit=limit):
                msg_ids.append(m.id)
        if not msg_ids:
            await event.edit("ℹ️ **Saaf karne ke liye koi message nahi mila.**")
            return
        try:
            await ubot.delete_messages(event.chat_id, msg_ids)
        except Exception as e:
            await event.edit(f"❌ **Purge nahi ho saka:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.timebio\b', outgoing=True))
    async def timebio_cmd(event):
        parts = event.raw_text.split()
        if len(parts) < 2 or parts[1].lower() not in ("on", "off"):
            await event.edit("ℹ️ **Istemaal:** `.timebio on` ya `.timebio off`")
            return
        mode = parts[1].lower()
        if mode == "off":
            task = timebio_tasks.pop(owner_id, None)
            if task:
                task.cancel()
            await event.edit("🛑 **TimeBio OFF ho gaya hai.**")
            return

        old_task = timebio_tasks.pop(owner_id, None)
        if old_task:
            old_task.cancel()

        async def _bio_loop():
            try:
                while True:
                    now_str = datetime.now().strftime("%I:%M %p")
                    bio_text = f"⚡ {BOT_BRAND} | 🕒 {now_str}"[:70]
                    try:
                        await ubot(UpdateProfileRequest(about=bio_text))
                    except Exception:
                        pass
                    await asyncio.sleep(60)
            except asyncio.CancelledError:
                pass

        timebio_tasks[owner_id] = asyncio.create_task(_bio_loop())
        await event.edit("🕒 **Live Clock TimeBio ON ho gaya hai.**")

    @ubot.on(events.NewMessage(pattern=r'^\.tts\b', outgoing=True))
    async def tts_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1].strip() if len(parts) > 1 else ((await event.get_reply_message()).raw_text if event.is_reply else "")
        if not txt:
            await event.edit("ℹ️ **Istemaal:** `.tts [text]`")
            return
        clean_txt = re.sub(r'[^\w\s\u0900-\u097F.,!?-]', '', txt).strip() or txt
        try:
            from gtts import gTTS
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
                mp3_path = tf.name
            gTTS(text=clean_txt[:300], lang="hi").save(mp3_path)
            await ubot.send_file(event.chat_id, mp3_path, voice_note=True, reply_to=event.reply_to_msg_id)
            try:
                os.remove(mp3_path)
            except Exception:
                pass
            try:
                await event.delete()
            except Exception:
                pass
        except ImportError:
            await event.edit(f"🎙️ **TTS:** `{clean_txt}` *(gTTS install karein voice note ke liye)*")
        except Exception as e:
            await event.edit(f"❌ **TTS error:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.auto\b', outgoing=True))
    async def auto_smart_link_cmd(event):
        parts = event.raw_text.split()
        target_chat = event.chat_id
        reply_to = event.reply_to_msg_id
        count = 15
        for tok in parts[1:]:
            if tok.isdigit():
                count = max(1, min(int(tok), 200))
            elif "t.me/" in tok:
                if "/c/" in tok:
                    m = re.search(r'/c/(\d+)/(\d+)', tok)
                    if m:
                        target_chat = int("-100" + m.group(1))
                        reply_to = int(m.group(2))
                else:
                    m = re.search(r't\.me/([^/]+)(?:/(\d+))?', tok)
                    if m:
                        try:
                            ent = await ubot.get_entity(m.group(1))
                            target_chat = ent.id
                            if m.group(2):
                                reply_to = int(m.group(2))
                        except Exception:
                            pass
            elif tok.startswith("@"):
                try:
                    ent = await ubot.get_entity(tok)
                    target_chat = ent.id
                except Exception:
                    pass

        if target_chat in active_raid_tasks:
            active_raid_tasks[target_chat].cancel()
        active_raids.add(target_chat)
        try:
            await event.delete()
        except Exception:
            pass

        async def _auto_worker():
            try:
                for _ in range(count):
                    if target_chat not in active_raids:
                        break
                    try:
                        await ubot.send_message(target_chat, random.choice(SINGLE_GAALIS), reply_to=reply_to)
                    except FloodWaitError as f:
                        await asyncio.sleep(f.seconds + 0.5)
                    except Exception:
                        break
                    await asyncio.sleep(0.2)
            finally:
                active_raids.discard(target_chat)
                active_raid_tasks.pop(target_chat, None)

        active_raid_tasks[target_chat] = asyncio.create_task(_auto_worker())

    @ubot.on(events.NewMessage(pattern=r'^\.chup$', outgoing=True))
    async def chup_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi message par reply karke `.chup` likhein.**")
            return
        r = await event.get_reply_message()
        if not r or not r.sender_id:
            await event.edit("❌ **User ID nahi mil saki.**")
            return
        chup_muted_users.add(r.sender_id)
        if event.is_group or event.is_channel:
            try:
                await ubot.edit_permissions(event.chat_id, r.sender_id, send_messages=False)
            except Exception:
                pass
        await event.edit(f"🤐 **Chup kar diya gaya (`{r.sender_id}`). Unmute ke liye `.bol`.**")

    @ubot.on(events.NewMessage(pattern=r'^\.bol$', outgoing=True))
    async def bol_cmd(event):
        target_id = None
        if event.is_reply:
            r = await event.get_reply_message()
            target_id = r.sender_id if r else None
        if not target_id and chup_muted_users:
            target_id = next(iter(chup_muted_users))
        if not target_id:
            await event.edit("ℹ️ **Unmute karne ke liye reply karein ya `.bol` chalayein.**")
            return
        chup_muted_users.discard(target_id)
        if event.is_group or event.is_channel:
            try:
                await ubot.edit_permissions(event.chat_id, target_id, send_messages=True)
            except Exception:
                pass
        await event.edit(f"🗣️ **Ab bol sakta hai (`{target_id}`) — Unmute ho gaya.**")

    # 10 EXTRA COMMANDS
    @ubot.on(events.NewMessage(pattern=r'^\.pingall$', outgoing=True))
    async def pingall_cmd(event):
        if not event.is_group and not event.is_channel:
            await event.edit("ℹ️ **Yeh command group mein chalti hai.**")
            return
        tags = []
        async for u in ubot.iter_participants(event.chat_id, limit=20):
            if not u.bot and u.first_name:
                tags.append(f"[{u.first_name}](tg://user?id={u.id})")
        await event.edit("🔔 " + (" • ".join(tags) if tags else "No users."))

    @ubot.on(events.NewMessage(pattern=r'^\.alive2$', outgoing=True))
    async def alive2_cmd(event):
        await event.edit(f"⚡ **{BOT_BRAND} v2** | 👑 `{OWNER_NAME}` | ⏱️ `{format_uptime()}`")

    @ubot.on(events.NewMessage(pattern=r'^\.id2$', outgoing=True))
    async def id2_cmd(event):
        r = await event.get_reply_message() if event.is_reply else None
        await event.edit(f"`Chat: {event.chat_id} | Msg: {event.id} | ReplyUser: {r.sender_id if r else 'None'}`")

    @ubot.on(events.NewMessage(pattern=r'^\.info2$', outgoing=True))
    async def info2_cmd(event):
        uid = (await event.get_reply_message()).sender_id if event.is_reply else event.sender_id
        u = await ubot.get_entity(uid)
        await event.edit(f"👤 `{getattr(u, 'first_name', '')}` (`{u.id}`)")

    @ubot.on(events.NewMessage(pattern=r'^\.whois2$', outgoing=True))
    async def whois2_cmd(event):
        uid = (await event.get_reply_message()).sender_id if event.is_reply else event.sender_id
        u = await ubot.get_entity(uid)
        await event.edit(f"🪪 ID: `{u.id}` | User: `@{u.username or 'N/A'}`")

    @ubot.on(events.NewMessage(pattern=r'^\.chatinfo2$', outgoing=True))
    async def chatinfo2_cmd(event):
        c = await event.get_chat()
        await event.edit(f"💬 `{getattr(c, 'title', getattr(c, 'first_name', 'Chat'))}` (`{event.chat_id}`)")

    @ubot.on(events.NewMessage(pattern=r'^\.stats2$', outgoing=True))
    async def stats2_cmd(event):
        await event.edit(f"📈 Sessions: `{len(user_sessions)}` | Raids: `{len(active_raids)}` | Up: `{format_uptime()}`")

    @ubot.on(events.NewMessage(pattern=r'^\.calc2\b', outgoing=True))
    async def calc2_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2 or not re.fullmatch(r'[0-9+\-*/().%\s]+', parts[1]):
            await event.edit("ℹ️ **Istemaal:** `.calc2 10+20`")
            return
        try:
            await event.edit(f"🧮 `{eval(parts[1], {'__builtins__': None}, {})}`")
        except Exception:
            await event.edit("❌ **Galat expression.**")

    @ubot.on(events.NewMessage(pattern=r'^\.mock2\b', outgoing=True))
    async def mock2_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        src = parts[1] if len(parts) > 1 else ((await event.get_reply_message()).raw_text if event.is_reply else "")
        if not src:
            await event.edit("ℹ️ **Text dein ya reply karein.**")
            return
        await event.edit("".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(src)))

    @ubot.on(events.NewMessage(pattern=r'^\.save2$', outgoing=True))
    async def save2_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi message par reply karke `.save2` likhein.**")
            return
        r = await event.get_reply_message()
        await ubot.send_message("me", r)
        await event.edit("✅ **Saved Messages mein bhej diya gaya.**")

    await ubot.start()
    print(f"{BOT_BRAND} session started for owner ID: {owner_id}")
    await ubot.run_until_disconnected()

# MAIN ENTRY POINT
if __name__ == '__main__':
    for uid, s_str in list(user_sessions.items()):
        try:
            loop.create_task(start_userbot_session(s_str, int(uid)))
        except Exception:
            pass
    print(f"{BOT_BRAND} started successfully for {OWNER_NAME}. Ready for connections!")
    bot.run_until_disconnected()
