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
        self.wfile.write(b"Bot is Live!")
    def log_message(self, *a):
        pass

def run_web():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), H).serve_forever()

threading.Thread(target=run_web, daemon=True).start()

# ==========================================
# VILLIAN USERBOT & HOSTING BOT V2.0 (UPDATED)
# OWNER: kashayap (5769074791)
# ==========================================

try:
    import telethon
except ImportError:
    os.system(f"{sys.executable} -m pip install telethon")
    import telethon

from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PhoneNumberInvalidError, FloodWaitError
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

# CONFIGURATION
API_ID = 39105091
API_HASH = "257594e70a9926b6bb44644e17be94a9"
BOT_TOKEN = "9241124031:AAFa6bpjJSq_gGhYgRDqrxjEbFcvsZiYcl4"
OWNER_ID = 9239452757
OWNER_NAME = "KASHYAP"
START_TIME = time.time()
SESSIONS_FILE = "sessions.json"

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

ROAST_LINES = [
    "Tumhari baatein sun kar lagta hai Wi-Fi slow chal raha hai.",
    "Itna confident mat ho, mirror bhi kabhi kabhi shock mein aa jata hai.",
    "Aapki argument aisi hai jaise bina battery ka remote.",
    "Bolne se pehle ek baar mute button check kar liya karo."
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

# INITIALIZE BOT CLIENT (HOSTING PANEL)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
bot = TelegramClient('host_bot_session', API_ID, API_HASH, loop=loop).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    welcome_text = (
        f"+----------------------+\n"
        f"  ⚡ **{OWNER_NAME.upper()} USERBOT HOSTING** ⚡\n"
        f"+----------------------+\n\n"
        f"🔥 **HEY, I AM YOUR USERBOT MANAGER!**\n"
        f"💀 Single-Word Heavy Raids, Multi-Lang Raids, Hack/Anim & Auto-Reacts loaded.\n\n"
        f"👇 **Click below to host or view commands:**"
    )
    buttons = [
        [Button.inline("⚡ CLICK TO HOST", b"host_login"), Button.inline("ℹ️ ABOUT", b"about")],
        [Button.inline("📖 GUIDE", b"guide"), Button.inline("💻 SOURCE", b"source")],
        [Button.inline("👑 OWNER", b"owner"), Button.inline("📜 HELP AND COMMAND", b"help_cmd")]
    ]
    await event.respond(welcome_text, buttons=buttons)

@bot.on(events.CallbackQuery(data=b'about'))
async def about_cb(event):
    await event.answer("Volt Userbot V2.0 - Heavy Raid, Hack, Anim & Auto-React Bot", alert=True)

@bot.on(events.CallbackQuery(data=b'owner'))
async def owner_cb(event):
    await event.answer(f"Owner Name: {OWNER_NAME}\nOwner ID: {OWNER_ID}", alert=True)

@bot.on(events.CallbackQuery(data=b'guide'))
async def guide_cb(event):
    await event.answer("Click 'CLICK TO HOST', send your phone number with country code, then OTP & 2FA!", alert=True)

@bot.on(events.CallbackQuery(data=b'source'))
async def source_cb(event):
    await event.answer("Private VILLIAN Userbot Source Code. Fully Optimized for Hosting.", alert=True)

@bot.on(events.CallbackQuery(data=b'help_cmd'))
async def help_cb(event):
    await event.answer("Opening Help Menu...", alert=False)
    help_msg = (
        "📜 **USERBOT COMMANDS & USAGE** 📜\n\n"
        "• `.raid [count]` / `.oneraid [count]` (Reply) - Heavy & Single-Word Raid\n"
        "• `.rraid` / `.drraid` (Reply) - Auto-Reply Raid On/Off\n"
        "• `.spam` / `.fastspam` / `.flood [count] [text]` - Spam Variants\n"
        "• `.engraid` / `.praid` / `.braid [count]` - English, Punjabi & Bengali Raids\n"
        "• `.araid / .saraid / .oaraid / .faraid / .earaid` - Styled Variant Raids\n"
        "• `.dmraid [count]` (Reply) / `.mraid [count]` / `.delayraid [sec] [count]` - Extra Raids\n"
        "• `.emoraid [count]` / `.emojispam [count] [emoji] [text]` - Emoji Raids\n"
        "• `.mixraid [1-50]` / `.tagraid [1-50]` / `.capsraid [1-50]` / `.slowraid [1-50]` - Max-50 Raids\n"
        "• `.hack` / `.matrix` / `.scan` / `.bruteforce [1-50]` / `.packetflood [1-50]` / `.sysbreach [1-50]`\n"
        "• `.loading` / `.boom` / `.fbi` / `.pulse [1-50]` / `.countanim [1-50]` / `.glitch [1-50]`\n"
        "• `.roast` / `.iq` / `.love` / `.toss` / `.dice` / `.calc [expr]` / `.type [text]` / `.mock [text]`\n"
        "• `.ping` / `.alive` / `.id` / `.info` / `.afk [reason]` / `.save`\n"
        "• `.dmblock on|off` / `.dmmute` / `.undmmute` - DM Control\n"
        "• `.ar` / `.dar` / `.uar` / `.duar` / `.rar` / `.drar` - Auto-Reacts\n"
        "• `/welcome [text]` - Set Welcome Pic & Msg\n"
        "• `.stop` / `.stopall` - Stop Active Raids"
    )
    await event.respond(help_msg)

@bot.on(events.CallbackQuery(data=b'host_login'))
async def host_login_cb(event):
    await event.answer("Initializing Login Session...", alert=False)
    sender_id = event.sender_id
    async with bot.conversation(sender_id, timeout=300) as conv:
        await conv.send_message("📱 **Send phone number in international format:**\n`+91XXXXXXXXXX`")
        phone_msg = await conv.get_response()
        phone = phone_msg.text.strip()

        client = TelegramClient(StringSession(), API_ID, API_HASH)
        await client.connect()

        try:
            sent = await client.send_code_request(phone)
        except Exception as e:
            await conv.send_message(f"❌ Error sending code: `{e}`")
            await client.disconnect()
            return

        await conv.send_message("✅ **Code sent!** Please send the OTP code received on Telegram:")
        code_msg = await conv.get_response()
        code = "".join(code_msg.text.split())

        try:
            await client.sign_in(phone, code, phone_code_hash=sent.phone_code_hash)
        except SessionPasswordNeededError:
            await conv.send_message("🔐 **2-Step Verification detected!** Please send your password:")
            pwd_msg = await conv.get_response()
            password = pwd_msg.text.strip()
            try:
                await client.sign_in(password=password)
            except Exception as e:
                await conv.send_message(f"❌ 2FA Password error: `{e}`")
                await client.disconnect()
                return
        except Exception as e:
            await conv.send_message(f"❌ Sign in error: `{e}`")
            await client.disconnect()
            return

        session_str = client.session.save()
        user_sessions[str(sender_id)] = session_str
        save_sessions_to_disk(user_sessions)

        asyncio.create_task(start_userbot_session(session_str, sender_id))

        await conv.send_message(
            f"✅ **Hosted done successfully!**\n"
            f"⚡ Active commands loaded: `.raid`, `.oneraid`, `.rraid`, `.drraid`, `.spam`, `.fastspam`, `.flood`, `.engraid`, `.praid`, `.braid`, `.araid`, `.dmraid`, `.emoraid`, `.mixraid`, `.hack`, `.pulse`, `.afk`, `.ar`, `.uar`, `.rar`, `/welcome`, `.stopall`\n"
            f"👑 Logged in for: **{OWNER_NAME}**"
        )

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
            text = text_arg or (reply.text if reply and reply.text else "Welcome to the group! 👋")
            if reply and reply.media:
                chat_welcomes[chat_id] = {'text': text, 'media': reply.media}
                await event.edit("✅ **Welcome photo & message set successfully for this chat!**")
            else:
                chat_welcomes[chat_id] = {'text': text, 'media': None}
                await event.edit("✅ **Welcome text set successfully! (Reply to a photo to include image)**")
        elif event.media:
            text = text_arg or "Welcome to the group! 👋"
            chat_welcomes[chat_id] = {'text': text, 'media': event.media}
            await event.edit("✅ **Welcome photo & message set successfully for this chat!**")
        else:
            await event.edit("❌ **Usage:** Send a photo with caption `/welcome [text]` or reply to a photo with `/welcome [text]`")

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

    @ubot.on(events.NewMessage(pattern=r'^\.ar\b', outgoing=True))
    async def ar_command(event):
        args = event.raw_text.split()
        chat_id = event.chat_id
        if len(args) > 1:
            emoji = args[1]
            self_reacts[chat_id] = emoji
            await event.edit(f"✅ **Self Auto-React Enabled with emoji:** `{emoji}`")
        else:
            await event.edit("❌ Usage: `.ar [emoji]` (Ex: `.ar 🔥`)")

    @ubot.on(events.NewMessage(pattern=r'^\.dar$', outgoing=True))
    async def dar_command(event):
        chat_id = event.chat_id
        if chat_id in self_reacts:
            del self_reacts[chat_id]
            await event.edit("🛑 **Self Auto-React Stopped.**")
        else:
            await event.edit("❌ Self auto-react is not active here.")

    # 2. AUTO-REACT (B): Target User Auto-React with '🔥'
    @ubot.on(events.NewMessage(incoming=True))
    async def uar_incoming_handler(event):
        chat_id = event.chat_id
        sender_id = event.sender_id
        if chat_id in user_react_targets and sender_id in user_react_targets[chat_id]:
            try:
                await event.react("🔥")
            except Exception:
                pass

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
                await event.edit("❌ Invalid user or username!")
                return

        if target_user:
            if chat_id not in user_react_targets:
                user_react_targets[chat_id] = set()
            user_react_targets[chat_id].add(target_user)
            await event.edit("✅ **User Auto-React Enabled (`🔥`) for targeted user!**")
        else:
            await event.edit("❌ Usage: Reply to a user or use `.uar @username`")

    @ubot.on(events.NewMessage(pattern=r'^\.duar$', outgoing=True))
    async def duar_command(event):
        chat_id = event.chat_id
        if chat_id in user_react_targets:
            del user_react_targets[chat_id]
            await event.edit("🛑 **User Auto-React Stopped for this chat.**")
        else:
            await event.edit("❌ No active user auto-react in this chat.")

    # 3. AUTO-REACT (C): All Messages Auto-React with selected reactions
    @ubot.on(events.NewMessage(incoming=True))
    async def rar_incoming_handler(event):
        chat_id = event.chat_id
        if chat_id in all_reacts and all_reacts[chat_id]:
            emoji = random.choice(all_reacts[chat_id])
            try:
                await event.react(emoji)
            except Exception:
                pass

    @ubot.on(events.NewMessage(pattern=r'^\.rar\b', outgoing=True))
    async def rar_command(event):
        args = event.raw_text.split()
        chat_id = event.chat_id
        emojis = args[1:]
        if not emojis:
            await event.edit("❌ Usage: `.rar 🔥 💀 ⚡`")
            return
        all_reacts[chat_id] = emojis
        await event.edit(f"✅ **All Message Auto-React Enabled with emojis:** `{' '.join(emojis)}`")

    @ubot.on(events.NewMessage(pattern=r'^\.drar$', outgoing=True))
    async def drar_command(event):
        chat_id = event.chat_id
        if chat_id in all_reacts:
            del all_reacts[chat_id]
            await event.edit("🛑 **All-Message Auto-React Stopped.**")
        else:
            await event.edit("❌ No active all-message auto-react in this chat.")

    # 4. REPLY RAID (.rraid / .drraid)
    @ubot.on(events.NewMessage(pattern=r'^\.rraid$', outgoing=True))
    async def rraid_start_cmd(event):
        if not event.is_reply:
            await event.edit("❌ Reply to a user's message with `.rraid`.")
            return
        reply = await event.get_reply_message()
        if not reply.sender_id:
            await event.edit("❌ Target user ID not found.")
            return
        rraid_targets.add((event.chat_id, reply.sender_id))
        await event.edit(f"✅ **RRAID Enabled** for `{reply.sender_id}`!")

    @ubot.on(events.NewMessage(pattern=r'^\.drraid$', outgoing=True))
    async def rraid_stop_cmd(event):
        if event.is_reply:
            reply = await event.get_reply_message()
            rraid_targets.discard((event.chat_id, reply.sender_id))
            await event.edit(f"🛑 **RRAID Stopped** for `{reply.sender_id}`.")
        else:
            for item in [x for x in rraid_targets if x[0] == event.chat_id]:
                rraid_targets.discard(item)
            await event.edit("🛑 **All RRAID stopped in this chat.**")

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
            await event.edit(f"❌ Usage: `.{cmd} [count] [text]`")
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
            await event.edit("❌ Reply to a user's message with `.dmraid [count]`.")
            return
        reply = await event.get_reply_message()
        if not reply.sender_id:
            await event.edit("❌ User ID not found.")
            return
        parts = event.raw_text.split()
        count = max(1, min(int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 15, 100))
        await event.edit(f"📩 Sending {count} DM raid messages...")
        for _ in range(count):
            try:
                await ubot.send_message(reply.sender_id, random.choice(GAALIS))
                await asyncio.sleep(0.35)
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
            except Exception:
                break
        await event.edit("✅ **DM Raid Completed!**")

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
            await event.edit("❌ Usage: `.delayraid [seconds] [count]`")
            return
        try:
            delay = max(0.2, min(float(parts[1]), 10.0))
            count = max(1, min(int(parts[2]), 200))
        except Exception:
            await event.edit("❌ Invalid numbers.")
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
            await event.edit("❌ Usage: `.emojispam [count] [emoji] [text]`")
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
            await event.edit("❌ Use this inside a group.")
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

    # 9. DM CONTROL (.dmblock, .dmmute, .undmmute) & AFK
    @ubot.on(events.NewMessage(pattern=r'^\.dmblock\b', outgoing=True))
    async def dmblock_cmd(event):
        parts = event.raw_text.split()
        if len(parts) < 2 or parts[1].lower() not in ("on", "off"):
            await event.edit("❌ Usage: `.dmblock on|off`")
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
            await event.edit("❌ Use in DM or reply to a user.")
            return
        dm_muted_users[owner_id].add(target_id)
        await event.edit(f"🔇 **Muted in DM:** `{target_id}`")

    @ubot.on(events.NewMessage(pattern=r'^\.undmmute$', outgoing=True))
    async def undmmute_cmd(event):
        target_id = event.chat_id if event.is_private else None
        if event.is_reply:
            r = await event.get_reply_message()
            target_id = r.sender_id
        if target_id and target_id in dm_muted_users[owner_id]:
            dm_muted_users[owner_id].remove(target_id)
            await event.edit(f"🔊 **Unmuted in DM:** `{target_id}`")
        else:
            await event.edit("❌ User is not muted.")

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
                    from telethon.tl.functions.contacts import BlockRequest
                    await ubot(BlockRequest(event.sender_id))
                except Exception:
                    pass
                return
        if owner_id in afk_status and (event.is_private or event.mentioned):
            try:
                await event.reply(f"💤 **I am currently AFK:** {afk_status[owner_id]}")
            except Exception:
                pass

    @ubot.on(events.NewMessage(pattern=r'^\.afk\b', outgoing=True))
    async def afk_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        reason = parts[1] if len(parts) > 1 else "Busy right now"
        afk_status[owner_id] = reason
        await event.edit(f"💤 **AFK Enabled:** `{reason}`")

    # 10. HACK & ANIMATION COMMANDS (INCLUDING MAX-50 STEPS)
    @ubot.on(events.NewMessage(pattern=r'^\.hack$', outgoing=True))
    async def hack_cmd(event):
        steps = [
            "💻 `Initializing exploit framework...`",
            "🔓 `Bypassing firewall rules... 34%`",
            "📡 `Injecting payload into target node... 78%`",
            "✅ `Access granted (Simulated Demo).`"
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
            await event.edit(f"🔍 `Scanning target ports... {pct}%`")
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
                txt = f"🔐 `Bruteforcing PIN [{i}/{steps}] -> {str(i).zfill(4)}`"
            elif cmd == "packetflood":
                txt = f"📡 `Sending packet [{i}/{steps}] -> 192.168.1.{i}:443`"
            elif cmd == "sysbreach":
                txt = f"🛡️ `Breach stage [{i}/{steps}] -> {int((i/steps)*100)}%`"
            elif cmd == "pulse":
                icon = pulse_icons[i % len(pulse_icons)]
                txt = f"{icon} **PULSE [{i}/{steps}]** {icon}"
            elif cmd == "countanim":
                txt = f"🔢 **Counter:** `{i} / {steps}`"
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
        for line in ["🚨 **FBI OPEN UP!** 🚨", "🚔 `Perimeter secured...`", "📡 `Tracking signal...`"]:
            await event.edit(line)
            await asyncio.sleep(0.5)

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
        await event.edit(f"🧠 **IQ Score:** `{random.randint(1, 150)}%`")

    @ubot.on(events.NewMessage(pattern=r'^\.love$', outgoing=True))
    async def love_cmd(event):
        await event.edit(f"❤️ **Compatibility:** `{random.randint(1, 100)}%`")

    @ubot.on(events.NewMessage(pattern=r'^\.toss$', outgoing=True))
    async def toss_cmd(event):
        await event.edit(f"🪙 **Coin Toss:** `{random.choice(['Heads', 'Tails'])}`")

    @ubot.on(events.NewMessage(pattern=r'^\.dice$', outgoing=True))
    async def dice_cmd(event):
        await event.edit(f"🎲 **Dice Rolled:** `{random.randint(1, 6)}`")

    @ubot.on(events.NewMessage(pattern=r'^\.ping$', outgoing=True))
    async def ping_cmd(event):
        t0 = time.time()
        msg = await event.edit("🏓 `Pinging...`")
        ms = int((time.time() - t0) * 1000)
        await msg.edit(f"🏓 **Pong:** `{ms} ms`")

    @ubot.on(events.NewMessage(pattern=r'^\.alive$', outgoing=True))
    async def alive_cmd(event):
        uptime = int(time.time() - START_TIME)
        await event.edit(f"⚡ **{OWNER_NAME} Userbot is Alive!**\n⏱️ **Uptime:** `{uptime}s`")

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
            await event.edit(
                f"👤 **User Info**\n"
                f"• **ID:** `{u.id}`\n"
                f"• **Name:** `{getattr(u, 'first_name', '')}`\n"
                f"• **Username:** `@{u.username}`" if getattr(u, 'username', None) else f"• **ID:** `{u.id}`\n• **Name:** `{getattr(u, 'first_name', '')}`"
            )
        except Exception as e:
            await event.edit(f"❌ Error: `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.calc\b', outgoing=True))
    async def calc_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2 or not re.fullmatch(r'[0-9+\-*/().%\s]+', parts[1]):
            await event.edit("❌ Usage: `.calc 25*4`")
            return
        try:
            ans = eval(parts[1], {"__builtins__": None}, {})
            await event.edit(f"🧮 `{parts[1]}` = **`{ans}`**")
        except Exception:
            await event.edit("❌ Invalid math expression.")

    @ubot.on(events.NewMessage(pattern=r'^\.type\b', outgoing=True))
    async def type_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2:
            await event.edit("❌ Usage: `.type hello`")
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
            await event.edit("❌ Give text or reply to a message.")
            return
        out = "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(src))
        await event.edit(out)

    @ubot.on(events.NewMessage(pattern=r'^\.save$', outgoing=True))
    async def save_cmd(event):
        if not event.is_reply:
            await event.edit("❌ Reply to a message/media with `.save`.")
            return
        r = await event.get_reply_message()
        try:
            await ubot.send_message("me", r)
            await event.edit("💾 **Saved to Saved Messages!**")
        except Exception as e:
            await event.edit(f"❌ Could not save: `{e}`")

    # Background Continuous/Unlimited Raid Worker Loop with Single-Word Insults
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

            text = base_text

            try:
                if reply_to:
                    await ubot.send_message(target_chat, text, reply_to=reply_to)
                else:
                    await ubot.send_message(target_chat, text)
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
            except Exception:
                await asyncio.sleep(0.5)

            iteration += 1
            await asyncio.sleep(1.1 / 8)

        if target_chat in active_raids:
            active_raids.remove(target_chat)
        if target_chat in active_raid_tasks:
            del active_raid_tasks[target_chat]

    # Raid Handler with Advanced Link / Target & Optional Count Parsing
    @ubot.on(events.NewMessage(pattern=r'^\.(araid|saraid|oaraid|faraid|earaid)', outgoing=True))
    async def raid_handler(event):
        command = event.pattern_match.group(1)
        args = event.raw_text.split()

        target_chat = event.chat_id
        reply_to = event.reply_to_msg_id
        count = None  # Default to continuous/unlimited
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
                await event.edit("🛑 **Raid Stopped in this chat!**")
            except Exception:
                pass
        else:
            try:
                await event.edit("❌ No active raid in this chat.")
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
            await event.edit("🛑 **All Raids Stopped Globally!**")
        except Exception:
            pass

    await ubot.start()
    print(f"Userbot session started for owner ID: {owner_id}")
    await ubot.run_until_disconnected()

# MAIN ENTRY POINT
if __name__ == '__main__':
    for uid, s_str in list(user_sessions.items()):
        try:
            loop.create_task(start_userbot_session(s_str, int(uid)))
        except Exception:
            pass
    print(f"Volt Hosting Bot started successfully for {OWNER_NAME}. Ready for connections!")
    bot.run_until_disconnected()
