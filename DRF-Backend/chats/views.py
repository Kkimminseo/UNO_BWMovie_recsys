from django.shortcuts import render


def serve_react(request):
    return render(request, "index.html")  # React의 index.html 렌더링
