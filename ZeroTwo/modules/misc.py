from ZeroTwo.modules.helper_funcs.chat_status import user_admin
from ZeroTwo.modules.disable import DisableAbleCommandHandler
from ZeroTwo import dispatcher

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import MessageEntity, ParseMode, Update, Bot, Message
from telegram.ext.dispatcher import run_async
from telegram.ext import CallbackContext, Filters, CommandHandler

MARKDOWN_HELP = f"""
Markdown is a very powerful formatting tool supported by telegram. {dispatcher.bot.first_name} has some enhancements, to make sure that \
saved messages are correctly parsed, and to allow you to create buttons.

• <code>_italic_</code>: wrapping text with '_' will produce italic text
• <code>*bold*</code>: wrapping text with '*' will produce bold text
• <code>`code`</code>: wrapping text with '`' will produce monospaced text, also known as 'code'
• <code>[sometext](someURL)</code>: this will create a link - the message will just show <code>sometext</code>, \
and tapping on it will open the page at <code>someURL</code>.
<b>Example:</b><code>[test](example.com)</code>

• <code>[buttontext](buttonurl:someURL)</code>: this is a special enhancement to allow users to have telegram \
buttons in their markdown. <code>buttontext</code> will be what is displayed on the button, and <code>someurl</code> \
will be the url which is opened.
<b>Example:</b> <code>[This is a button](buttonurl:example.com)</code>

If you want multiple buttons on the same line, use :same, as such:
<code>[one](buttonurl://example.com)
[two](buttonurl://google.com:same)</code>
This will create two buttons on a single line, instead of one button per line.

Keep in mind that your message <b>MUST</b> contain some text other than just a button!
"""


@run_async
@user_admin
def echo(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message

    if message.reply_to_message:
        message.reply_to_message.reply_text(
            args[1], parse_mode="MARKDOWN", disable_web_page_preview=True)
    else:
        message.reply_text(
            args[1],
            quote=False,
            parse_mode="MARKDOWN",
            disable_web_page_preview=True)
    message.delete()


def markdown_help_sender(update: Update):
    update.effective_message.reply_text(
        MARKDOWN_HELP, parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(
        "Try forwarding the following message to me, and you'll see, and Use #test!"
    )
    update.effective_message.reply_text(
        "/save test This is a markdown test. _italics_, *bold*, code, "
        "[URL](example.com) [button](buttonurl:github.com) "
        "[button2](buttonurl://google.com:same)")


@run_async
def markdown_help(update: Update, context: CallbackContext):
    if update.effective_chat.type != "private":
        update.effective_message.reply_text(
            'Contact me in pm',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "Markdown help",
                    url=f"t.me/{context.bot.username}?start=markdownhelp")
            ]]))
        return
    markdown_help_sender(update)
    
    
#Dictionary module by @TheRealPhoenixBot.
@run_async
def define(bot: Bot, update: Update, args):
    msg = update.effective_message
    word = " ".join(args)
    res = requests.get(f"https://googledictionaryapi.eu-gb.mybluemix.net/?define={word}")
    if res.status_code == 200:
        info = res.json()[0].get("meaning")
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
        
        
        
__help__ = """
*Available commands:*
*Markdown:*
 • `/markdownhelp`*:* quick summary of how markdown works in telegram - can only be called in private chats
*Paste:*
 • `/paste`*:* Saves replied content to `nekobin.com` and replies with a url
*React:*
 • `/react`*:* Reacts with a random reaction 
*Urban Dictonary:*
 • `/ud <word>`*:* Type the word or expression you want to search use
*Dictionary:*
 - `/def <word>`*:* Accesses Dictionary and gives info about the word.
*Wikipedia:*
 • `/wiki <query>`*:* wikipedia your query
*Currency converter:* 
 • `/cash`*:* currency converter
Example:
 `/cash 1 USD INR`  
      _OR_
 `/cash 1 usd inr`
Output: `1.0 USD = 75.505 INR`

*Time*
 • `/time <query>`*:* Gives information about a timezone.
 - *Available queries:* Country Code/Country Name/Timezone Name [Timezones list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
 
*Sed*
 • `s/<text1>/<text2>(/<flag>)`*:* Reply to a message with this to perform a sed operation on that message, replacing all \
occurrences of 'text1' with 'text2'. [Example](https://t.me/FranXXSupport/2908)!
"""

ECHO_HANDLER = DisableAbleCommandHandler("echo", echo, filters=Filters.group)
MD_HELP_HANDLER = CommandHandler("markdownhelp", markdown_help)
DEFINE_HANDLER = DisableAbleCommandHandler(["dict", "def"], define)

dispatcher.add_handler(ECHO_HANDLER)
dispatcher.add_handler(MD_HELP_HANDLER)
dispatcher.add_handler(DEFINE_HANDLER)

__mod_name__ = "Extras"
__command_list__ = ["id", "echo", "time", "dict"]
__handlers__ = [
    ECHO_HANDLER,
    MD_HELP_HANDLER,
    DEFINE_HANDLER,
]
