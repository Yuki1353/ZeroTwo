import requests
from ZeroTwo import dispatcher, DICT_API
from ZeroTwo.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async


@run_async
def ud(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text[len('/ud '):]
    results = requests.get(
        f'https://api.urbandictionary.com/v0/define?term={text}').json()
    try:
        reply_text = f'*{text}*\n\n{results["list"][0]["definition"]}\n\n_{results["list"][0]["example"]}_'
    except:
        reply_text = "No results found."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)
    
    
    
#Dictionary module by @TheRealPhoenixBot.
@run_async
def define(update: Update, context: CallbackContext):
    msg = update.effective_message
    word = msg.text[len('/def '):]
    res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{word}")
    if res.status_code == 200:
        info = res.json()[0].get("meanings")
        if info:
            meaning = ""
            for count, (key, value) in enumerate(info.items(), start=1):
                meaning += f"<b>{count}. {word}</b> <i>({key})</i>\n"
                for i in value:
                    defs = i.get("definition")
                    meaning += f"• <i>{defs}</i>\n"
            msg.reply_text(meaning, parse_mode=ParseMode.HTML)
        else:
            return 
    else:
        msg.reply_text("No results found!")


UD_HANDLER = DisableAbleCommandHandler(["ud"], ud)
DEFINE_HANDLER = DisableAbleCommandHandler(["dict", "def"], define)

dispatcher.add_handler(UD_HANDLER)
dispatcher.add_handler(DEFINE_HANDLER)

__command_list__ = ["ud", "def"]
__handlers__ = [UD_HANDLER, DEFINE_HANDLER]
