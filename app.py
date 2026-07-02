import time
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# --- الإعدادات الأساسية ---
TOKEN = "8787548951:AAHVabUXTaQWKQRxwsURRcfRtdrLJWjyjEQ"
CHANNEL_USERNAME = "@rexmodstop1"  # معرف قناتك للاشتراك الإجباري في الخاص

# --- روابط الـ APIs المحدثة ---
API_INFO = "http://187.127.175.208:5000/Bmw"
API_JWT = "http://187.127.175.208:5001/Bmw"  # تم التحديث بناءً على طلبك لجلب توكن جوات
API_BIO = "http://shappno-long-bio-api-ob54.vercel.app/bio_upload"
API_EAT = "http://shappno-eat-to-access-api-ob54.vercel.app/access_token"
API_ITEM = "http://shappno-profile-item-api-ob54-fhh.vercel.app/item"
API_CLAN = "https://star-guild-info.lovable.app/api/public/info"

# --- النصوص واللغات الرسمية للبوت ---
STRINGS = {
    "ar": {
        "start": """🎮 𝙒𝙀𝙇𝘾𝙊𝙈𝙀 𝙏𝙊 𝙍𝙀𝙓 𝘽𝙊𝙏 𝙁𝙍𝙀𝙀 𝙁𝙄𝙍𝙀 𝙏𝙊𝙊𝙇𝙎 𝘽𝙊𝙏

⏳ : ▰▱▱▱▱ 20%
[▓▓░░░░░░░░] 25%
𝒅𝒆𝒗𝒆𝒍𝒐𝒑𝒆𝒓@Rexadmin23

📜 قائمة الأوامر:

🔍 /info UID
جلب معلومات اللاعب الكاملة منظم بالإيموجي.

🛡️ /clan CLAN_ID REGION
 (مثال: /clan 3086500970 BD).

🔑 /jwt UID PASSWORD
استخراج JWT Token و Access Token من السيرفر الجديد.

🎒 /item JWT_TOKEN ITEM_ID
رفع سكنات أو رقصات وهمية في الحساب.

🍿 /eat JWT_TOKEN
تفعيل ميزة الـ Eat To Access لتثبيت الرقصات والسكنات.

📝 /bio JWT_TOKEN TEXT
تعديل بيو الحساب الطويل (أكثر من 500 حرف).

📊 /ping
فحص سرعة استجابة البوت السحابي.

🌐 /lang
تغيير لغة البوت.""",
        "sub_required": "❌ يجب عليك الاشتراك في قناة البوت أولاً لتتمكن من استخدامه!\n\nاشترك هنا: {channel}\n\nبعد الاشتراك، أرسل /start مجدداً.",
        "sub_button": "📢 اشترك في القناة",
        "lang_select": "🌐 الرجاء اختيار لغة البوت الرسمية:",
        "lang_success": "✅ تم تغيير لغة البوت إلى العربية بنجاح!",
        "error_args": "❌ الاستخدام الخاطئ للأمر! يرجى كتابة المدخلات بشكل صحيح.",
        "loading": "⏳ جاري جلب البيانات ومعالجة طلبك، يرجى الانتظار...",
        "api_error": "❌ حدث خطأ أثناء الاتصال بالخادم الداخلي أو البيانات غير صحيحة."
    },
    "en": {
        "start": """🎮 𝙒𝙀𝙇𝘾𝙊𝙈𝙀 𝙏𝙊 𝙍𝙀𝙓 𝘽𝙊𝙏

⏳ : ▰▱▱▱▱ 20%
[▓▓░░░░░░░░] 25%
𝒅𝒆𝒗𝒆𝒍𝒐𝒑𝒆𝒓@Rexadmin23

📜 Commands List:
🔍 /info UID
Fetch complete player profile info.

🛡️ /clan CLAN_ID REGION
Fetch complete clan info (e.g., /clan 3086500970 BD).

🔑 /jwt UID PASSWORD
Extract JWT Token and Access Token.

🎒 /item JWT_TOKEN ITEM_ID
Equip visual/glitch items or emotes.

🍿 /eat JWT_TOKEN
Activate Eat To Access feature.

📝 /bio JWT_TOKEN TEXT
Set an extended custom account bio (>500 chars).

📊 /ping
Check bot application response latency.

🌐 /lang
Change the bot display language.""",
        "sub_required": "❌ You must subscribe to our channel first to use this bot!\n\nJoin here: {channel}\n\nAfter joining, send /start again.",
        "sub_button": "📢 Join Channel",
        "lang_select": "🌐 Please select your preferred language:",
        "lang_success": "✅ Language successfully set to English!",
        "error_args": "❌ Invalid command format! Please check your arguments.",
        "loading": "⏳ Processing your request and fetching data, please wait...",
        "api_error": "❌ An error occurred while contacting the server or data is invalid."
    },
    "fr": {
        "start": """🎮 Bienvenue sur Free Fire Tools Bot

⏳ : ▰▱▱▱▱ 20%
[▓▓░░░░░░░░] 25%
𝒅𝒆𝒗𝒆𝒍𝒐𝒑𝒆𝒓@Rexadmin23

📜 Liste des Commandes:

🔍 /info UID
Obtenir les informations complètes du joueur.

🛡️ /clan CLAN_ID REGION
Obtenir les infos du clan (Ex: /clan 3086500970 BD).

🔑 /jwt UID PASSWORD
Extraire le token JWT et le token d'accès.

🎒 /item JWT_TOKEN ITEM_ID
Équiper des skins ou des emotes visuels.

🍿 /eat JWT_TOKEN
Activer la fonctionnalité Eat To Access.

📝 /bio JWT_TOKEN TEXT
Définir une bio de compte étendue (>500 caractères).

📊 /ping
Vérifier la latence de réponse du bot.

🌐 /lang
Changer la langue du bot.""",
        "sub_required": "❌ Vous devez d'abord vous abonner à notre chaîne pour utiliser ce bot!\n\nRejoignez ici: {channel}\n\nAprès avoir rejoint, renvoyez /start.",
        "sub_button": "📢 Rejoindre la chaîne",
        "lang_select": "🌐 Veuillez sélectionner votre langue préférée:",
        "lang_success": "✅ Langue configurée en Français avec succès!",
        "error_args": "❌ Format de commande invalide! Veuillez vérifier vos arguments.",
        "loading": "⏳ Traitement de votre demande en cours, veuillez patienter...",
        "api_error": "❌ Une erreur est survenue lors du contact avec le serveur."
    }
}

