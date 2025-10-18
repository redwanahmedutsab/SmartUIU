import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import ChatSession, ChatMessage
from django.utils.safestring import mark_safe
import markdown

# OpenAI client
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)


# --- CHAT HOME ---
def chat_home(request):
    chats = ChatSession.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "smart_bot/smart_bot_home.html", {"chats": chats})


# --- CREATE NEW CHAT ---
def new_chat(request):
    chat = ChatSession.objects.create(
        user=request.user,
        session_id=str(uuid.uuid4()),
        title="New Lecture Chat"
    )
    return redirect("chat_detail", chat_id=chat.id)


# --- CHAT DETAIL ---
def chat_detail(request, chat_id):
    chat = get_object_or_404(ChatSession, id=chat_id, user=request.user)
    messages = ChatMessage.objects.filter(chat=chat).order_by("created_at")
    return render(request, "smart_bot/chat_detail.html", {"chat": chat, "messages": messages})


# --- SEND MESSAGE & GET AI RESPONSE ---
@csrf_exempt
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

            if chat.title == "New Lecture Chat" and user_text:
                chat.title = user_text[:50]  # limit to 50 chars
                chat.save()

        # Default AI response
        ai_response = "Sorry, I couldn’t process that."

        # Call OpenAI API for AI response
        if user_text:
            try:
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a lecture summarizer AI."},
                        {"role": "user", "content": user_text}
                    ]
                )
                ai_response = completion.choices[0].message.content
            except Exception as e:
                ai_response = f"AI Error: {str(e)}"

        # If file uploaded
        if file:
            ai_response += "\n\n(📎 File received: will be summarized soon.)"

        # Convert AI response from Markdown to HTML
        ai_html = mark_safe(markdown.markdown(ai_response))

        # Save AI response
        ChatMessage.objects.create(
            chat=chat,
            sender="ai",
            text=ai_html
        )

        return JsonResponse({"response": ai_html})

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def delete_chat(request, chat_id):
    chat = get_object_or_404(ChatSession, id=chat_id, user=request.user)
    if request.method == "POST":
        chat.delete()
        messages.success(request, "Chat deleted successfully!")
    return redirect("smart_bot_home")  # or wherever your chat list is
