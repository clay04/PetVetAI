# controller/chatbot_controller.py

from service.fonnte_service import send_whatsapp
from service.gemini_service import analyze_pet_health
from model.user_model import User
from model.chat_model import ChatHistory
from model.database import db
from view.response_format import menu_text, tips_care, vaccine_info, help_info

def get_user_history(user, limit=10):
    chats = ChatHistory.query.filter_by(user_id=user.id) \
                             .order_by(ChatHistory.timestamp.desc()) \
                             .limit(limit).all()
    
    if not chats:
        return "Tidak ada riwayat konsultasi sebelumnya."

    result = "*📜 Riwayat Konsultasi Terakhir:*\n\n"
    for c in reversed(chats):
        result += f"• Kamu: {c.message}\n  Bot: {c.response[:50]}...\n\n"
    
    return result


def handle_message(sender, message):
    user = User.get_or_create_user(sender)

    text = message.lower().strip()

    # MENU UTAMA
    if text in ["menu", "start", "mulai", "hi", "halo"]:
        send_whatsapp(sender, menu_text())  
        return

    # PILIHAN MENU
    if text == "1":
        send_whatsapp(sender, "Silakan jelaskan gejala hewan Anda 🐾")
        return

    if text == "2":
        send_whatsapp(sender, tips_care())
        return

    if text == "3":
        send_whatsapp(sender, vaccine_info())
        return

    if text == "4":
        history = get_user_history(user)
        send_whatsapp(sender, history)
        return

    if text == "5":
        send_whatsapp(sender, help_info())
        return

    # ================
    # DEFAULT: KONSULTASI
    # ================
    response = analyze_pet_health(text)

    # Simpan ke database
    chat = ChatHistory(
        user_id=user.id,
        message=message,
        response=response
    )

    db.session.add(chat)
    db.session.commit()

    # Kirim jawaban
    send_whatsapp(sender, response)
