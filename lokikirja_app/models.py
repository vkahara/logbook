from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    # Tapahtuman nimi, joka on enintään 100 merkkiä pitkä
    name = models.CharField(max_length=100)
    # Tapahtuman luontipäivämäärä ja -aika, tallentuu automaattisesti kun tapahtuma luodaan
    created_at = models.DateTimeField(auto_now_add=True)
    
class Logbook(models.Model):
    # Viittaus tapahtumaan, johon tämä lokikirja kuuluu
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # Viittaus käyttäjään, joka loi tämän lokikirjan
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Lokikirjan luontipäivämäärä ja -aika, tallentuu automaattisesti kun lokikirja luodaan
    created_at = models.DateTimeField(auto_now_add=True)
    # Peilataanko lokikirja?
    mirror = models.BooleanField(default=False)

class LogEntry(models.Model):
    # Viittaus lokikirjaan, johon lokimerkintä kuuluu
    logbook = models.ForeignKey(Logbook, on_delete=models.CASCADE, related_name='log_entries')
    # Lokimerkinnän viesti, asetettu viestin enimmäispituudeksi 10 000 merkkiä väärinkäyttöjen välttämiseksi.
    message = models.TextField(max_length=10000)
    # Viittaus käyttäjään, joka loi tämän lokimerkinnän
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='log_entries')
    # Lokimerkinnän luontipäivämäärä ja luontiaika, tallentuu automaattisesti kun lokimerkintä luodaan
    created_at = models.DateTimeField(auto_now_add=True)

class MirrorLogbook(models.Model):
    # Viittaus käyttäjään, joka omistaa tämän peililokikirjan
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # mitkä lokikirjat peilataan
    mirrored_logbooks = models.ManyToManyField(Logbook)
