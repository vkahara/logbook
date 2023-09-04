from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Event, LogEntry, Logbook, MirrorLogbook
from .forms import EventForm, LogbookPostForm

def login_view(request):
    """Käsittelee käyttäjän kirjautumisen.

    Käyttäjä täyttää lomakkeen tiedot ja lähettää ne. Jos tiedot ovat kelvolliset,
    käyttäjä kirjataan sisään. Jos tiedot eivät ole kelvolliset, näytetään virheviesti.

    Args:
        request: Pyynnön olio.

    Returns:
        Palauttaa käyttäjän etusivulle jos kirjautuminen onnistui, 
        muutoin palautetaan takaisin kirjautumissivulle.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return render(request, "lokikirja_app/login.html", {"form": form})
        else:
            return render(request, "lokikirja_app/login.html", {"form": form})
    else:
        form = AuthenticationForm()
        return render(request, "lokikirja_app/login.html", {"form": form})

def register(request):
    """Käsittelee käyttäjän rekisteröitymisen.

    Käyttäjä täyttää lomakkeen tiedot ja lähettää ne. Jos tiedot ovat kelvolliset, 
    luodaan uusi käyttäjä ja kirjataan käyttäjä sisään. Jos tiedot eivät ole kelvolliset, 
    näytetään virheviesti.

    Args:
        request: Pyynnön olio.

    Returns:
        Ohjaa käyttäjän etusivulle jos rekisteröityminen onnistui, 
        muutoin palautetaan takaisin rekisteröitymissivulle.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            MirrorLogbook.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Virhe kirjautumisessa, tarkasta salasanavaatimukset.')
    else:
        form = UserCreationForm()
    return render(request, 'lokikirja_app/register.html', {'form': form})


@login_required
def index(request):
    """Näyttää kaikki tapahtumat.

    Args:
        request: Pyynnön olio.

    Returns:
        Renderöi index-sivun, jossa näytetään kaikki tapahtumat.
    """
    events = Event.objects.all()
    return render(request, "lokikirja_app/index.html", {"events": events})


@login_required
def create_event(request):
    """Luo uuden tapahtuman.

    Args:
        request: Pyynnön olio.

    Returns:
        Palauttaa käyttäjän etusivulle jos tapahtuman luominen onnistui, 
        muutoin palautetaan takaisin tapahtuman luomissivulle.
    """
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lokikirja_app:index")
    else:
        form = EventForm()

    return render(request, "lokikirja_app/create_event.html", {"form": form})


@login_required
def logbook_detail(request, event_id):
    """Näyttää tietyn lokikirjan tiedot.

    Args:
        request: Pyynnön olio.
        event_id: Tapahtuman id.

    Returns:
        Renderöi logbook_detail-sivun, jossa näytetään tietyn lokikirjan tiedot.
    """
    # Hae tapahtuma tai palauta 404-virhe, jos sitä ei ole olemassa
    event = get_object_or_404(Event, id=event_id)

    user = request.user
    logbook = Logbook.objects.filter(event=event, user=user).first()

    # Jos käyttäjä avaa eventin ensimmäistä kertaa luodaan uusi lokikirja
    if not logbook:
        logbook = Logbook.objects.create(event=event, user=user)

    form = LogbookPostForm()
    if request.method == "POST":
        form = LogbookPostForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            LogEntry.objects.create(logbook=logbook, user=user, message=message)
            return redirect("lokikirja_app:logbook_detail", event_id=event_id)

    logbooks = Logbook.objects.filter(event=event)
    mirror_logbook = MirrorLogbook.objects.get(user=user)
    mirrored_logbooks = mirror_logbook.mirrored_logbooks.filter(event=event)
    # Hae ja järjestä kaikki logbookin merkinnät luontiajan mukaan
    logbook_entries = logbook.log_entries.all().order_by('created_at')

    for mirrored_logbook in mirrored_logbooks:
        if mirrored_logbook.event == event:
            logbook_entries = logbook_entries | mirrored_logbook.log_entries.all().order_by('created_at')

    return render(
        request,
        "lokikirja_app/logbook_detail.html",
        {
            "logbook_entries": logbook_entries,
            "form": form,
            "event": event,
            "logbooks": logbooks,
        },
    )


@login_required
def toggle_mirror(request, logbook_id):
    """Asettaa tai poistaa peilauksen valitusta lokikirjasta.

    Args:
        request: Pyynnön olio.
        logbook_id: Lokikirjan id.

    Returns:
        Uudelleenohjaus takaisin logbook_detail-näkymään.
    """
    logbook = get_object_or_404(Logbook, id=logbook_id)
    mirror_logbook, _ = MirrorLogbook.objects.get_or_create(user=request.user)
    if logbook in mirror_logbook.mirrored_logbooks.all():
        mirror_logbook.mirrored_logbooks.remove(logbook)
    else:
        mirror_logbook.mirrored_logbooks.add(logbook)
    return redirect("lokikirja_app:logbook_detail", event_id=logbook.event.id)