user_languages = {}

def get_user_lang(user_id):
    return user_languages.get(user_id, "ar")

# دالة التحقق من الاشتراك الإجباري
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if update.effective_chat.type != "private":
        return True
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=update.effective_user.id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except Exception:
        pass

    lang = get_user_lang(update.effective_user.id)
    keyboard = [[InlineKeyboardButton(STRINGS[lang]["sub_button"], url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        STRINGS[lang]["sub_required"].format(channel=CHANNEL_USERNAME),
        reply_markup=reply_markup,
        reply_to_message_id=update.message.message_id
    )
    return False

# أمر البدء /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        return
    lang = get_user_lang(update.effective_user.id)
    await update.message.reply_text(STRINGS[lang]["start"], reply_to_message_id=update.message.message_id)

# دالة تغيير اللغة /lang
async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        return
    lang = get_user_lang(update.effective_user.id)
    keyboard = [
        [
            InlineKeyboardButton("🇸🇦 العربية", callback_data="set_lang_ar"),
            InlineKeyboardButton("🇺🇸 English", callback_data="set_lang_en"),
            InlineKeyboardButton("🇫🇷 Français", callback_data="set_lang_fr")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(STRINGS[lang]["lang_select"], reply_markup=reply_markup, reply_to_message_id=update.message.message_id)

# معالج ضغطات الأزرار (تغيير اللغة)
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "set_lang_ar":
        user_languages[user_id] = "ar"
    elif data == "set_lang_en":
        user_languages[user_id] = "en"
    elif data == "set_lang_fr":
        user_languages[user_id] = "fr"

    lang = user_languages[user_id]
    await query.edit_message_text(STRINGS[lang]["lang_success"])
    await context.bot.send_message(chat_id=query.message.chat_id, text=STRINGS[lang]["start"])

# دالة محاكاة وتحديث تأثير الأنيميشن عند معالجة الطلبات
async def play_loading_animation(message):
    try:
        await message.edit_text("⏳ : ▰▱▱▱▱ 20%\n[▓▓░░░░░░░░] 25%\n🔄 جاري الاتصال بالسيرفرات...")
        time.sleep(0.4)
        await message.edit_text("⏳ : ▰▰▰▱▱ 60%\n[▓▓▓▓▓▓░░░░] 60%\n⚡ يتم الآن فك وتنسيق البيانات...")
        time.sleep(0.4)
        await message.edit_text("⏳ : ▰▰▰▰▰ 100%\n[▓▓▓▓▓▓▓▓▓▓] 100%\n✅ تم جلب البيانات بنجاح!")
    except Exception:
        pass

# أمر جلب معلومات اللاعب /info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        return
    lang = get_user_lang(update.effective_user.id)
    if not context.args:
        await update.message.reply_text(STRINGS[lang]["error_args"], reply_to_message_id=update.message.message_id)
        return

    uid = context.args[0]
    loading_msg = await update.message.reply_text(STRINGS[lang]["loading"], reply_to_message_id=update.message.message_id)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    
    # تشغيل تأثير الأنيميشن المطلوب
    await play_loading_animation(loading_msg)

    try:
        response = requests.get(f"{API_INFO}?uid={uid}", timeout=15)
        if response.status_code == 200:
            data = response.json()
            formatted_text = f"🔍 *👤 Player Info (UID: {uid}):*\n\n"
            for key, value in data.items():
                formatted_text += f"🔹 *{key.replace('_', ' ').title()}:* `{value}`\n"
            formatted_text += f"\n⚙️ _Developer:_ @Rexadmin23"
            await loading_msg.edit_text(formatted_text, parse_mode="Markdown")
        else:
            await loading_msg.edit_text(STRINGS[lang]["api_error"])
    except Exception:
        await loading_msg.edit_text(STRINGS[lang]["api_error"])

# أمر جلب معلومات الكلان /clan
async def clan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        return
    lang = get_user_lang(update.effective_user.id)
    if len(context.args) < 2:
        await update.message.reply_text(STRINGS[lang]["error_args"], reply_to_message_id=update.message.message_id)
        return

    clan_id = context.args[0]
    region = context.args[1].upper()
    
    loading_msg = await update.message.reply_text(STRINGS[lang]["loading"], reply_to_message_id=update.message.message_id)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    
    # تشغيل تأثير الأنيميشن المطلوب
    await play_loading_animation(loading_msg)

    try:
        response = requests.get(f"{API_CLAN}?clan_id={clan_id}&region={region}", timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                formatted_text = f"🛡️ *Clan Info ({clan_id} - {region}):*\n\n"
                formatted_text += f"👑 *Guild ID:* `{data.get('guild_id')}`\n"
                formatted_text += f"🌟 *Level:* `{data.get('guild_level')}`\n"
                formatted_text += f"👥 *Members:* `{data.get('current_members')}/{data.get('total_members')}`\n"
                formatted_text += f"🔥 *Glory Points:* `{data.get('glory_points')}`\n"
                formatted_text += f"👤 *Leader ID:* `{data.get('guild_leader_id')}`\n"
                formatted_text += f"📅 *Created At:* `{data.get('created_at')}`\n"
                formatted_text += f"💬 *Bio:* `{data.get('guild_bio')}`\n"
                formatted_text += f"👋 *Welcome Msg:* `{data.get('welcome_message')}`\n"
                formatted_text += f"📈 *XP:* `{data.get('xp')}`\n\n"
                formatted_text += f"⚙️ _Developer:_ @Rexadmin23"
                
                await loading_msg.edit_text(formatted_text, parse_mode="Markdown")
            else:
                await loading_msg.edit_text(STRINGS[lang]["api_error"])
        else:
            await loading_msg.edit_text(STRINGS[lang]["api_error"])
    except Exception:
        await loading_msg.edit_text(STRINGS[lang]["api_error"])

# أمر استخراج الـ JWT Token المحدث بالسيرفر الجديد
async def jwt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        return
    lang = get_user_lang(update.effective_user.id)
    if len(context.args) < 2:
        await update.message.reply_text(STRINGS[lang]["error_args"], reply_to_message_id=update.message.message_id)
        return

    uid, password = context.args[0], context.args[1]
    loading_msg = await update.message.reply_text(STRINGS[lang]["loading"], reply_to_message_id=update.message.message_id)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    
    # تشغيل تأثير الأنيميشن المطلوب
    await play_loading_animation(loading_msg)

    try:
        response = requests.get(f"{API_JWT}?uid={uid}&password={password}", timeout=15)
        if response.status_code == 200:
            data = response.json()
            formatted_text = "🔑 *Tokens Extracted Successfully:*\n\n"
            for key, value in data.items():
                formatted_text += f"🔸 *{key.upper()}:*\n`{value}`\n\n"
            formatted_text += f"⚙️ _Developer:_ @Rexadmin23"
            await loading_msg.edit_text(formatted_text, parse_mode="Markdown")
        else:
            await loading_msg.edit_text(STRINGS[lang]["api_error"])
    except Exception:
        await loading_msg.edit_text(STRINGS[lang]["api_error"])

# أمر رفع الرقصات والسكنات /item
async def item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        return
    lang = get_user_lang(update.effective_user.id)
    if len(context.args) < 2:
        await update.message.reply_text(STRINGS[lang]["error_args"], reply_to_message_id=update.message.message_id)
        return

    jwt_token, item_id = context.args[0], context.args[1]
    loading_msg = await update.message.reply_text(STRINGS[lang]["loading"], reply_to_message_id=update.message.message_id)
    
    await play_loading_animation(loading_msg)

    try:
        response = requests.get(f"{API_ITEM}?jwt={jwt_token}&item_id={item_id}", timeout=15)
        if response.status_code == 200:
            await loading_msg.edit_text(f"✅ *Response:* `{response.text}`\n\n⚙️ _Developer:_ @Rexadmin23", parse_mode="Markdown")
        else:
            await loading_msg.edit_text(STRINGS[lang]["api_error"])
    except Exception:
        await loading_msg.edit_text(STRINGS[lang]["api_error"])

# أمر الـ Eat to access
async def eat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        return
    lang = get_user_lang(update.effective_user.id)
    if not context.args:
        await update.message.reply_text(STRINGS[lang]["error_args"], reply_to_message_id=update.message.message_id)
        return

    jwt_token = context.args[0]
    loading_msg = await update.message.reply_text(STRINGS[lang]["loading"], reply_to_message_id=update.message.message_id)
    
    await play_loading_animation(loading_msg)

    try:
        response = requests.get(f"{API_EAT}?jwt={jwt_token}", timeout=15)
        if response.status_code == 200:
            await loading_msg.edit_text(f"✅ *Response:* `{response.text}`\n\n⚙️ _Developer:_ @Rexadmin23", parse_mode="Markdown")
        else:
            await loading_msg.edit_text(STRINGS[lang]["api_error"])
    except Exception:
        await loading_msg.edit_text(STRINGS[lang]["api_error"])

# أمر البيو الطويل /bio
async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        return
    lang = get_user_lang(update.effective_user.id)
    if len(context.args) < 2:
        await update.message.reply_text(STRINGS[lang]["error_args"], reply_to_message_id=update.message.message_id)
        return

    jwt_token = context.args[0]
    text = " ".join(context.args[1:])
    loading_msg = await update.message.reply_text(STRINGS[lang]["loading"], reply_to_message_id=update.message.message_id)
    
    await play_loading_animation(loading_msg)

    try:
        response = requests.get(f"{API_BIO}?jwt={jwt_token}&text={text}", timeout=15)
        if response.status_code == 200:
            await loading_msg.edit_text(f"✅ *Response:* `{response.text}`\n\n⚙️ _Developer:_ @Rexadmin23", parse_mode="Markdown")
        else:
            await loading_msg.edit_text(STRINGS[lang]["api_error"])
    except Exception:
        await loading_msg.edit_text(STRINGS[lang]["api_error"])

# أمر فحص السرعة /ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    message = await update.message.reply_text("📊 Checking speed...", reply_to_message_id=update.message.message_id)
    ping_ms = round((time.time() - start_time) * 1000)
    await message.edit_text(f"🚀 Speed: {ping_ms}ms\n\n⚙️ _Developer:_ @Rexadmin23")

# --- 🎬 تهيئة وإقلاع البوت 🎬 ---
def main():
    application = Application.builder().token(TOKEN).build()

    # تسجيل مستمعي الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("clan", clan))
    application.add_handler(CommandHandler("jwt", jwt))
    application.add_handler(CommandHandler("item", item))
    application.add_handler(CommandHandler("eat", eat))
    application.add_handler(CommandHandler("bio", bio))
    application.add_handler(CommandHandler("lang", lang_command))
    application.add_handler(CommandHandler("ping", ping))
    
    # مستمع الأزرار التفاعلية
    application.add_handler(CallbackQueryHandler(button_callback))

    # بدء تشغيل البوت
    print("🤖 Bot is successfully running...")
    application.run_polling()

if __name__ == '__main__':
    main()
ng...")
    application.run_polling()

if __name__ == '__main__':
    main()
