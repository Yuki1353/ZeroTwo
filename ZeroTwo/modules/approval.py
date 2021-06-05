import html
from telegram import Chat, User, ParseMode, Update
from telegram.error import BadRequest
from telegram.utils.helpers import mention_html
from telegram import ParseMode
from telegram.ext import (run_async,
                          Filters, CommandHandler, CallbackContext)

from ZeroTwo import dispatcher, REDIS, DRAGONS
from ZeroTwo.modules.disable import DisableAbleCommandHandler
from ZeroTwo.modules.helper_funcs.chat_status import (
    bot_admin,
    user_admin
)
from ZeroTwo.modules.helper_funcs.extraction import extract_user_and_text
from ZeroTwo.modules.log_channel import loggable
from ZeroTwo.modules.helper_funcs.chat_status import user_admin



@run_async
def approval(update, context):
    chat = update.effective_chat  
    user = update.effective_user 
    message = update.effective_message
    args = context.args 
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("You don't seem to be referring to a user.")
        return 
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I can't seem to find this user")
            return 
        else:
            raise
    if user_id == context.bot.id:
        message.reply_text("How I supposed to approve myself!?")
        return 
    
    chat_id = str(chat.id)[1:] 
    approve_list = list(REDIS.sunion(f'approve_list_{chat_id}'))
    target_user = mention_html(member.user.id, member.user.first_name)
    if target_user in approve_list:
        message.reply_text(
            f"{member.user['first_name']} is an approved user. Locks, antiflood, and blocklists won't apply to them.",
        )
    else:
      message.reply_text(
        f"{member.user['first_name']} is not an approved user. They are affected by normal commands.",
      )



@loggable 
@run_async
@bot_admin
@user_admin
def approve(update, context):
    chat = update.effective_chat  
    user = update.effective_user 
    message = update.effective_message
    args = context.args 
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("You don't seem to be referring to a user.")
        return 
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I can't seem to find this user.")
            return 
        else:
            raise
    if user_id == context.bot.id:
        message.reply_text("You're high.")
        return 
    
    chat_id = str(chat.id)[1:] 
    approve_list = list(REDIS.sunion(f'approve_list_{chat_id}'))
    target_user = mention_html(member.user.id, member.user.first_name)
    if target_user in approve_list:
        message.reply_text(
            f"[{member.user['first_name']}](tg://user?id={member.user['id']}) is already approved in {chat_title}",
            parse_mode=ParseMode.MARKDOWN,
        )
        return ""
    member = chat.get_member(int(user_id))
    chat_id = str(chat.id)[1:]
    REDIS.sadd(f'approve_list_{chat_id}', mention_html(member.user.id, member.user.first_name))
    message.reply_text(
        f"[{member.user['first_name']}](tg://user?id={member.user['id']}) has been approved in {chat_title}! They will now be ignored by automated admin actions like locks, blocklists, and antiflood.",
        parse_mode=ParseMode.MARKDOWN,
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#APPROVED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    return log_message


@loggable
@run_async
@bot_admin
@user_admin
def unapprove(update, context):
    chat = update.effective_chat  
    user = update.effective_user 
    message = update.effective_message
    args = context.args 
    user_id, reason = extract_user_and_text(message, args)
    if not user_id:
        message.reply_text("You don't seem to be referring to a user.")
        return 
    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("I can't seem to find this user")
            return 
        else:
            raise
    if user_id == context.bot.id:
        message.reply_text("How I supposed to approve or unapprove myself!?")
        return 
    chat_id = str(chat.id)[1:] 
    approve_list = list(REDIS.sunion(f'approve_list_{chat_id}'))
    if target_user not in approve_list:
        message.reply_text(f"{member.user['first_name']} isn't approved yet!")
        return ""
    member = chat.get_member(int(user_id))
    chat_id = str(chat.id)[1:]
    REDIS.srem(f'approve_list_{chat_id}', mention_html(member.user.id, member.user.first_name))
    message.reply_text(
        f"{member.user['first_name']} is no longer approved in {chat_title}.",
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNAPPROVED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    return log_message

    
@run_async
@bot_admin
@user_admin
def approved(update, context):
    chat = update.effective_chat 
    user = update.effective_user 
    message = update.effective_message
    chat_id = str(chat.id)[1:] 
    approved_list = list(REDIS.sunion(f'approve_list_{chat_id}'))
    approved_list.sort()
    approved_list = "\n- ".join(approved_list)
    
    if approved_list: 
            message.reply_text(
                "The Following Users Are Approved:"
                "{}".format(approved_list),
                parse_mode=ParseMode.HTML
            )
    else:
        message.reply_text(
            "No users are are approved in {}.".format(chat.title),
                parse_mode=ParseMode.HTML
        )
"""
@run_async
@bot_admin
@user_admin
def unapproveall(update, context):
    chat = update.effective_chat 
    user = update.effective_user 
    message = update.effective_message
    chat_id = str(chat.id)[1:] 
    approve_list = list(REDIS.sunion(f'approve_list_{chat_id}'))
    for target_user in approve_list:
        REDIS.srem(f'approve_list_{chat_id}', target_user)
    message.reply_text(
        "Successully unapproved all users from {}.".format(chat.title)
    )
 """

@run_async
def unapproveall(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    if member.status != "creator" and user.id not in DRAGONS:
        update.effective_message.reply_text(
            "Only the chat owner can unapprove all users at once.",
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Unapprove all users", callback_data="unapproveall_user",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Cancel", callback_data="unapproveall_cancel",
                    ),
                ],
            ],
        )
        update.effective_message.reply_text(
            f"Are you sure you would like to unapprove ALL users in {chat.title}? This action cannot be undone.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN,
        )


