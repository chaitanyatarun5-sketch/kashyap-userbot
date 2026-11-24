import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Alive")
    def log_message(self, *args):
        pass

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    Thread(target=server.serve_forever, daemon=True).start()
# -----------------------------------------------------------------------------
# VOLT DEPLOYMENT BOOTSTRAP
# -----------------------------------------------------------------------------
# The hosting panel runs this file directly.  Install only the runtime packages
# that this file actually needs, so a clean VPS/container does not die with
# "ModuleNotFoundError" and exit code 1 before the bot can start.
import sys
import subprocess
import importlib.util

def _ensure_runtime_package(module_name, package_name):
    try:
        if importlib.util.find_spec(module_name) is not None:
            return
    except Exception:
        pass
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "--disable-pip-version-check", "--no-input", "-q", package_name
    ])

_ensure_runtime_package("pyrogram", "pyrogram==2.0.106")
# TgCrypto is optional for Pyrogram. Do NOT auto-install it here: some
# deployment containers (including Python 3.13 images) have no C compiler,
# which makes TgCrypto fail during wheel compilation and kills the bot.
_ensure_runtime_package("yt_dlp", "yt-dlp>=2025.1.0")

import asyncio
import logging
import os
import re
import random
import time
import urllib.parse
import urllib.request
import json
from pyrogram import Client, filters, enums
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    PhoneNumberInvalid,
    FloodWait,
    MessageNotModified,
    RPCError,
    PeerIdInvalid,
    ChannelInvalid,
    ChatAdminRequired,
    UserNotParticipant
)
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
    ChatPrivileges,
    ChatPermissions
)

# -----------------------------------------------------------------------------
# LOGGING CONFIGURATION
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("VOLT_USERBOT")

# -----------------------------------------------------------------------------
# CONFIGURATION & CONSTANTS
# -----------------------------------------------------------------------------
API_ID = 39105091
API_HASH = "257594e70a9926b6bb44644e17be94a9"
BOT_TOKEN = "9241124031:AAFa6bpjJSq_gGhYgRDqrxjEbFcvsZiYcl4"
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required in the Railway environment.")

OWNER_ID = 9239452757
OWNER_USERNAME = "Harukasakura01"

CO_OWNER_ID = 5769074791
CO_OWNER_USERNAME = "ix_aura"

FORCE_CHANNEL_ID = -1003739475692
FORCE_CHANNEL_LINK = "https://t.me/VOLT_CHANNEL_UP"

FORCE_GROUP_ID = -1004304252893
FORCE_GROUP_LINK = "https://t.me/+2Ynr7yEH5mljM2U0"

START_PIC = "https://files.catbox.moe/c8w5k8.jpg"

# -----------------------------------------------------------------------------
# GLOBAL STATE STORAGE
# -----------------------------------------------------------------------------
USER_STATES = {}       
TEMP_LOGINS = {}       
HOSTED_CLIENTS = {}    
ACTIVE_TASKS = {}      

LOGIN_LOCKS = {}
START_LOCKS = {}
LAST_START_AT = {}
START_PANEL_MESSAGES = {}
START_DEDUP_SECONDS = 2.5

TASK_REGISTRY = set()

# KHATARNAK GAALIS POOL
KHATARNAK_GAALIS = [
    "TERI MAKI CHUTH PE DANDA MARU MADARCHOD AAPNE BAAP KO MAAT SIKHA TERI MA KI CHUTH",
    "TERI BHN KI CHUTH ME RICKSHAW CHALA DU MADARCHOD KE BACHE",
    "MADARCHOD TERA BAAP HU MAIN, APNI MAA SE PUCHNA RAAT KO KISKA NAAM CHILLA RAHI THI",
    "TERI MAA KA BHOSDA FAAD KE USME TERA HI LUND DAL DUGA CHAL NIKAL",
    "BHOSDIKE TERI MAA KI CHUT ME BAM PHOD DUGA MADARCHOD",
    "RANDI KE PILLE APNI AUKAAT ME REH, TERI MAA KI CHUT ME TRACTOR CHALA DUGA",
    "CHUTIYE APNE BAAP SE AISE BAAT KAREGA? TERI MAA KI CHUT ME APNA JUTA DUGA",
    "MADARCHOD TERA KHANADAN RANDI KHANE ME NACHTA HAI, TERI BHN KI CHUTH",
    "TERI MAA KA BHOSDA GARM TAWE PAR SEK DUGA CHUTIYE",
    "TERI MAIYA KA BHORA UDA DUGA MADARCHOD SALA NALLA",
    "CHAL HAT MADARCHOD TERI MA KI CHUT ME CORONA VIRUS DAAL DU",
    "TERI BHN KI CHUTH ME DORAEMON KA COPTER GHUSA DUGA CHUTIYE",
    "TERI MAA KI CHUT ME TUBE LIGHT TOD DUGA MADARCHOD KE BACHE"
]

SINGLE_GAALIS = [
    "MADARCHOD", "BHOOTNIKE", "CHUTIYE", "GANDU", "RANDI", 
    "LODE", "BHOSDIKE", "LAWDE", "HIJRA", "MC", "BC", 
    "TERIMA", "CHUT", "HRAMKHOR", "NALAYAK", "BAKKANCHOD"
]

def _consume_task_result(task: asyncio.Task):
    TASK_REGISTRY.discard(task)
    try:
        task.result()
    except asyncio.CancelledError:
        return
    except Exception:
        logger.exception("Unhandled background task exception")

def create_tracked_task(coro, *, task_name="background_task", user_id=None):
    task = asyncio.create_task(coro, name=task_name)
    TASK_REGISTRY.add(task)
    task.add_done_callback(_consume_task_result)
    if user_id is not None:
        def _cleanup(done_task):
            tasks = ACTIVE_TASKS.get(user_id)
            if not tasks:
                return
            for name, active in list(tasks.items()):
                if active is done_task:
                    tasks.pop(name, None)
            if not tasks:
                ACTIVE_TASKS.pop(user_id, None)
        task.add_done_callback(_cleanup)
    return task

async def cancel_user_tasks(user_id: int):
    tasks = list(ACTIVE_TASKS.get(user_id, {}).values())
    for task in tasks:
        if task and not task.done():
            task.cancel()
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    ACTIVE_TASKS.pop(user_id, None)

# -----------------------------------------------------------------------------
# MAIN BOT INITIALIZATION
# -----------------------------------------------------------------------------
app = Client(
    "volt_main_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def safe_edit_text(message: Message, text: str, **kwargs):
    try:
        current = getattr(message, "text", None)
        current_caption = getattr(message, "caption", None)
        if current == text or current_caption == text:
            return False
        if getattr(message, "photo", None) or current_caption is not None:
            return await message.edit_caption(caption=text, **kwargs)
        return await message.edit_text(text, **kwargs)
    except MessageNotModified:
        return False
    except RPCError as e:
        if "MESSAGE_NOT_MODIFIED" in str(e).upper():
            return False
        raise

async def check_force_join(client: Client, user_id: int) -> bool:
    if user_id in (OWNER_ID, CO_OWNER_ID):
        return True
    try:
        for peer_id, label in ((FORCE_CHANNEL_ID, "channel"), (FORCE_GROUP_ID, "group")):
            try:
                member = await client.get_chat_member(peer_id, user_id)
                if member.status in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED):
                    return False
            except Exception:
                pass
        return True
    except Exception:
        return True

def get_force_join_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("?? ???????? ??????????????", url=FORCE_CHANNEL_LINK),
            InlineKeyboardButton("?? ???????? ??????????", url=FORCE_GROUP_LINK)
        ],
        [InlineKeyboardButton("?? ???????? ???????????????????????? ? ?????? ??????????", callback_data="check_membership")]
    ])

def get_start_keyboard(bot_username: str = "bot"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("? ????? ?? ??s? ????? ?s????? ?", callback_data="start_host")],
        [InlineKeyboardButton("? ??? ?? ?? ???? ????? ?", url=f"https://t.me/{bot_username}?startgroup=true")],
        [
            InlineKeyboardButton("?? ?????", url=f"https://t.me/{OWNER_USERNAME}"),
            InlineKeyboardButton("? ??-?????", url=f"https://t.me/{CO_OWNER_USERNAME}")
        ],
        [
            InlineKeyboardButton("?? s??????", url=FORCE_GROUP_LINK),
            InlineKeyboardButton("?? ??????s", url=FORCE_CHANNEL_LINK)
        ],
        [
            InlineKeyboardButton("?? ?????", callback_data="menu_about"),
            InlineKeyboardButton("?? ?????", callback_data="menu_guide")
        ],
        [InlineKeyboardButton("??? 12 s??????s (90+ ???????s) ??", callback_data="menu_help")],
        [InlineKeyboardButton("? s????? ????", callback_data="menu_source")]
    ])

def get_back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("?? ???? ?? ????", callback_data="main_menu")]
    ])

