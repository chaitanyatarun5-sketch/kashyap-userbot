# ==========================================
# VOLT USERBOT & HOSTING BOT V2.0 (UPDATED)
# OWNER: volt (5769074791)
# ==========================================

import os
import sys
import asyncio
import random
import re
from datetime import datetime

# Auto-install dependencies if missing on hosting platforms like Railway
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
API_ID = 39475299
API_HASH = "4203992a8c6c0aab7ad639e785f77bb5"
BOT_TOKEN = "8786112166:AAHOlxGpdXcOhBE9bdwpQsdFHkb_nBtdzqQ"  # Updated with your new token
OWNER_ID = 5769074791
OWNER_NAME = "volt"

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

# Expanding dynamically to 1000+ heavy single-word variants
GAALIS = []
modifiers = ["VALA", "SALE", "KAMINEY", "BHADWE", "MADARCHOD", "GAANDU", "CHUTIYE", "HARAMKHOR", "KAMJAT", "CHHINAR"]
for g in RAW_BASE_GAALIS:
    GAALIS.append(g)
    for m in modifiers:
        GAALIS.append(f"{g} {m}")
        GAALIS.append(f"{m} {g}")
while len(GAALIS) < 1200:
    GAALIS.extend(RAW_BASE_GAALIS)

EARAID_LIST = [
    "??MADARCHOD", "??GAANDU", "??CHUTIYA", "??BHADWA", "??RANDI",
    "??LUND", "??HIJDA", "??CHHAKKA", "??SUAR", "??KAMINEY", "??KANJAR"
] * 100

# FONT FORMATTERS
def format_araid(text):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    bold = "????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????"
    return text.upper().translate(str.maketrans(normal, bold))

def format_saraid(word):
    emojis = ["??", "??", "??", "??", "??", "??", "??", "??", "??", "??", "??"]
    res = []
    for char in word.upper():
        if char.isalpha():
            rep = "".join([char for _ in range(5)])
            res.append(f"*{rep}{random.choice(emojis)}*")
        else:
            res.append(char)
    return "".join(res)

def format_oaraid(text):
    mapping = {'A':'??','B':'??','C':'C','D':'??','E':'??','F':'??','G':'??','H':'H','I':'??','J':'??','K':'??','L':'??','M':'??','N':'N','O':'??','P':'P','Q':'Q','R':'R','S':'??','T':'??','U':'??','V':'??','W':'??','X':'??','Y':'??','Z':'Z'}
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
user_sessions = {}
active_raids = set()
active_raid_tasks = {}       # chat_id: asyncio.Task
self_reacts = {}             # chat_id: emoji (for .ar)
user_react_targets = {}      # chat_id: set of user_ids (for .uar)
all_reacts = {}              # chat_id: [emojis] (for .rar)
chat_welcomes = {}           # chat_id: {'text': str, 'media': file}

# INITIALIZE BOT CLIENT (HOSTING PANEL)
bot = TelegramClient('host_bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    welcome_text = (
        f"+----------------------+\n"
        f"  ??? **{OWNER_NAME.upper()} USERBOT HOSTING** ???\n"
        f"+----------------------+\n\n"
        f"? **HEY, I AM YOUR USERBOT MANAGER!**\n"
        f"?? Single-Word Heavy Raids & Custom Advanced Auto-Reacts loaded.\n\n"
        f"?? **Click below to host or view commands:**"
    )
    buttons = [
        [Button.inline("??? CLICK TO HOST", b"host_login"), Button.inline("?? ABOUT", b"about")],
        [Button.inline("?? GUIDE", b"guide"), Button.inline("?? SOURCE", b"source")],
        [Button.inline("?? OWNER", b"owner"), Button.inline("?? HELP AND COMMAND", b"help_cmd")]
    ]
    await event.respond(welcome_text, buttons=buttons)

@bot.on(events.CallbackQuery(data=b'about'))
async def about_cb(event):
    await event.answer("Volt Userbot V2.0 - One-Word Heavy Raid & Auto-React Bot", alert=True)