@run_async
def unapproveall_btn(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    member = chat.get_member(query.from_user.id)
    if query.data == "unapproveall_user":
        if member.status == "creator" or query.from_user.id in DRAGONS:
              chat_id = str(chat.id)[1:]
            approve_list = list(REDIS.sunion(f'approve_list_{chat_id}'))
            for target_user in approve_list:
              REDIS.srem(f'approve_list_{chat_id}', target_user)
              message.edit_text("Successfully Unapproved all user in this Chat.")
              return
        if member.status == "administrator":
            query.answer("Only owner of the chat can do this.")

        if member.status == "member":
            query.answer("You need to be admin to do this.")
    elif query.data == "unapproveall_cancel":
        if member.status == "creator" or query.from_user.id in DRAGONS:
            message.edit_text("Removing of all approved users has been cancelled.")
            return ""
        if member.status == "administrator":
            query.answer("Only owner of the chat can do this.")
        if member.status == "member":
            query.answer("You need to be admin to do this.")
        
__mod_name__ = "Approval"    

__help__ = """ 
\
Specially authorized users having power on par with admins but can't use any admins command. Basically, they're admin without having any permissions.
Admin commands:
 • `/approval`*:* Check a user's approval status in this chat.
 • `/approve`*:* Approve of a user. Locks, blacklists, and antiflood won't apply to them anymore.
 • `/unapprove`*:* Unapprove of a user. They will now be subject to locks, blacklists, and antiflood again.
 • `/approved`*:* List all approved users.
 • `/unapproveall`*:* Unapprove ALL users in a chat. This cannot be undone.
\
"""    

APPROVED_HANDLER = DisableAbleCommandHandler("approved", approved, filters=Filters.group)
UNAPPROVE_ALL_HANDLER = DisableAbleCommandHandler("unapproveall", unapproveall, filters=Filters.group)
APPROVE_HANDLER = DisableAbleCommandHandler("approve", approve, pass_args=True, filters=Filters.group)
UNAPPROVE_HANDLER = DisableAbleCommandHandler("unapprove", unapprove, pass_args=True, filters=Filters.group)
APPROVAL_HANDLER = DisableAbleCommandHandler("approval", approval, pass_args=True, filters=Filters.group)


dispatcher.add_handler(APPROVED_HANDLER)
dispatcher.add_handler(UNAPPROVE_ALL_HANDLER)
dispatcher.add_handler(APPROVE_HANDLER) 
dispatcher.add_handler(UNAPPROVE_HANDLER) 
dispatcher.add_handler(APPROVAL_HANDLER)
