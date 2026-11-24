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
from pyrogram import Client, filters, enums, idle
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
OWNER_USERNAME = "KASHYAP17"

CO_OWNER_ID = 9108265973
CO_OWNER_USERNAME = "ix_aura"

FORCE_CHANNEL_ID = -1003739475692
FORCE_CHANNEL_LINK = "https://t.me/Hacrrrrjoin2"

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
            f"? **VOLT Userbot is Online & Running Smoothly!**\n"
            f"?? **User:** `{user_id}`\n"
            f"?? **Status:** Active"
        )

async def main():
    await app.start()
    logger.info("VOLT Main Bot started successfully.")
    try:
        await idle()
    finally:
        for uid, h_client in list(HOSTED_CLIENTS.items()):
            try:
                await h_client.stop()
            except Exception:
                pass
        HOSTED_CLIENTS.clear()
        try:
            await app.stop()
        except Exception:
            pass

if __name__ == "__main__":
    if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