@bot.on(events.CallbackQuery(data=b'owner'))
async def owner_cb(event):
    await event.answer(f"Owner Name: {OWNER_NAME}\nOwner ID: {OWNER_ID}", alert=True)

@bot.on(events.CallbackQuery(data=b'guide'))
async def guide_cb(event):
    await event.answer("Click 'CLICK TO HOST', send your phone number with country code, then OTP & 2FA!", alert=True)

@bot.on(events.CallbackQuery(data=b'source'))
async def source_cb(event):
    await event.answer("Private Volt Userbot Source Code. Fully Optimized for Railway.", alert=True)

@bot.on(events.CallbackQuery(data=b'help_cmd'))
async def help_cb(event):
    await event.answer("Opening Help Menu...", alert=False)
    help_msg = (
        "?? **USERBOT COMMANDS & USAGE** ??\n\n"
        "• `.araid [link/tag]` - One-Word Heavy Raid\n"
        "• `.saraid / .oaraid / .faraid / .earaid` - Variant Raids\n"
        "• `.ar [emoji]` - Self Auto-React (Stop: `.dar`)\n"
        "• `.uar` (Reply or `@username`) - Target User Auto-React with `??` (Stop: `.duar`)\n"
        "• `.rar [emojis...]` - All Chat Messages Auto-React (Stop: `.drar`)\n"
        "• `/welcome [text]` (Send with pic or reply to pic) - Set Welcome Pic & Msg\n"
        "• `.stop` / `.stopall` - Stop Active Raids\n\n"
        "? Speed: **Single-Word Heavy Insults, Unlimited Continuous Mode**"
    )
    await event.respond(help_msg)

@bot.on(events.CallbackQuery(data=b'host_login'))
async def host_login_cb(event):
    await event.answer("Initializing Login Session...", alert=False)
    sender_id = event.sender_id
    async with bot.conversation(sender_id, timeout=300) as conv:
        await conv.send_message("?? **Send phone number in international format:**\n`+91XXXXXXXXXX`")
        phone_msg = await conv.get_response()
        phone = phone_msg.text.strip()
        
        client = TelegramClient(StringSession(), API_ID, API_HASH)
        await client.connect()
        
        try:
            sent = await client.send_code_request(phone)
        except Exception as e:
            await conv.send_message(f"? Error sending code: `{e}`")
            await client.disconnect()
            return
        
        await conv.send_message("? **Code sent!** Please send the OTP code received on Telegram:")
        code_msg = await conv.get_response()
        code = "".join(code_msg.text.split())
        
        try:
            await client.sign_in(phone, code, phone_code_hash=sent.phone_code_hash)
        except SessionPasswordNeededError:
            await conv.send_message("?? **2-Step Verification detected!** Please send your password:")
            pwd_msg = await conv.get_response()
            password = pwd_msg.text.strip()
            try:
                await client.sign_in(password=password)
            except Exception as e:
                await conv.send_message(f"? 2FA Password error: `{e}`")
                await client.disconnect()
                return
        except Exception as e:
            await conv.send_message(f"? Sign in error: `{e}`")
            await client.disconnect()
            return
        
        session_str = client.session.save()
        user_sessions[sender_id] = session_str
        
        asyncio.create_task(start_userbot_session(session_str, sender_id))
        
        await conv.send_message(
            f"? **Hosted done successfully!**\n"
            f"? Active commands loaded: `.araid`, `.ar`, `.dar`, `.uar`, `.duar`, `.rar`, `.drar`, `/welcome`, `.stopall`\n"
            f"?? Logged in for: **{OWNER_NAME}**"
        )