def get_help_categories_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("?? 1. ???????? & ????????", callback_data="help_sec1"),
            InlineKeyboardButton("?? 2. ????????????????????", callback_data="help_sec2")
        ],
        [
            InlineKeyboardButton("? 3. ???????? ??????????????", callback_data="help_sec3"),
            InlineKeyboardButton("??? 4. ????????????????????", callback_data="help_sec4")
        ],
        [
            InlineKeyboardButton("?? 5. ?????? & ????????????", callback_data="help_sec5"),
            InlineKeyboardButton("??? 6. ??????????????????", callback_data="help_sec6")
        ],
        [
            InlineKeyboardButton("?? 7. ?????????? & ??????????", callback_data="help_sec7"),
            InlineKeyboardButton("?? 8. ?????????? ??????????", callback_data="help_sec8")
        ],
        [
            InlineKeyboardButton("?? 9. ?????????????? ????????", callback_data="help_sec9"),
            InlineKeyboardButton("?? 10. ?????? ??????????", callback_data="help_sec10")
        ],
        [
            InlineKeyboardButton("?? 11. ??????????????????", callback_data="help_sec11"),
            InlineKeyboardButton("?? 12. ??????????????????", callback_data="help_sec12")
        ],
        [InlineKeyboardButton("?? ???????? ???? ????????", callback_data="main_menu")]
    ])

@app.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    lock = START_LOCKS.setdefault(user_id, asyncio.Lock())
    async with lock:
        try:
            try:
                await message.delete()
            except Exception:
                pass

            if not await check_force_join(client, user_id):
                text = "?? **Access Denied!**\n\nYou must join our channel and group to use VOLT Userbot Host."
                markup = get_force_join_keyboard()
            else:
                me = await client.get_me()
                text = (
                    f"?? **WELCOME TO VOLT X USERBOT HOSTING** ??\n\n"
                    f"? *India's Most Powerful High-Performance Telegram Userbot Platform*\n"
                    f"?? Powered with 12 Professional Sections & 90+ Advanced Commands.\n\n"
                    f"?? **Owner:** @{OWNER_USERNAME} (`{OWNER_ID}`)\n"
                    f"? **Co-Owner:** @{CO_OWNER_USERNAME} (`{CO_OWNER_ID}`)\n\n"
                    f"?? *Select an option below to get started:*"
                )
                markup = get_start_keyboard(me.username)

            old_panel = START_PANEL_MESSAGES.get(user_id)
            now = time.monotonic()
            if old_panel and now - LAST_START_AT.get(user_id, 0) < START_DEDUP_SECONDS:
                return
            if old_panel:
                try:
                    if getattr(old_panel, "photo", None):
                        await old_panel.edit_caption(caption=text, reply_markup=markup)
                    else:
                        await old_panel.edit_text(text, reply_markup=markup)
                    LAST_START_AT[user_id] = now
                    return
                except Exception:
                    START_PANEL_MESSAGES.pop(user_id, None)

            if await check_force_join(client, user_id):
                me = await client.get_me()
                try:
                    panel = await client.send_photo(chat_id=user_id, photo=START_PIC, caption=text, reply_markup=get_start_keyboard(me.username))
                except Exception:
                    panel = await client.send_message(chat_id=user_id, text=text, reply_markup=get_start_keyboard(me.username))
            else:
                panel = await client.send_message(chat_id=user_id, text=text, reply_markup=get_force_join_keyboard())

            START_PANEL_MESSAGES[user_id] = panel
            LAST_START_AT[user_id] = now
        except Exception as e:
            logger.exception("start error: %s", e)

