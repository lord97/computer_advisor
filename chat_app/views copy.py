from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
import google.generativeai as genai
import json
from .models import Ordinateur

def get_gemini_response(user_message):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = f"""Tu es un assistant expert en recommandation d'ordinateurs. Analyse la demande de l'utilisateur et extrais les critères techniques pertinents.

    Règles importantes:
    1. Pour les composants (processeur, carte graphique,ram), retourne UN SEUL MODÈLE précis quand c'est mentionné
    2. Si l'utilisateur donne des alternatives (ex: "RTX ou RX"), retourne les deux séparément
    3. Si aucune marque n'est spécifiée, ne retourne pas de critère de marque

    Format de réponse JSON:
    {{
        "description": "Description du besoin",
        "budget_max": nombre ou null,
        "budget_min": nombre ou null,
        "critères": {{
            "processeur": ["modèle1", "modèle2"] ou null,
            "carte_graphique": ["modèle1", "modèle2"] ou null,
            "ram_min": nombre ou null,
            "stockage": ["type1", "type2"] ou null,
            "utilisations": ["mot-clé1", "mot-clé2"] ou null
        }}
    }}

    Exemple 1:
    Input: "Je veux un PC avec RTX 3080 ou RX 6800"
    Output: {{
        "description": "PC gaming haut de gamme",
        "budget_max": null,
        "budget_min": null,
        "critères": {{
            "carte_graphique": ["RTX 3080", "RX 6800"],
            "processeur": null,
            "ram_min": 16,
            "stockage": ["SSD"],
            "utilisations": ["gaming"]
        }}
    }}

    Input: "{user_message}"
    Réponse:"""

    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Erreur Gemini: {e}")
        return {
            "description": "Besoin non spécifié",
            "budget_max": None,
            "budget_min": None,
            "critères": {}
        }

def apply_filters(queryset, criteres):
    # Filtre processeur
    if criteres.get('processeur'):
        q_processeur = Q()
        for proc in criteres['processeur']:
            q_processeur |= Q(processeur__icontains=proc)
        queryset = queryset.filter(q_processeur)

    # Filtre carte graphique
    if criteres.get('carte_graphique'):
        q_gpu = Q()
        for gpu in criteres['carte_graphique']:
            q_gpu |= Q(carte_graphique__icontains=gpu)
        queryset = queryset.filter(q_gpu)

    # Filtre RAM
    if criteres.get('ram_min'):
        queryset = queryset.filter(memoire_ram__gte=criteres['ram_min'])

    # Filtre stockage
    if criteres.get('stockage'):
        q_stockage = Q()
        for stock in criteres['stockage']:
            q_stockage |= Q(stockage__icontains=stock)
        queryset = queryset.filter(q_stockage)

    # Filtre utilisations
    if criteres.get('utilisations'):
        q_util = Q()
        for util in criteres['utilisations']:
            q_util |= Q(utilisations_recommandees__icontains=util)
        queryset = queryset.filter(q_util)

    return queryset

def chat_view(request):
    if request.method == 'POST':
        try:
            analyse = get_gemini_response(request.POST.get('message', ''))
            queryset = Ordinateur.objects.all()

            # Filtrage budget
            if analyse['budget_max']:
                queryset = queryset.filter(prix__lte=analyse['budget_max'])
            if analyse['budget_min']:
                queryset = queryset.filter(prix__gte=analyse['budget_min'])

            # Filtrage technique
            queryset = apply_filters(queryset, analyse['critères'])

            # Résultats
            ordinateurs = list(queryset.order_by('prix')[:10].values(...))
            
            return JsonResponse({
                'description': analyse['description'],
                'results': ordinateurs
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)