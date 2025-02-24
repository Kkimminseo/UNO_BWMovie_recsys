from django.http import JsonResponse
from django.shortcuts import render
from django.middleware.csrf import get_token

def serve_react(request):
    return render(request, "index.html")  # React의 index.html 렌더링
def get_csrf_token(request):
    response = JsonResponse({"csrfToken": get_token(request)})
    response.set_cookie("csrftoken", get_token(request), samesite='Lax')  # ✅ CSRF 쿠키 설정 강제
    return response
