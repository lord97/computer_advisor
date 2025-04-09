from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
import google.generativeai as genai
import json
from .models import Ordinateur

def get_gemini_response_reco(user_message, computers_str):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = f"""
        You are a computer recommendation assistant. Based on the user's message and the list of available computers, select the most relevant computers and return ONLY their IDs.

        User request:
        \"\"\"{user_message}\"\"\"

        Available computers (id - specs):
        \"\"\"{computers_str}\"\"\"

        If the user's message is not related to computer recommendations, respond with a JSON object like this:
        {{
            "description": "This question is not related to computer recommendations.",
            "recommended_ids": []
        }}

        Return format (JSON):
        {{
        "description": "Short description of the user need",
        "recommended_ids": [list of integers]
        }}
        
        Example: 
        Respond with a JSON object like this:
        {{
            "description": "Short summary of the user's need",
            "recommended_ids": [1, 5, 12]
        }}
        """

    try:
        response = model.generate_content(prompt)
        cleaned = response.text.replace("```json", "").replace("```", "").strip()
        print(cleaned)
        return json.loads(cleaned)
    except Exception as e:
        print(f"Error with Gemini: {e}")
        return {
            "description": "Recommendation failed",
            "recommended_ids": []
        }


# Vue principale
def chat_view(request):
    if request.method == 'POST':
        try:
            user_message = request.POST.get('message', '').strip()
            if not user_message:
                return JsonResponse({'error': 'Please enter a message'}, status=400)
            
            # Sélectionner 30 ordinateurs aléatoires
            queryset = Ordinateur.objects.all().order_by('?')[:30]
            computers_list = ""

            # Format the selected computers into a string to send to Gemini
            for comp in queryset:
                computers_list += f"{comp.id} - CPU: {comp.processeur}, GPU: {comp.carte_graphique}, RAM: {comp.memoire_ram}GB, Storage: {comp.stockage}, Price: {comp.prix} RMB, Use: {comp.utilisations_recommandees}\n"

            # Get the response from Gemini
            analyse = get_gemini_response_reco(user_message, computers_list)

            # Check if Gemini's response indicates the question is not about computers
            if analyse['recommended_ids'] == []:
                return JsonResponse({
                    'description': analyse.get('description', 'Results'),
                    'results': []
                })

            # Retrieve the recommended computers based on the IDs returned by Gemini
            ordinateurs = list(
                Ordinateur.objects.filter(id__in=analyse['recommended_ids']).values(
                    'id', 'nom_modele', 'description', 'prix', 'processeur',
                    'memoire_ram', 'stockage', 'carte_graphique',
                    'utilisations_recommandees', 'image'
                )
            )

            
            
            
            return JsonResponse({
                'description': analyse.get('description', 'Results'),
                'ordinateurs': ordinateurs
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # GET request fallback
    return render(request, 'chat_app/chat.html')
