from django.db import models

class Ordinateur(models.Model):
    nom_modele = models.CharField(max_length=255)
    description = models.TextField()
    prix =  models.IntegerField() #prix en rmb
    processeur = models.CharField(max_length=255)
    memoire_ram = models.IntegerField()
    stockage = models.CharField(max_length=255)
    carte_graphique = models.CharField(max_length=100, blank=True, null=True)  # Peut être vide
    utilisations_recommandees = models.CharField(max_length=255)  # Liste de mots-clés séparés par des virgules par exemple
    image = models.ImageField(upload_to='ordinateurs/', blank=True, null=True)
    
    def __str__(self):
        return self.nom_modele