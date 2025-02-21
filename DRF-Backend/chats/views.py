from django.shortcuts import render

def chat_page(request):
    return render(request, 'chats/index.html')