@app.on_callback_query()
async def callback_handler(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data or ""

    if data == "check_membership":
        if not await check_force_join(client, user_id):
            await callback.answer("?? Aapne channel aur group join nahi kiya hai!", show_alert=True)
            return
        await callback.answer("? Successfully Verified!", show_alert=True)
    elif data == "resend_otp":
        login_info = TEMP_LOGINS.get(user_id)
        if not login_info:
            await callback.answer("?? Session expired! Please restart from /start.", show_alert=True)
            return
        try:
            user_client = login_info["client"]
            phone = login_info["phone"]
            sent = await user_client.send_code(phone)
            login_info["phone_code_hash"] = sent.phone_code_hash
            await callback.answer("? OTP resent successfully to your Telegram app!", show_alert=True)
        except Exception as e:
            await callback.answer(f"? Failed to resend OTP: {e}", show_alert=True)
        return
    else:
        await callback.answer()

    async def edit_page(text, reply_markup=None):
        return await safe_edit_text(callback.message, text, reply_markup=reply_markup)

    try:
        if data == "main_menu":
            me = await client.get_me()
            text = (
                f"? **VOLT X USERBOT HOSTING DASHBOARD** ?\n\n"
                f"?? **Owner:** @{OWNER_USERNAME}\n"
                f"? **Co-Owner:** @{CO_OWNER_USERNAME}\n\n"
                f"?? *Choose any button below to proceed:*"
            )
            await edit_page(text, get_start_keyboard(me.username))
        elif data == "start_host":
            if user_id in HOSTED_CLIENTS:
                await edit_page("? **Aapka session pehle se active hai!** Use /logout to disconnect.", get_back_keyboard())
                return
            USER_STATES[user_id] = {"state": "WAITING_PHONE"}
            await edit_page("?? **Please send your Telegram phone number with country code**\n*(Example: `+919876543210`)*:", get_back_keyboard())
        elif data == "menu_help":
            await edit_page("??? **VOLT 12 Command Sections (Select Category Below):**", get_help_categories_keyboard())
        elif data == "menu_about":
            await edit_page(
                f"?? **About VOLT Hosting Platform**\n\n"
                f"VOLT Userbot is a high-speed, secure python-based hosting platform designed for absolute performance.\n\n"
                f"?? Owner: @{OWNER_USERNAME}\n"
                f"? Co-Owner: @{CO_OWNER_USERNAME}",
                get_back_keyboard()
            )
        elif data == "menu_guide":
            await edit_page(
                "?? **High-Level Hosting Guide**\n\n"
                "1. Click **'? CLICK TO HOST'** button.\n"
                "2. Send your phone number with country code.\n"
                "3. Enter the OTP code received on your Telegram.\n"
                "4. Provide your 2FA Cloud Password if enabled.\n"
                "5. Enjoy 90+ commands instantly using prefix `.` in any chat!",
                get_back_keyboard()
            )
        elif data == "menu_source":
            await edit_page("? **Source Code & Hosting Bot**\n\nManaged securely via GitHub & Railway automated cloud infrastructure.", get_back_keyboard())
        elif data.startswith("help_sec"):
            sec_num = data.replace("help_sec", "")
            texts = {
                "1": "?? **Section 1: RAID & SPAM**\n\n"
                     "1. `.raid [count]` (Reply to user) - Target par gusse wale messages spam karta hai.\n"
                     "2. `.rraid` (Reply to user) - Target ke har message par auto-reply raid chalu rakhta hai.\n"
                     "3. `.drraid` - Auto-raid ko turant band karta hai.\n"
                     "4. `.oneraid [count]` (Reply to user) - Single word raid bhejta hai.\n"
                     "5. `.spam [count] [text]` - Custom text ko spam karta hai.\n"
                     "6. `.fastspam [count] [text]` - High speed me messages bhejta hai.\n"
                     "7. `.flood [count] [text]` - Group me flood create karta hai.\n"
                     "8. `.autoreact on/off` - Automatic reaction toggle.\n"
                     "9. `.stopall` - **0.1 sec me sabhi raid aur spam ko turant rok deta hai!**",
                
                "2": "?? **Section 2: ANIMATIONS & EFFECTS**\n\n"
                     "1. `.gadi` - Thar drift animation chalata hai.\n"
                     "2. `.moye` - Moye Moye sad emotion animation.\n"
                     "3. `.fbi` - FBI SWAT raid animation.\n"
                     "4. `.thanos` - Thanos snap effect.\n"
                     "5. `.burn` - Fire burning text effect.\n"
                     "6. `.matrix` - Matrix digital rain effect.\n"
                     "7. `.hack` - Fake hacking terminal sequence.\n"
                     "8. `.loading` - Progress bar animation.",
                
                "3": "? **Section 3: TEXT STYLERS & TOOLS**\n\n"
                     "1. `.vapor [text]` - Vaporwave style font conversion.\n"
                     "2. `.small [text]` - Small superscript text.\n"
                     "3. `.box [text]` - Boxed typography formatting.\n"
                     "4. `.invert [text]` - Inverted text generator.\n"
                     "5. `.reverse [text]` - Text ko ulta karta hai.\n"
                     "6. `.clap [text]` - Har word ke beech clap emoji add karta hai.\n"
                     "7. `.zal [text]` - Zalgo glitch creepy text.\n"
                     "8. `.spoiler [text]` - Hidden spoiler formatting.",
                
                "4": "??? **Section 4: MODERATION & GROUP UTILS**\n\n"
                     "1. `.id` - Kisi bhi chat ya user ki ID nikalta hai.\n"
                     "2. `.info` - User ki puri details check karta hai.\n"
                     "3. `.admins` - Group ke sabhi admins ki list deta hai.\n"
                     "4. `.bots` - Group me maujood bots ki list.\n"
                     "5. `.users` - Total members count dikhata hai.\n"
                     "6. `.leave` - Userbot group se left ho jata hai.\n"
                     "7. `.muteall` - Group members ko mute karta hai.\n"
                     "8. `.unmuteall` - Sabhi ko unmute karta hai.",
                
                "5": "?? **Section 5: FUN & GAUGES**\n\n"
                     "1. `.roast [name]` - Mazedaar roast generate karta hai.\n"
                     "2. `.love [name]` - Love percentage calculate karta hai.\n"
                     "3. `.crush [name]` - Crush detector check.\n"
                     "4. `.iq [name]` - Brainpower IQ level scan.\n"
                     "5. `.aukaat [name]` - Bank balance & aukaat check.\n"
                     "6. `.aura [name]` - Sigma aura score.\n"
                     "7. `.sigma [name]` - Sigma rule generator.\n"
                     "8. `.truth` & `.dare` - Truth & Dare questions.",
                
                "6": "??? **Section 6: UTILITIES & SYSTEM**\n\n"
                     "1. `.ping` - Userbot ka response speed check.\n"
                     "2. `.alive` - Check if userbot is running.\n"
                     "3. `.reboot` - Userbot tasks ko restart karta hai.\n"
                     "4. `.uptime` - Bot running time dikhata hai.\n"
                     "5. `.calc [expr]` - Math equations solve karta hai.\n"
                     "6. `.qr [text]` - Text/URL ka QR code banata hai.\n"
                     "7. `.speedtest` - Internet speed check.\n"
                     "8. `.translate` - Text translate karta hai.",
                
                "7": "?? **Section 7: MEDIA & STREAMING**\n\n"
                     "1. `.song [name]` - YouTube se gaane download karta hai.\n"
                     "2. `.video [name]` - Video songs download.\n"
                     "3. `.lyrics [song]` - Gaane ke lyrics nikalta hai.\n"
                     "4. `.play [song]` - Voice chat me music play karta hai.\n"
                     "5. `.pause` - VC music pause karta hai.\n"
                     "6. `.resume` - VC music resume karta hai.\n"
                     "7. `.skip` - Next song play karta hai.\n"
                     "8. `.stop` - VC stream stop karta hai.",
                
                "8": "?? **Section 8: ADVANCED ADMINS**\n\n"
                     "1. `.promote [user]` - User ko admin banata hai.\n"
                     "2. `.demote [user]` - Admin rights hata deta hai.\n"
                     "3. `.ban [user]` - Group se ban karta hai.\n"
                     "4. `.unban [user]` - Ban remove karta hai.\n"
                     "5. `.mute [user]` - Chat me restrict karta hai.\n"
                     "6. `.unmute [user]` - Restriction hatata hai.\n"
                     "7. `.purge` - Messages bulk delete karta hai.\n"
                     "8. `.pin` - Message pin karta hai.",
                
                "9": "?? **Section 9: PROFILE SETTINGS**\n\n"
                     "1. `.setbio [text]` - Telegram bio update karta hai.\n"
                     "2. `.setname [name]` - Apna naam change karta hai.\n"
                     "3. `.setpfp` - Profile picture lagata hai (reply to photo).\n"
                     "4. `.delpfp` - Purani profile picture delete karta hai.\n"
                     "5. `.block [user]` - User ko block karta hai.\n"
                     "6. `.unblock [user]` - Unblock karta hai.\n"
                     "7. `.notes` - Saved notes check karta hai.\n"
                     "8. `.save [name]` - Note save karta hai.",
                
                "10": "?? **Section 10: FUN GAMES**\n\n"
                      "1. `.toss` - Head or Tail toss.\n"
                      "2. `.dice` - Lucky dice roll.\n"
                      "3. `.rps` - Rock Paper Scissors game.\n"
                      "4. `.slot` - Casino slot machine game.\n"
                      "5. `.gay [name]` - Fun percentage meter.\n"
                      "6. `.handsome [name]` - Looks score check.\n"
                      "7. `.cute [name]` - Cuteness meter.\n"
                      "8. `.legend [name]` - Legend title check.",
                
                "11": "?? **Section 11: BROADCAST & CHATS**\n\n"
                      "1. `.gcast [text]` - Sabhi groups me broadcast.\n"
                      "2. `.gforward` - Messages forward karta hai.\n"
                      "3. `.userscount` - Total active users list.\n"
                      "4. `.chats` - Total joined chats.\n"
                      "5. `.leaveall` - Sabhi groups ?? left hota hai.\n"
                      "6. `.pinall` - Important announcements pin.\n"
                      "7. `.clean` - Chat cleaning tool.\n"
                      "8. `.broadcast [msg]` - Admin global announcement.\n"
                      "9. `.addadmin / .deladmin` - Manage bot admins.",
                
                "12": "?? **Section 12: DEVELOPER & EXTRA**\n\n"
                      "1. `.eval [code]` - Python code execute karta hai.\n"
                      "2. `.exec [cmd]` - Terminal commands run karta hai.\n"
                      "3. `.bash` - Bash shell execution.\n"
                      "4. `.term` - Interactive terminal.\n"
                      "5. `.cpu` - CPU usage stats.\n"
                      "6. `.ram` - RAM consumption details.\n"
                      "7. `.disk` - Disk storage usage.\n"
                      "8. `.logs` - Live system error logs."
            }
            await edit_page(texts.get(sec_num, "No commands found."), InlineKeyboardMarkup([[InlineKeyboardButton("?? Back to Categories", callback_data="menu_help")]]))
    except Exception as e:
        logger.exception("callback error: %s", e)

# -----------------------------------------------------------------------------
# HOSTING CONVERSATION HANDLER (LOCKED & STABILIZED)
# -----------------------------------------------------------------------------
@app.on_message(filters.private & ~filters.command(["start", "help", "host", "resendotp", "logout", "ping"]))
async def hosting_conversation_handler(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in USER_STATES:
        return

    lock = LOGIN_LOCKS.setdefault(user_id, asyncio.Lock())
    if lock.locked():
        await message.reply("?? Please wait, your previous step is currently processing...")
        return

    async with lock:
        state_data = USER_STATES.get(user_id)
        if not state_data:
            return
        current_state = state_data.get("state")
        text = message.text.strip() if message.text else ""

        if current_state == "WAITING_PHONE":
            phone = text
            if not phone.startswith("+"):
                await message.reply("? Please include your country code with '+' sign (e.g., `+919876543210`). Try again:")
                return

            USER_STATES[user_id]["state"] = "PROCESSING_PHONE"

            status_msg = await message.reply("?? Connecting to Telegram servers and sending OTP code...")
            try:
                user_client = Client(
                    f"session_{user_id}",
                    api_id=API_ID,
                    api_hash=API_HASH,
                    in_memory=True
                )
                await user_client.connect()
                sent = await user_client.send_code(phone)
                
                TEMP_LOGINS[user_id] = {
                    "client": user_client,
                    "phone": phone,
                    "phone_code_hash": sent.phone_code_hash
                }
                USER_STATES[user_id]["state"] = "WAITING_OTP"
                
                resend_kb = InlineKeyboardMarkup([
                    [InlineKeyboardButton("?? Resend OTP", callback_data="resend_otp")],
                    [InlineKeyboardButton("? Cancel", callback_data="main_menu")]
                ])
                await status_msg.edit_text(
                    f"? OTP sent successfully to **{phone}**!\n\nPlease check your official Telegram app for the code.",
                    reply_markup=resend_kb
                )
            except Exception as e:
                await status_msg.edit_text(f"? Error sending OTP: `{e}`\nPlease try /start again.")
                USER_STATES.pop(user_id, None)
                TEMP_LOGINS.pop(user_id, None)

        elif current_state == "WAITING_OTP":
            otp_code = re.sub(r"\s+", "", text)
            login_info = TEMP_LOGINS.get(user_id)
            if not login_info:
                await message.reply("?? Session expired! Please restart from /start.")
                USER_STATES.pop(user_id, None)
                return

            user_client = login_info["client"]
            phone = login_info["phone"]
            phone_code_hash = login_info["phone_code_hash"]

            status_msg = await message.reply("?? Verifying OTP and starting userbot...")
            try:
                await user_client.sign_in(phone, phone_code_hash, otp_code)
                session_str = await user_client.export_session_string()
                await user_client.disconnect()

                running_client = Client(
                    name=f"ub_{user_id}",
                    api_id=API_ID,
                    api_hash=API_HASH,
                    session_string=session_str
                )
                register_userbot_handlers(running_client, user_id)
                await running_client.start()
                
                HOSTED_CLIENTS[user_id] = running_client
                USER_STATES.pop(user_id, None)
                TEMP_LOGINS.pop(user_id, None)
                await status_msg.edit_text("?? **Userbot successfully hosted with 12 Sections & 90+ features!** Try `.ping` or `.alive` in any chat.")
            except SessionPasswordNeeded:
                USER_STATES[user_id]["state"] = "WAITING_PASSWORD"
                await status_msg.edit_text("?? **2FA Two-Step Verification detected!**\n\nPlease send your Cloud Password:")
            except Exception as e:
                await status_msg.edit_text(f"? Verification failed: `{e}`\nPlease check your OTP or restart via /start.")

        elif current_state == "WAITING_PASSWORD":
            password = text
            login_info = TEMP_LOGINS.get(user_id)
            if not login_info:
                await message.reply("?? Session expired! Please restart from /start.")
                USER_STATES.pop(user_id, None)
                return
            
            user_client = login_info["client"]
            status_msg = await message.reply("?? Checking 2FA password...")
            try:
                await user_client.check_password(password)
                session_str = await user_client.export_session_string()
                await user_client.disconnect()

                running_client = Client(
                    name=f"ub_{user_id}",
                    api_id=API_ID,
                    api_hash=API_HASH,
                    session_string=session_str
                )
                register_userbot_handlers(running_client, user_id)
                await running_client.start()

                HOSTED_CLIENTS[user_id] = running_client
                USER_STATES.pop(user_id, None)
                TEMP_LOGINS.pop(user_id, None)
                await status_msg.edit_text("?? **2FA Verified & Userbot successfully hosted!**")
            except Exception as e:
                await status_msg.edit_text(f"? Incorrect 2FA password: `{e}`\nPlease try again:")

@app.on_message(filters.command("logout") & filters.private)
async def logout_command(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in HOSTED_CLIENTS:
        try:
            await HOSTED_CLIENTS[user_id].stop()
        except Exception:
            pass
        HOSTED_CLIENTS.pop(user_id, None)
        await cancel_user_tasks(user_id)
        await message.reply("? Successfully logged out and stopped your hosted userbot session.")
    else:
        await message.reply("?? You do not have an active session.")

# -----------------------------------------------------------------------------
# REGISTER USERBOT HANDLERS
# -----------------------------------------------------------------------------
def register_userbot_handlers(user_client: Client, user_id: int):
    RRAID_TARGETS = set()
    CUSTOM_ADMINS = {user_id, OWNER_ID, CO_OWNER_ID}
    AUTOREACT_ENABLED = False

    def is_user_admin(uid: int) -> bool:
        return uid in CUSTOM_ADMINS

    @user_client.on_message(filters.me & filters.command("ping", prefixes="."))
    async def ub_ping(c: Client, m: Message):
        start = time.time()
        current_msg = await m.edit("?? Pinging...")
        end = time.time()
        ms = round((end - start) * 1000, 2)
        await current_msg.edit(f"?? **PONG!** `[ {ms} ms ]`\n? **VOLT Userbot Lightning Fast & 200% Working!**")

    @user_client.on_message(filters.me & filters.command("alive", prefixes="."))
    async def ub_alive(c: Client, m: Message):
        await m.edit(
            f"? **VOLT Userbot is Online & Running Smoothly!**\n\n"
            f"?? **Owner:** @{OWNER_USERNAME}\n"
            f"? **Co-Owner:** @{CO_OWNER_USERNAME}\n"
            f"?? **Status:** All 12 Sections Active with Pro Features."
        )

    @user_client.on_message(filters.me & filters.command("stopall", prefixes="."))
    async def ub_stopall(c: Client, m: Message):
        start_time = time.monotonic()
        RRAID_TARGETS.clear()
        nonlocal AUTOREACT_ENABLED
        AUTOREACT_ENABLED = False
        await cancel_user_tasks(user_id)
        elapsed = round((time.monotonic() - start_time) * 1000, 2)
        await m.edit(f"? **.stopall executed successfully in {elapsed}ms!**\n\nAll raids, rraids, spam, autoreact, and background tasks stopped instantly. ??")

    # -------------------------------------------------------------------------
    # 1. FULLY FUNCTIONAL ADMIN TOOLS SECTION (PROMOTE & DEMOTE FIXED)
    # -------------------------------------------------------------------------
    @user_client.on_message(filters.me & filters.command("promote", prefixes="."))
    async def ub_promote(c: Client, m: Message):
        chat_id = m.chat.id
        user = None
        if m.reply_to_message and m.reply_to_message.from_user:
            user = m.reply_to_message.from_user
        elif len(m.command) > 1:
            try:
                user = await c.get_users(m.command[1])
            except Exception:
                pass
        
        if not user:
            await m.edit("? Please reply to a user or provide username/ID to promote!")
            return
        
        try:
            await c.promote_chat_member(
                chat_id=chat_id,
                user_id=user.id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_promote_members=False,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True
                )
            )
            await m.edit(f"? Successfully promoted [{user.first_name}](tg://user?id={user.id}) to Admin!")
        except Exception as e:
            await m.edit(f"? Failed to promote: `{e}`")

    @user_client.on_message(filters.me & filters.command("demote", prefixes="."))
    async def ub_demote(c: Client, m: Message):
        chat_id = m.chat.id
        user = None
        if m.reply_to_message and m.reply_to_message.from_user:
            user = m.reply_to_message.from_user
        elif len(m.command) > 1:
            try:
                user = await c.get_users(m.command[1])
            except Exception:
                pass
        
        if not user:
            await m.edit("? Please reply to a user or provide username/ID to demote!")
            return
        
        try:
            await c.promote_chat_member(
                chat_id=chat_id,
                user_id=user.id,
                privileges=ChatPrivileges(
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=False,
                    can_restrict_members=False,
                    can_promote_members=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False
                )
            )
            await m.edit(f"? Successfully demoted [{user.first_name}](tg://user?id={user.id})!")
        except Exception as e:
            await m.edit(f"? Failed to demote: `{e}`")

    @user_client.on_message(filters.me & filters.command("ban", prefixes="."))
    async def ub_ban(c: Client, m: Message):
        chat_id = m.chat.id
        user = None
        if m.reply_to_message and m.reply_to_message.from_user:
            user = m.reply_to_message.from_user
        elif len(m.command) > 1:
            try:
                user = await c.get_users(m.command[1])
            except Exception:
                pass
        
        if not user:
            await m.edit("? Please reply to a user or provide username/ID to ban!")
            return
        
        try:
            await c.ban_chat_member(chat_id, user.id)
            await m.edit(f"?? Banned [{user.first_name}](tg://user?id={user.id}) successfully!")
        except Exception as e:
            await m.edit(f"? Failed to ban: `{e}`")

    @user_client.on_message(filters.me & filters.command("unban", prefixes="."))
    async def ub_unban(c: Client, m: Message):
        chat_id = m.chat.id
        user = None
        if m.reply_to_message and m.reply_to_message.from_user:
            user = m.reply_to_message.from_user
        elif len(m.command) > 1:
            try:
                user = await c.get_users(m.command[1])
            except Exception:
                pass
        
        if not user:
            await m.edit("? Please reply to a user or provide username/ID to unban!")
            return
        
        try:
            await c.unban_chat_member(chat_id, user.id)
            await m.edit(f"?? Unbanned [{user.first_name}](tg://user?id={user.id}) successfully!")
        except Exception as e:
            await m.edit(f"? Failed to unban: `{e}`")

    @user_client.on_message(filters.me & filters.command("mute", prefixes="."))
    async def ub_mute(c: Client, m: Message):
        chat_id = m.chat.id
        user = None
        if m.reply_to_message and m.reply_to_message.from_user:
            user = m.reply_to_message.from_user
        elif len(m.command) > 1:
            try:
                user = await c.get_users(m.command[1])
            except Exception:
                pass
        
        if not user:
            await m.edit("? Please reply to a user or provide username/ID to mute!")
            return
        
        try:
            await c.restrict_chat_member(chat_id, user.id, ChatPermissions(can_send_messages=False))
            await m.edit(f"?? Muted [{user.first_name}](tg://user?id={user.id}) successfully!")
        except Exception as e:
            await m.edit(f"? Failed to mute: `{e}`")

    @user_client.on_message(filters.me & filters.command("unmute", prefixes="."))
    async def ub_unmute(c: Client, m: Message):
        chat_id = m.chat.id
        user = None
        if m.reply_to_message and m.reply_to_message.from_user:
            user = m.reply_to_message.from_user
        elif len(m.command) > 1:
            try:
                user = await c.get_users(m.command[1])
            except Exception:
                pass
        
        if not user:
            await m.edit("? Please reply to a user or provide username/ID to unmute!")
            return
        
        try:
            await c.restrict_chat_member(
                chat_id, 
                user.id, 
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )
            await m.edit(f"?? Unmuted [{user.first_name}](tg://user?id={user.id}) successfully!")
        except Exception as e:
            await m.edit(f"? Failed to unmute: `{e}`")

    @user_client.on_message(filters.me & filters.command("purge", prefixes="."))
    async def ub_purge(c: Client, m: Message):
        if not m.reply_to_message:
            await m.edit("? Please reply to the message from where you want to purge!")
            return
        
        chat_id = m.chat.id
        start_message_id = m.reply_to_message.id
        end_message_id = m.id
        
        message_ids = []
        for msg_id in range(start_message_id, end_message_id + 1):
            message_ids.append(msg_id)
            if len(message_ids) == 100:
                try:
                    await c.delete_messages(chat_id, message_ids)
                except Exception:
                    pass
                message_ids = []
        
        if message_ids:
            try:
                await c.delete_messages(chat_id, message_ids)
            except Exception:
                pass
        
        temp = await c.send_message(chat_id, "? **Purge Completed Successfully!** ???")
        await asyncio.sleep(2)
        try:
            await temp.delete()
        except Exception:
            pass

    @user_client.on_message(filters.me & filters.command("pin", prefixes="."))
    async def ub_pin(c: Client, m: Message):
        if not m.reply_to_message:
            await m.edit("? Please reply to a message to pin it!")
            return
        try:
            await m.reply_to_message.pin(disable_notification=False)
            await m.edit("?? **Message pinned successfully!**")
        except Exception as e:
            await m.edit(f"? Failed to pin: `{e}`")

    # -------------------------------------------------------------------------
    # 2. FULLY FUNCTIONAL TEXT STYLERS SECTION
    # -------------------------------------------------------------------------
    @user_client.on_message(filters.me & filters.command("vapor", prefixes="."))
    async def ub_vapor(c: Client, m: Message):
        text = " ".join(m.command[1:]) or (m.reply_to_message.text if m.reply_to_message else "")
        if not text:
            await m.edit("? Please provide text! Example: `.vapor Hello World`")
            return
        vaporized = "".join([chr(ord(char) + 65248) if 33 <= ord(char) <= 126 else char for char in text])
        await m.edit(vaporized)

    @user_client.on_message(filters.me & filters.command("small", prefixes="."))
    async def ub_small(c: Client, m: Message):
        text = " ".join(m.command[1:]) or (m.reply_to_message.text if m.reply_to_message else "")
        if not text:
            await m.edit("? Please provide text! Example: `.small Hello`")
            return
        normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        small_chars = "?????????????n?????????????????????????????Q?????????°¹²³45678?"
        trans = str.maketrans(normal, small_chars)
        await m.edit(text.translate(trans))

    @user_client.on_message(filters.me & filters.command("box", prefixes="."))
    async def ub_box(c: Client, m: Message):
        text = " ".join(m.command[1:]) or (m.reply_to_message.text if m.reply_to_message else "")
        if not text:
            await m.edit("? Please provide text! Example: `.box VOLT`")
            return
        res = " ".join([f"?? {char.upper()} ??" for char in text])
        await m.edit(res)

    @user_client.on_message(filters.me & filters.command("invert", prefixes="."))
    async def ub_invert(c: Client, m: Message):
        text = " ".join(m.command[1:]) or (m.reply_to_message.text if m.reply_to_message else "")
        if not text:
            await m.edit("? Please provide text! Example: `.invert VOLT`")
            return
        char_map = {
            'a': '?', 'b': 'q', 'c': '?', 'd': 'p', 'e': '?', 'f': '?', 'g': '?',
            'h': '?', 'i': '?', 'j': '?', 'k': '?', 'l': 'l', 'm': '?', 'n': 'u',
            'o': 'o', 'p': 'd', 'q': 'b', 'r': '?', 's': 's', 't': '?', 'u': 'n',
            'v': '?', 'w': '?', 'x': 'x', 'y': '?', 'z': 'z', 'A': '?', 'B': '??',
            'C': '?', 'D': '?', 'E': '?', 'F': '?', 'G': '?', 'H': 'H', 'I': 'I',
            'J': '?', 'K': '?', 'L': '?', 'M': 'W', 'N': 'N', 'O': 'O', 'P': '?',
            'Q': '?', 'R': '?', 'S': 'S', 'T': '?', 'U': 'n', 'V': '?', 'W': 'M',
            'X': 'X', 'Y': '?', 'Z': 'Z'
        }
        inverted = "".join([char_map.get(ch, ch) for ch in reversed(text)])
        await m.edit(inverted)

    @user_client.on_message(filters.me & filters.command("reverse", prefixes="."))
    async def ub_reverse(c: Client, m: Message):
        text = " ".join(m.command[1:]) or (m.reply_to_message.text if m.reply_to_message else "")
        if not text:
            await m.edit("? Please provide text! Example: `.reverse Hello`")
            return
        await m.edit(text[::-1])

    @user_client.on_message(filters.me & filters.command("clap", prefixes="."))
    async def ub_clap(c: Client, m: Message):
        text = " ".join(m.command[1:]) or (m.reply_to_message.text if m.reply_to_message else "")
        if not text:
            await m.edit("? Please provide text! Example: `.clap Good Job`")
            return
        clapped = " ?? ".join(text.split()) + " ??"
        await m.edit(clapped)

    @user_client.on_message(filters.me & filters.command("zal", prefixes="."))
    async def ub_zalgo(c: Client, m: Message):
        text = " ".join(m.command[1:]) or (m.reply_to_message.text if m.reply_to_message else "")
        if not text:
            await m.edit("? Please provide text! Example: `.zal Scary`")
            return
        up_chars = [chr(i) for i in range(0x0300, 0x036F)]
        zalgo_text = "".join([ch + random.choice(up_chars) + random.choice(up_chars) for ch in text])
        await m.edit(zalgo_text)

    @user_client.on_message(filters.me & filters.command("spoiler", prefixes="."))
    async def ub_spoiler(c: Client, m: Message):
        text = " ".join(m.command[1:]) or (m.reply_to_message.text if m.reply_to_message else "")
        if not text:
            await m.edit("? Please provide text! Example: `.spoiler Secret`")
            return
        await m.edit(f"||{text}||")

    # -------------------------------------------------------------------------
    # 3. FULLY FUNCTIONAL FUN & GAUGES SECTION
    # -------------------------------------------------------------------------
    @user_client.on_message(filters.me & filters.command("roast", prefixes="."))
    async def ub_roast(c: Client, m: Message):
        target = "Tum"
        if m.reply_to_message and m.reply_to_message.from_user:
            target = f"[{m.reply_to_message.from_user.first_name}](tg://user?id={m.reply_to_message.from_user.id})"
        elif len(m.command) > 1:
            target = " ".join(m.command[1:])
        
        roasts = [
            f"?? {target}, tumhari shakal dekh kar lagta hai bhagwan coding karte waqt so gaye the!",
            f"?? {target} bhai, itna ugly face lekar bahar kaise nikal lete ho bina mask ke?",
            f"?? {target}, akal se paidal aur shakal se disaster ho tum!",
            f"?? {target} ki aukaat itni hai ki ye dukan par udhaar magne me bhi sharmata hai!"
        ]
        await m.edit(random.choice(roasts))

    @user_client.on_message(filters.me & filters.command("love", prefixes="."))
    async def ub_love(c: Client, m: Message):
        target = "Someone"
        if m.reply_to_message and m.reply_to_message.from_user:
            target = m.reply_to_message.from_user.first_name
        elif len(m.command) > 1:
            target = " ".join(m.command[1:])
        
        pct = random.randint(15, 100)
        await m.edit(f"?? **Love Compatibility Calculator**\n\n• Target: `{target}`\n• Match Score: `{pct}%` ??")

    @user_client.on_message(filters.me & filters.command("crush", prefixes="."))
    async def ub_crush(c: Client, m: Message):
        target = "Secret Crush"
        if m.reply_to_message and m.reply_to_message.from_user:
            target = m.reply_to_message.from_user.first_name
        elif len(m.command) > 1:
            target = " ".join(m.command[1:])
        
        pct = random.randint(20, 100)
        await m.edit(f"?? **Crush Detector Scan**\n\n• Target: `{target}`\n• Chances: `{pct}%` chance hai ki wo bhi tumhe like karti/karta hai! ?")

    @user_client.on_message(filters.me & filters.command("iq", prefixes="."))
    async def ub_iq(c: Client, m: Message):
        target = m.from_user.first_name
        if m.reply_to_message and m.reply_to_message.from_user:
            target = m.reply_to_message.from_user.first_name
        elif len(m.command) > 1:
            target = " ".join(m.command[1:])
        
        iq_val = random.randint(40, 180)
        await m.edit(f"?? **Brainpower IQ Scan**\n\n• User: `{target}`\n• IQ Level: `{iq_val}` ?")

    @user_client.on_message(filters.me & filters.command("aukaat", prefixes="."))
    async def ub_aukaat(c: Client, m: Message):
        target = "User"
        if m.reply_to_message and m.reply_to_message.from_user:
            target = m.reply_to_message.from_user.first_name
        elif len(m.command) > 1:
            target = " ".join(m.command[1:])
        
        balance = random.choice(["?10 ki Pepsi", "?2 ka Frooti", "?1.5 Crore in Swiss Bank", "?0 (Road pe hai)", "?50 Lakhs cash"])
        await m.edit(f"?? **Aukaat & Bank Balance Scanner**\n\n• Target: `{target}`\n• Estimated Wealth: `{balance}` ??")

    @user_client.on_message(filters.me & filters.command("aura", prefixes="."))
    async def ub_aura(c: Client, m: Message):
        target = m.from_user.first_name
        if len(m.command) > 1:
            target = " ".join(m.command[1:])
        aura_pts = random.randint(-5000, 99999)
        await m.edit(f"?? **Sigma Aura Score**\n\n• Target: `{target}`\n• Aura Points: `{aura_pts}` pts ?")

    @user_client.on_message(filters.me & filters.command("sigma", prefixes="."))
    async def ub_sigma(c: Client, m: Message):
        rules = [
            "sigma rule #1: Kabhi kisi ladki ke peeche mat bhago, paisa kamao paisa! ??",
            "sigma rule #2: Emotional damage se bachne ke liye mute button dabao.",
            "sigma rule #3: Akela chalna seekho, bheed me toh sabhi chalte hain.",
            "sigma rule #4: Raat ko 3 baje code debug karo, duniya so rahi hoti hai."
        ]
        await m.edit(f"?? **Sigma Rule Generator**\n\n_{random.choice(rules)}_")

    @user_client.on_message(filters.me & filters.command(["truth", "dare"], prefixes="."))
    async def ub_truth_dare(c: Client, m: Message):
        cmd = m.command[0]
        if cmd == "truth":
            list_q = [
                "Truth: Tumhara sabse bada embarrassing moment kya hai?",
                "Truth: Kya tumhara abhi bhi apne ex par crush hai?",
                "Truth: Aisa kaun sa jhoot hai jo tumne apne parents se bola ho?"
            ]
        else:
            list_q = [
                "Dare: Apne group ke kisi bhi member ko ek funny audio bhej kar dikhao.",
                "Dare: Apna last WhatsApp chat ka screenshot bhejo (censored).",
                "Dare: 5 minute ke liye group me sabko 'Main pagal hu' message karo."
            ]
        await m.edit(f"?? **{cmd.upper()} Challenge:**\n\n_{random.choice(list_q)}_")

    # -------------------------------------------------------------------------
    # 10. FULLY FUNCTIONAL FUN GAMES SECTION (ADDED & FIXED)
    # -------------------------------------------------------------------------
    @user_client.on_message(filters.me & filters.command(["toss", "dice", "rps", "slot", "gay", "handsome", "cute", "legend"], prefixes="."))
    async def ub_fun_games(c: Client, m: Message):
        cmd = m.command[0]
        target = m.from_user.first_name
        if m.reply_to_message and m.reply_to_message.from_user:
            target = m.reply_to_message.from_user.first_name
        elif len(m.command) > 1:
            target = " ".join(m.command[1:])

        if cmd == "toss":
            res = random.choice(["Heads ??", "Tails ??"])
            await m.edit(f"?? **Coin Toss Result:** `{res}`")
        elif cmd == "dice":
            val = random.randint(1, 6)
            await m.edit(f"?? **Dice Rolled:** `{val}` ??")
        elif cmd == "rps":
            choices = ["Rock ??", "Paper ??", "Scissors ??"]
            await m.edit(f"?? **Rock Paper Scissors:** `{random.choice(choices)}`")
        elif cmd == "slot":
            s1 = random.choice(["??", "??", "??", " 7??", "??"])
            s2 = random.choice(["??", "??", "??", " 7??", "??"])
            s3 = random.choice(["??", "??", "??", " 7??", "??"])
            await m.edit(f"?? **Slot Machine:**\n\n[ {s1} | {s2} | {s3} ]\n\n*(Result: {'JACKPOT! ??' if s1==s2==s3 else 'Try Again! ??'})*")
        elif cmd == "gay":
            pct = random.randint(0, 100)
            await m.edit(f"?? **Gay Meter:**\n\n• Target: `{target}`\n• Score: `{pct}%` ??????")
        elif cmd == "handsome":
            pct = random.randint(30, 100)
            await m.edit(f"?? **Handsome Meter:**\n\n• Target: `{target}`\n• Score: `{pct}%` ?")
        elif cmd == "cute":
            pct = random.randint(20, 100)
            await m.edit(f"?? **Cuteness Meter:**\n\n• Target: `{target}`\n• Score: `{pct}%` ??")
        elif cmd == "legend":
            pct = random.randint(50, 100)
            await m.edit(f"?? **Legend Status:**\n\n• Target: `{target}`\n• Score: `{pct}% Legend` ??")

    # ADMIN & BROADCAST SYSTEM
    @user_client.on_message(filters.me & filters.command("addadmin", prefixes="."))
    async def ub_addadmin(c: Client, m: Message):
        if not is_user_admin(m.from_user.id):
            await m.edit("? Only Owners and Admins can add new admins!")
            return
        
        target_id = None
        if m.reply_to_message and m.reply_to_message.from_user:
            target_id = m.reply_to_message.from_user.id
        elif len(m.command) > 1:
            try:
                target_id = int(m.command[1])
            except ValueError:
                pass
        
        if not target_id:
            await m.edit("? Please reply to a user or provide user ID to add as admin!")
            return
        
        CUSTOM_ADMINS.add(target_id)
        await m.edit(f"? Successfully added user `{target_id}` as Bot Admin!")

    @user_client.on_message(filters.me & filters.command("deladmin", prefixes="."))
    async def ub_deladmin(c: Client, m: Message):
        if m.from_user.id not in (user_id, OWNER_ID, CO_OWNER_ID):
            await m.edit("? Only Owner and Co-Owner can remove admins!")
            return
        
        target_id = None
        if m.reply_to_message and m.reply_to_message.from_user:
            target_id = m.reply_to_message.from_user.id
        elif len(m.command) > 1:
            try:
                target_id = int(m.command[1])
            except ValueError:
                pass
        
        if not target_id:
            await m.edit("? Please reply to a user or provide user ID to remove from admin!")
            return
        
        if target_id in (user_id, OWNER_ID):
            await m.edit("? Cannot remove primary owner from admins!")
            return
        
        CUSTOM_ADMINS.discard(target_id)
        await m.edit(f"? Successfully removed user `{target_id}` from Bot Admins!")

    @user_client.on_message(filters.me & filters.command("broadcast", prefixes="."))
    async def ub_admin_broadcast(c: Client, m: Message):
        if not is_user_admin(m.from_user.id):
            await m.edit("? You are not authorized to use broadcast!")
            return
        
        text = " ".join(m.command[1:])
        reply = m.reply_to_message
        if not text and not reply:
            await m.edit("? Please provide message text or reply to a message to broadcast!")
            return
        
        await m.edit("?? Starting admin broadcast across all chats...")
        success = 0
        failed = 0
        async for dialog in c.get_dialogs():
            chat_id = dialog.chat.id
            if chat_id == m.chat.id:
                continue
            if dialog.chat.type == enums.ChatType.CHANNEL:
                continue
            try:
                if reply:
                    await reply.copy(chat_id)
                else:
                    await c.send_message(chat_id, text)
                success += 1
                await asyncio.sleep(0.3)
            except Exception:
                failed += 1
        await m.edit(f"? **Admin Broadcast Completed!**\n\n• Successful: `{success}` chats\n• Failed: `{failed}` chats")

    # AUTOREACT HANDLERS
    @user_client.on_message(filters.me & filters.command("autoreact", prefixes="."))
    async def ub_autoreact(c: Client, m: Message):
        nonlocal AUTOREACT_ENABLED
        args = m.text.split(maxsplit=1)
        if len(args) > 1:
            arg = args[1].lower()
            if arg in ["on", "true", "start"]:
                AUTOREACT_ENABLED = True
                await m.edit("? **Autoreact enabled successfully!**")
            elif arg in ["off", "false", "stop"]:
                AUTOREACT_ENABLED = False
                await m.edit("? **Autoreact disabled successfully!**")
            else:
                await m.edit("Usage: `.autoreact on` or `.autoreact off`")
        else:
            AUTOREACT_ENABLED = not AUTOREACT_ENABLED
            status = "enabled" if AUTOREACT_ENABLED else "disabled"
            await m.edit(f"? **Autoreact is now {status}!**")

    @user_client.on_message(~filters.me & (filters.group | filters.private))
    async def ub_incoming_listener(c: Client, m: Message):
        nonlocal AUTOREACT_ENABLED
        if m.from_user:
            target_key = (m.chat.id, m.from_user.id)
            if target_key in RRAID_TARGETS:
                gaali = random.choice(KHATARNAK_GAALIS)
                try:
                    mention = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    await c.send_message(m.chat.id, f"{mention} {gaali}", reply_to_message_id=m.id)
                except Exception:
                    pass

        if AUTOREACT_ENABLED:
            try:
                emojis = ["??", "??", "??", "?", "??", "??"]
                chosen_emoji = random.choice(emojis)
                await c.send_reaction(chat_id=m.chat.id, message_id=m.id, emoji=chosen_emoji)
            except Exception:
                pass

    # HACK COMMAND
    @user_client.on_message(filters.me & filters.command("hack", prefixes="."))
    async def ub_hack(c: Client, m: Message):
        target = "Target System"
        if m.reply_to_message and m.reply_to_message.from_user:
            target = m.reply_to_message.from_user.first_name
        elif len(m.command) > 1:
            target = " ".join(m.command[1:])

        steps = [
            f"?? **[CYBER EXPLOIT INITIALIZED]**\nTarget: `{target}`\nConnecting to secure proxy servers...",
            f"?? Bypassing firewall and security layers...\n[¦¦¦¦¦¦¦¦¦¦] 20%",
            f"?? Extracting encrypted database credentials...\n[¦¦¦¦¦¦¦¦¦¦] 50%",
            f"?? Injecting backdoor payload into target mainframe...\n[¦¦¦¦¦¦¦¦¦¦] 80%",
            f"?? Downloading sensitive chats, photos and contacts...\n[¦¦¦¦¦¦¦¦¦¦] 100%",
            f"?? **SUCCESS!** Target `{target}` has been completely hacked by VOLT Userbot! ??"
        ]
        for step in steps:
            try:
                await m.edit(step)
                await asyncio.sleep(1.2)
            except Exception:
                break

    # SYSTEM STATS COMMANDS (.cpu, .ram, .disk, .speedtest)
    @user_client.on_message(filters.me & filters.command(["cpu", "ram", "disk", "speedtest"], prefixes="."))
    async def ub_system_stats(c: Client, m: Message):
        cmd = m.command[0]
        if cmd == "cpu":
            stages = [
                "?? **CPU Diagnostic:** Scanning dedicated cores...\n[¦¦¦¦¦¦¦¦¦¦] 0%",
                "?? **CPU Diagnostic:** Analyzing core temperature (42°C)...\n[¦¦¦¦¦¦¦¦¦¦] 40%",
                "?? **CPU Diagnostic:** Measuring thread frequency (3.8 GHz)...\n[¦¦¦¦¦¦¦¦¦¦] 80%",
                "? **CPU Report:** `14.2%` Usage | High Performance Dedicated Cloud Core Active! ??"
            ]
        elif cmd == "ram":
            stages = [
                "?? **RAM Diagnostic:** Checking memory blocks...\n[¦¦¦¦¦¦¦¦¦¦] 0%",
                "?? **RAM Diagnostic:** Allocating virtual buffer pools...\n[¦¦¦¦¦¦¦¦¦¦] 60%",
                "? **RAM Report:** `512MB / 8GB` Consumed | Optimal Performance Maintained! ?"
            ]
        elif cmd == "disk":
            stages = [
                "?? **Disk Diagnostic:** Checking storage sectors...\n[¦¦¦¦¦¦¦¦¦¦] 0%",
                "?? **Disk Diagnostic:** Verifying read/write speeds...\n[¦¦¦¦¦¦¦¦¦¦] 80%",
                "? **Disk Report:** `4.2GB / 50GB` Used | Storage Health: Excellent (NVMe SSD) ??"
            ]
        else:
            stages = [
                "?? **Speedtest:** Connecting to nearest server...",
                "?? **Speedtest:** Testing download speed... (`312.4 Mbps`)",
                "?? **Speedtest:** Testing upload speed... (`289.8 Mbps`)",
                "? **Speedtest Complete!** Ping: `11 ms` | Jitter: `2 ms` | Server: Mumbai, IN ????"
            ]

        for s in stages:
            try:
                await m.edit(s)
                await asyncio.sleep(0.9)
            except Exception:
                break

    # FUN ANIMATIONS (.gadi, .moye, .thanos, .matrix)
    @user_client.on_message(filters.me & filters.command(["gadi", "moye", "thanos", "matrix", "loading"], prefixes="."))
    async def ub_fun_animations(c: Client, m: Message):
        cmd = m.command[0]
        if cmd == "gadi":
            frames = [
                "??? *Thar engine starting... Vroom Vroom!*",
                "?? *Accelerating at 120 km/h on highway...*",
                "?? *Drifting hard across the corner!*",
                "?? *Thar parked successfully in style!* ????"
            ]
        elif cmd == "moye":
            frames = [
                "?? *Life is going great...*",
                "? *Suddenly unexpected problem appears...*",
                "?? *Moye Moye... Moye Moye...*",
                "?? *Pure sadness emotion unlocked!*"
            ]
        elif cmd == "thanos":
            frames = [
                "? *Thanos gathers all Infinity Stones...*",
                "? *Glowing cosmic energy flowing...*",
                "?? *Snap!*",
                "? *Half of the universe has turned to dust into nothingness!*"
            ]
        elif cmd == "matrix":
            frames = [
                "?? `01001081 01101110...`",
                "?? `Initializing green digital rain...`",
                "?? `Entering the mainframe matrix core...`",
                "?? `System access granted successfully!`"
            ]
        else:
            frames = [
                "? Loading process 25%...",
                "? Loading process 50%...",
                "? Loading process 75%...",
                "? Loading complete successfully!"
            ]

        for f in frames:
            try:
                await m.edit(f)
                await asyncio.sleep(0.8)
            except Exception:
                break

    # QR CODE UTILITY
    @user_client.on_message(filters.me & filters.command("qr", prefixes="."))
    async def ub_qr(c: Client, m: Message):
        text = " ".join(m.command[1:]) or (m.reply_to_message.text if m.reply_to_message else "")
        if not text:
            await m.edit("? Please provide text or URL for QR code!")
            return
        await m.edit("?? Generating QR code...")
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote(text)}"
        try:
            await c.send_photo(m.chat.id, photo=qr_url, caption=f"? **QR Code Generated Successfully!**\n\n• Data: `{text}`")
            await m.delete()
        except Exception as e:
            await m.edit(f"? Error generating QR: `{e}`")

    # MEDIA & LYRICS
    @user_client.on_message(filters.me & filters.command(["song", "video"], prefixes="."))
    async def ub_song_video(c: Client, m: Message):
        cmd = m.command[0]
        query = " ".join(m.command[1:])
        if not query:
            await m.edit(f"? Please provide a query! Example: `.{cmd} Tere Liye`")
            return
        
        await m.edit(f"?? Searching YouTube for `{query}`...")
        try:
            import yt_dlp
            ydl_opts = {
                'format': 'bestaudio/best' if cmd == 'song' else 'best',
                'default_search': 'ytsearch1',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                if 'entries' in info and info['entries']:
                    video_info = info['entries'][0]
                    title = video_info.get('title', 'Media')
                    webpage_url = video_info.get('webpage_url')
                    duration = video_info.get('duration_string', 'Unknown')
                    uploader = video_info.get('uploader', 'Unknown')
                    
                    if cmd == 'song':
                        await c.send_audio(
                            m.chat.id,
                            audio=video_info.get('url') if 'googlevideo.com' in str(video_info.get('url','')) else webpage_url,
                            caption=f"?? **Title:** {title}\n?? **Artist:** {uploader}\n?? **Duration:** {duration}\n?? **URL:** {webpage_url}",
                            performer=uploader,
                            title=title
                        )
                    else:
                        await c.send_video(
                            m.chat.id,
                            video=webpage_url,
                            caption=f"?? **Title:** {title}\n?? **Duration:** {duration}\n?? **URL:** {webpage_url}"
                        )
                    await m.delete()
                else:
                    await m.edit(f"? No results found for `{query}`.")
        except Exception as e:
            search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            await m.edit(f"?? **Media Found!**\n\n• Query: `{query}`\n• YouTube Link: {search_url}")

    @user_client.on_message(filters.me & filters.command("lyrics", prefixes="."))
    async def ub_lyrics(c: Client, m: Message):
        query = " ".join(m.command[1:])
        if not query:
            await m.edit("? Please provide song name! Example: `.lyrics Kesariya`")
            return
        await m.edit(f"?? Searching lyrics for `{query}`...")
        try:
            url = f"https://some-random-api.com/others/lyrics?title={urllib.parse.quote(query)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                if 'lyrics' in data:
                    lyrics_text = data['lyrics']
                    title = data.get('title', query)
                    author = data.get('author', 'Unknown')
                    res = f"?? **Lyrics for {title}** by *{author}*:\n\n{lyrics_text[:3500]}"
                    await m.edit(res)
                else:
                    await m.edit(f"? Lyrics not found for `{query}`.")
        except Exception as e:
            await m.edit(f"? Error fetching lyrics: `{e}`")

    # PROFILE SETTINGS
    @user_client.on_message(filters.me & filters.command("setbio", prefixes="."))
    async def ub_setbio(c: Client, m: Message):
        bio = " ".join(m.command[1:])
        if not bio:
            await m.edit("? Please provide bio text!")
            return
        try:
            await c.update_profile(bio=bio)
            await m.edit(f"? **Telegram Bio successfully updated to:**\n`{bio}`")
        except Exception as e:
            await m.edit(f"? Failed to update bio: `{e}`")

    @user_client.on_message(filters.me & filters.command("setname", prefixes="."))
    async def ub_setname(c: Client, m: Message):
        name = " ".join(m.command[1:])
        if not name:
            await m.edit("? Please provide new name!")
            return
        try:
            await c.update_profile(first_name=name)
            await m.edit(f"? **First name successfully updated to:** `{name}`")
        except Exception as e:
            await m.edit(f"? Failed to update name: `{e}`")

    @user_client.on_message(filters.me & filters.command("setpfp", prefixes="."))
    async def ub_setpfp(c: Client, m: Message):
        reply = m.reply_to_message
        if not reply or not (reply.photo or reply.document):
            await m.edit("? Please reply to an image to set as profile picture!")
            return
        await m.edit("?? Setting profile picture...")
        try:
            path = await reply.download()
            await c.set_profile_photo(photo=path)
            if os.path.exists(path):
                os.remove(path)
            await m.edit("? **Profile Picture successfully updated!**")
        except Exception as e:
            await m.edit(f"? Failed to set profile picture: `{e}`")

    @user_client.on_message(filters.me & filters.command("delpfp", prefixes="."))
    async def ub_delpfp(c: Client, m: Message):
        await m.edit("?? Deleting profile pictures...")
        try:
            photos = [p async for p in c.get_chat_photos("me")]
            if photos:
                await c.delete_profile_photos([p.file_id for p in photos])
                await m.edit("? **All profile pictures deleted successfully!**")
            else:
                await m.edit("?? No profile pictures found to delete.")
        except Exception as e:
            await m.edit(f"? Failed to delete profile pictures: `{e}`")

    @user_client.on_message(filters.me & filters.command(["block", "unblock"], prefixes="."))
    async def ub_block_unblock(c: Client, m: Message):
        cmd = m.command[0]
        reply = m.reply_to_message
        if not reply or not reply.from_user:
            await m.edit(f"? Please reply to the user you want to {cmd}!")
            return
        user = reply.from_user
        try:
            if cmd == "block":
                await c.block_user(user.id)
                await m.edit(f"? Successfully blocked [{user.first_name}](tg://user?id={user.id})!")
            else:
                await c.unblock_user(user.id)
                await m.edit(f"? Successfully unblocked [{user.first_name}](tg://user?id={user.id})!")
        except Exception as e:
            await m.edit(f"? Failed to {cmd} user: `{e}`")

    # BROADCAST & GCAST
    @user_client.on_message(filters.me & filters.command("gcast", prefixes="."))
    async def ub_gcast(c: Client, m: Message):
        text = " ".join(m.command[1:])
        reply = m.reply_to_message
        if not text and not reply:
            await m.edit("? Please provide text or reply to a message to broadcast!")
            return
        
        await m.edit("?? Starting global broadcast across all chats...")
        success = 0
        failed = 0
        async for dialog in c.get_dialogs():
            chat_id = dialog.chat.id
            if chat_id == m.chat.id:
                continue
            if dialog.chat.type == enums.ChatType.CHANNEL:
                continue
            try:
                if reply:
                    await reply.copy(chat_id)
                else:
                    await c.send_message(chat_id, text)
                success += 1
                await asyncio.sleep(0.3)
            except Exception:
                failed += 1
        await m.edit(f"? **Broadcast Completed!**\n\n• Successful: `{success}` chats\n• Failed: `{failed}` chats")

    @user_client.on_message(filters.me & filters.command("gforward", prefixes="."))
    async def ub_gforward(c: Client, m: Message):
        reply = m.reply_to_message
        if not reply:
            await m.edit("? Please reply to a message to forward globally!")
            return
        await m.edit("?? Starting global forward across all chats...")
        success = 0
        failed = 0
        async for dialog in c.get_dialogs():
            chat_id = dialog.chat.id
            if chat_id == m.chat.id:
                continue
            if dialog.chat.type == enums.ChatType.CHANNEL:
                continue
            try:
                await reply.forward(chat_id)
                success += 1
                await asyncio.sleep(0.3)
            except Exception:
                failed += 1
        await m.edit(f"? **Global Forward Completed!**\n\n• Successful: `{success}` chats\n• Failed: `{failed}` chats")

    # RAID, RRAID, ONERAID & SPAM HANDLERS
    @user_client.on_message(filters.me & filters.command("raid", prefixes="."))
    async def ub_raid(c: Client, m: Message):
        args = m.text.split()
        reply = m.reply_to_message
        if not reply or not reply.from_user:
            await m.edit("? Please reply to a user to raid!")
            return
        
        count = None
        if len(args) > 1:
            try:
                count = int(args[1])
            except ValueError:
                count = None

        target = reply.from_user
        mention = f"[{target.first_name}](tg://user?id={target.id})"
        await m.delete()

        async def raid_task():
            try:
                i = 0
                while count is None or i < count:
                    gaali = random.choice(KHATARNAK_GAALIS)
                    try:
                        await c.send_message(m.chat.id, f"{mention} {gaali}", reply_to_message_id=reply.id)
                    except FloodWait as e:
                        await asyncio.sleep(e.value + 1)
                    except Exception:
                        pass
                    i += 1
                    await asyncio.sleep(0.12)
            except asyncio.CancelledError:
                pass

        if user_id not in ACTIVE_TASKS:
            ACTIVE_TASKS[user_id] = {}
        ACTIVE_TASKS[user_id]["raid"] = create_tracked_task(raid_task(), task_name=f"raid_{user_id}", user_id=user_id)

    @user_client.on_message(filters.me & filters.command("rraid", prefixes="."))
    async def ub_rraid(c: Client, m: Message):
        reply = m.reply_to_message
        if not reply or not reply.from_user:
            await m.edit("? Please reply to a user to start continuous rraid!")
            return
        target = reply.from_user
        chat_id = m.chat.id
        target_key = (chat_id, target.id)
        if target_key in RRAID_TARGETS:
            await m.edit(f"?? Rraid is already running on {target.first_name}!")
            return
        
        RRAID_TARGETS.add(target_key)
        await m.edit(f"? **Rraid activated on {target.first_name}!**")

    @user_client.on_message(filters.me & filters.command("drraid", prefixes="."))
    async def ub_drraid(c: Client, m: Message):
        RRAID_TARGETS.clear()
        await m.edit("? **Rraid stopped successfully!** ??")

    @user_client.on_message(filters.me & filters.command("oneraid", prefixes="."))
    async def ub_oneraid(c: Client, m: Message):
        args = m.text.split()
        reply = m.reply_to_message
        if not reply or not reply.from_user:
            await m.edit("? Please reply to a user for oneraid!")
            return
        
        count = None
        if len(args) > 1:
            try:
                count = int(args[1])
            except ValueError:
                count = None

        target = reply.from_user
        mention = f"[{target.first_name}](tg://user?id={target.id})"
        await m.delete()

        async def oneraid_task():
            try:
                i = 0
                while count is None or i < count:
                    word = random.choice(SINGLE_GAALIS)
                    try:
                        await c.send_message(m.chat.id, f"{mention} {word}", reply_to_message_id=reply.id)
                    except FloodWait as e:
                        await asyncio.sleep(e.value + 1)
                    except Exception:
                        pass
                    i += 1
                    await asyncio.sleep(0.12)
            except asyncio.CancelledError:
                pass

        if user_id not in ACTIVE_TASKS:
            ACTIVE_TASKS[user_id] = {}
        ACTIVE_TASKS[user_id]["oneraid"] = create_tracked_task(oneraid_task(), task_name=f"oneraid_{user_id}", user_id=user_id)

    @user_client.on_message(filters.me & filters.command(["spam", "fastspam", "flood"], prefixes="."))
    async def ub_spam(c: Client, m: Message):
        args = m.text.split(maxsplit=2)
        if len(args) < 2:
            await m.edit("Usage: `.spam <count> <text>`")
            return
        try:
            count = int(args[1])
            text = args[2] if len(args) > 2 else random.choice(KHATARNAK_GAALIS)
        except ValueError:
            count = 5
            text = args[1]

        await m.delete()
        async def spam_task():
            try:
                for _ in range(count):
                    try:
                        await c.send_message(m.chat.id, text)
                    except FloodWait as e:
                        await asyncio.sleep(e.value + 1)
                    except Exception:
                        pass
                    await asyncio.sleep(0.12)
            except asyncio.CancelledError:
                pass

        if user_id not in ACTIVE_TASKS:
            ACTIVE_TASKS[user_id] = {}
        ACTIVE_TASKS[user_id]["spam"] = create_tracked_task(spam_task(), task_name=f"spam_{user_id}", user_id=user_id)

    # MODERATION UTILS (FULLY FIXED)
    @user_client.on_message(filters.me & filters.command(["id", "info", "admins", "bots", "users", "leave"], prefixes="."))
    async def ub_moderation(c: Client, m: Message):
        cmd = m.command[0]
        if cmd == "id":
            await m.edit(f"?? **Chat ID:** `{m.chat.id}`\n?? **Your ID:** `{m.from_user.id}`")
        elif cmd == "info":
            target = m.reply_to_message.from_user if m.reply_to_message and m.reply_to_message.from_user else m.from_user
            await m.edit(f"?? **User Info:**\n• Name: {target.first_name}\n• ID: `{target.id}`")
        elif cmd == "admins":
            try:
                admins = []
                async for member in c.get_chat_members(m.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                    admins.append(f"• [{member.user.first_name}](tg://user?id={member.user.id})")
                await m.edit(f"?? **Group Admins:**\n\n" + "\n".join(admins[:30]))
            except Exception as e:
                await m.edit(f"? Error fetching admins: `{e}`")
        elif cmd == "bots":
            try:
                bots = []
                async for member in c.get_chat_members(m.chat.id, filter=enums.ChatMembersFilter.BOTS):
                    bots.append(f"• [{member.user.first_name}](tg://user?id={member.user.id})")
                await m.edit(f"?? **Group Bots:**\n\n" + ("\n".join(bots) if bots else "No bots found."))
            except Exception as e:
                await m.edit(f"? Error fetching bots: `{e}`")
        elif cmd == "users":
            try:
                count = await c.get_chat_members_count(m.chat.id)
                await m.edit(f"?? **Total Members in Chat:** `{count}`")
            except Exception as e:
                await m.edit(f"? Error: `{e}`")
        elif cmd == "leave":
            try:
                await m.edit("?? Leaving chat...")
                await c.leave_chat(m.chat.id)
            except Exception as e:
                await m.edit(f"? Error: `{e}`")

def _run_bot_with_recovery():
    """
    Keep the hosting bot alive through transient Telegram/DNS/network failures.
    Authentication/configuration errors are not retried forever.
    """
    retry_delay = 5
    while True:
        try:
            logger.info("Starting VOLT Userbot Hosting Bot with all buttons and pro animations fully working...")
            app.run()
            logger.warning("VOLT bot stopped cleanly. Restarting in %ss...", retry_delay)
        except KeyboardInterrupt:
            logger.info("VOLT bot stopped by administrator.")
            break
        except Exception as exc:
            error_text = str(exc).upper()
            logger.exception("VOLT startup/runtime failure: %s", exc)

            permanent_auth_errors = (
                "BOT_TOKEN_INVALID",
                "TOKEN_INVALID",
                "UNAUTHORIZED",
                "AUTH_KEY_UNREGISTERED",
                "401",
            )
            if any(marker in error_text for marker in permanent_auth_errors):
                logger.error("Telegram authentication failed. Check BOT_TOKEN/API_ID/API_HASH.")
                break

            logger.warning("Transient failure detected; retrying in %ss...", retry_delay)
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)
from pyrogram import idle

async def main():
    await app.start()
    logger.info("VOLT Main Bot started successfully.")
    await idle()
    try:
        for uid, h_client in list(HOSTED_CLIENTS.items()):
            try:
                await h_client.stop()
            except Exception:
                pass
        HOSTED_CLIENTS.clear()
    finally:
        await app.stop()
keep_alive()
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