# DYNAMIC USERBOT SESSION RUNNER
async def start_userbot_session(session_string, owner_id):
    ubot = TelegramClient(StringSession(session_string), API_ID, API_HASH)
    
    # WELCOME FEATURE: SET WELCOME WITH PIC & TEXT
    @ubot.on(events.NewMessage(outgoing=True, pattern=r'^\/welcome'))
    async def set_welcome_handler(event):
        chat_id = event.chat_id
        text_arg = event.raw_text.replace('/welcome', '').strip()
        
        if event.is_reply:
            reply = await event.get_reply_message()
            text = text_arg or (reply.text if reply and reply.text else "Welcome to the group! ??")
            if reply and reply.media:
                chat_welcomes[chat_id] = {'text': text, 'media': reply.media}
                await event.edit("? **Welcome photo & message set successfully for this chat!**")
            else:
                chat_welcomes[chat_id] = {'text': text, 'media': None}
                await event.edit("? **Welcome text set successfully! (Reply to a photo to include image)**")
        elif event.media:
            text = text_arg or "Welcome to the group! ??"
            chat_welcomes[chat_id] = {'text': text, 'media': event.media}
            await event.edit("? **Welcome photo & message set successfully for this chat!**")
        else:
            await event.edit("? **Usage:** Send a photo with caption `/welcome [text]` or reply to a photo with `/welcome [text]`")

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
            await event.edit(f"? **Self Auto-React Enabled with emoji:** `{emoji}`")
        else:
            await event.edit("? Usage: `.ar [emoji]` (Ex: `.ar ??`)")

    @ubot.on(events.NewMessage(pattern=r'^\.dar$', outgoing=True))
    async def dar_command(event):
        chat_id = event.chat_id
        if chat_id in self_reacts:
            del self_reacts[chat_id]
            await event.edit("?? **Self Auto-React Stopped.**")
        else:
            await event.edit("? Self auto-react is not active here.")

    # 2. AUTO-REACT (B): Target User Auto-React with '??'
    @ubot.on(events.NewMessage(incoming=True))
    async def uar_incoming_handler(event):
        chat_id = event.chat_id
        sender_id = event.sender_id
        if chat_id in user_react_targets and sender_id in user_react_targets[chat_id]:
            try:
                await event.react("??")
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
                await event.edit("? Invalid user or username!")
                return

        if target_user:
            if chat_id not in user_react_targets:
                user_react_targets[chat_id] = set()
            user_react_targets[chat_id].add(target_user)
            await event.edit("? **User Auto-React Enabled (`??`) for targeted user!**")
        else:
            await event.edit("? Usage: Reply to a user or use `.uar @username`")

    @ubot.on(events.NewMessage(pattern=r'^\.duar$', outgoing=True))
    async def duar_command(event):
        chat_id = event.chat_id
        if chat_id in user_react_targets:
            del user_react_targets[chat_id]
            await event.edit("?? **User Auto-React Stopped for this chat.**")
        else:
            await event.edit("? No active user auto-react in this chat.")

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
            await event.edit("? Usage: `.rar ?? ?? ??`")
            return
        all_reacts[chat_id] = emojis
        await event.edit(f"? **All Message Auto-React Enabled with emojis:** `{' '.join(emojis)}`")

    @ubot.on(events.NewMessage(pattern=r'^\.drar$', outgoing=True))
    async def drar_command(event):
        chat_id = event.chat_id
        if chat_id in all_reacts:
            del all_reacts[chat_id]
            await event.edit("?? **All-Message Auto-React Stopped.**")
        else:
            await event.edit("? No active all-message auto-react in this chat.")

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
                await event.edit("?? **Raid Stopped in this chat!**")
            except Exception:
                pass
        else:
            try:
                await event.edit("? No active raid in this chat.")
            except Exception:
                pass

    @ubot.on(events.NewMessage(pattern=r'^\.stopall$', outgoing=True))
    async def stop_all_raids(event):
        active_raids.clear()
        for chat_id, task in active_raid_tasks.items():
            task.cancel()
        active_raid_tasks.clear()
        try:
            await event.edit("?? **All Raids Stopped Globally!**")
        except Exception:
            pass

    await ubot.start()
    print(f"Userbot session started for owner ID: {owner_id}")
    await ubot.run_until_disconnected()

# MAIN ENTRY POINT
if __name__ == '__main__':
    print(f"Volt Hosting Bot started successfully for {OWNER_NAME}. Ready for connections!")
    bot.run_until_disconnected()
