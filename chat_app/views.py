from django.shortcuts import render
from django.conf import settings
import google.generativeai as genai
import json
from .models import Ordinateur

# Create your views here.
def get_gemini_response(user_message):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash') #gemini-2.0 is free with limited token access
    response = model.generate_content(user_message)
    return response.text if response.text else ""

def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if user_message:
            gemini_response = get_gemini_response(user_message)
            print(gemini_response)
            # Ici, nous devrons traiter la réponse de Gemini pour rechercher les ordinateurs
            # Pour l'instant, renvoyons simplement la réponse de Gemini
            return JsonResponse({'bot_response': gemini_response})
        return JsonResponse({'error': 'No message received'}, status=400)
    return render(request, 'chat_app/chat.html')