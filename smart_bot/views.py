# import uuid
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib import messages
# from django.utils.safestring import mark_safe
# import markdown
# from .models import ChatSession, ChatMessage
#
# # OpenAI client
# from openai import OpenAI
# from django.conf import settings
#
# client = OpenAI(api_key=settings.OPENAI_API_KEY)
#
# # --- HOME PAGE: List Chats ---
# @login_required
# def chat_home(request):
#     chats = ChatSession.objects.filter(user=request.user).order_by("-created_at")
#     return render(request, "smart_bot/smart_bot_home.html", {"chats": chats})
#
# # --- CREATE NEW CHAT ---
# @login_required
# def new_chat(request):
#     chat = ChatSession.objects.create(
#         user=request.user,
#         session_id=str(uuid.uuid4()),
#         title="New UIU Lecture Chat"
#     )
#     return redirect("chat_detail", chat_id=chat.id)
#
# # --- CHAT DETAIL ---
# @login_required
# def chat_detail(request, chat_id):
#     chat = get_object_or_404(ChatSession, id=chat_id, user=request.user)
#     messages_list = ChatMessage.objects.filter(chat=chat).order_by("created_at")
#     return render(request, "smart_bot/chat_detail.html", {"chat": chat, "messages": messages_list})
#
# # --- SEND MESSAGE & GET AI RESPONSE ---
# @csrf_exempt
# @login_required
# def chat_message(request, chat_id):
#     if request.method == "POST":
#         chat = get_object_or_404(ChatSession, id=chat_id, user=request.user)
#         user_text = request.POST.get("message", "").strip()
#         file = request.FILES.get("file")
#
#         # Save user message
#         if user_text or file:
#             ChatMessage.objects.create(
#                 chat=chat,
#                 sender="user",
#                 text=user_text,
#                 file=file if file else None
#             )
#             # Update chat title if default
#             if chat.title == "New UIU Lecture Chat" and user_text:
#                 chat.title = user_text[:50]
#                 chat.save()
#
#         # Default AI response
#         ai_response = "Sorry, I couldn’t process that."
#
#         # --- Call OpenAI API ---
#         if user_text or file:
#             try:
#                 system_prompt = """
# You are an AI specialized for United International University (UIU) students.
# You know UIU course structures, departments, faculty, and lecture styles.
# Summarize lecture content, answer student questions, and explain UIU-specific topics clearly.
# If a file is uploaded (PDF, TXT, DOCX), extract and summarize the content in short bullets.
# Always keep context to UIU.
# """
#                 user_input = user_text
#                 if file:
#                     user_input += "\n\n📎 File uploaded: Summarize content in UIU context."
#
#                 completion = client.chat.completions.create(
#                     model="gpt-4o-mini",
#                     messages=[
#                         {"role": "system", "content": system_prompt},
#                         {"role": "user", "content": user_input}
#                     ]
#                 )
#                 ai_response = completion.choices[0].message.content
#
#             except Exception as e:
#                 ai_response = f"AI Error: {str(e)}"
#
#         # Convert Markdown to HTML
#         ai_html = mark_safe(markdown.markdown(ai_response))
#
#         # Save AI response
#         ChatMessage.objects.create(
#             chat=chat,
#             sender="ai",
#             text=ai_html
#         )
#
#         return JsonResponse({"response": ai_html})
#
#     return JsonResponse({"error": "Invalid request"}, status=400)
#
# # --- DELETE CHAT ---
# @login_required
# def delete_chat(request, chat_id):
#     chat = get_object_or_404(ChatSession, id=chat_id, user=request.user)
#     if request.method == "POST":
#         chat.delete()
#         messages.success(request, "Chat deleted successfully!")
#     return redirect("chat_home")


import uuid
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.safestring import mark_safe
import markdown
from .models import ChatSession, ChatMessage
from openai import OpenAI
from django.conf import settings

# OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


# --- HOME PAGE: List Chats ---
@login_required
def chat_home(request):
    chats = ChatSession.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "smart_bot/smart_bot_home.html", {"chats": chats})


# --- CREATE NEW CHAT ---
@login_required
def new_chat(request):
    chat = ChatSession.objects.create(
        user=request.user,
        session_id=str(uuid.uuid4()),
        title="New UIU Lecture Chat"
    )
    return redirect("chat_detail", chat_id=chat.id)


# --- CHAT DETAIL ---
@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(ChatSession, id=chat_id, user=request.user)
    messages_list = ChatMessage.objects.filter(chat=chat).order_by("created_at")
    return render(request, "smart_bot/chat_detail.html", {"chat": chat, "messages": messages_list})


# --- SEND MESSAGE & GET AI RESPONSE ---
@csrf_exempt
@login_required
def chat_message(request, chat_id):
    if request.method == "POST":
        chat = get_object_or_404(ChatSession, id=chat_id, user=request.user)
        user_text = request.POST.get("message", "").strip()
        file = request.FILES.get("file")

        # Save user message
        if user_text or file:
            ChatMessage.objects.create(
                chat=chat,
                sender="user",
                text=user_text,
                file=file if file else None
            )
            # Update chat title if default
            if chat.title == "New UIU Lecture Chat" and user_text:
                chat.title = user_text[:50]
                chat.save()

        # Default AI response
        ai_response = "Sorry, I couldn’t process that."

        # --- Call OpenAI API ---
        if user_text or file:
            try:
                system_prompt = """
You are an AI specialized for United International University (UIU) students.
You know UIU course structures, departments, faculty, and lecture styles.
Summarize lecture content, answer student questions, and explain UIU-specific topics clearly.
If a file is uploaded (PDF, TXT, DOCX), extract and summarize the content in short bullets.
Always keep context to UIU.
Always use proper line spacing, bullets, and numbered lists.
"""
                user_input = user_text
                if file:
                    user_input += "\n\n📎 File uploaded: Summarize content in UIU context."

                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ]
                )
                ai_response = completion.choices[0].message.content

            except Exception as e:
                ai_response = f"AI Error: {str(e)}"

        # --- Preprocess AI text for better Markdown ---
        def preprocess_markdown(text):
            # Replace multiple empty lines with a single line break
            text = re.sub(r'\n\s*\n', '\n\n', text)

            # Convert plain numbered lists to Markdown style
            text = re.sub(r'^\s*(\d+)[.)]\s+', r'\1. ', text, flags=re.MULTILINE)

            # Convert plain dashes or bullets to Markdown bullets
            text = re.sub(r'^\s*[-–*]\s+', '- ', text, flags=re.MULTILINE)

            # Ensure spacing after bullets
            text = re.sub(r'(- )([^\s])', r'\1\2', text)

            return text

        ai_response = preprocess_markdown(ai_response)

        # Convert Markdown to HTML with extra extensions for better formatting
        ai_html = mark_safe(markdown.markdown(ai_response, extensions=['extra', 'nl2br']))

        # Save AI response
        ChatMessage.objects.create(
            chat=chat,
            sender="ai",
            text=ai_html
        )

        return JsonResponse({"response": ai_html})

    return JsonResponse({"error": "Invalid request"}, status=400)


# --- DELETE CHAT ---
@login_required
def delete_chat(request, chat_id):
    chat = get_object_or_404(ChatSession, id=chat_id, user=request.user)
    if request.method == "POST":
        chat.delete()
        messages.success(request, "Chat deleted successfully!")
    return redirect("smart_bot_home")