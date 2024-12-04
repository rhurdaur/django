# Aufgabe

Es soll eine Klasse Ticket erstellt werden.
Ein eingeloggter User kann für beliebige Events Tickets erstellen.
das Ticketmodel hat ein Feld "nummer", dass ein alphanumerischer String
von der Länge 8 ist. Diese Nummer ist unique.


## Das Ticket-Model

    Ticket (DateMixin):
    - name
    - author (FK)
    - event (FK)
    - nummer (str), unique, alphanumerisch
    - message: str, optional


## Views und Formulare

Es soll eine ListView und eine CreateView erstellt werden.
Dafür ist ein Formular und ein einfaches Template notwendig (Update & Delete nicht nötig)



## FormularTests ausführen.
- Erfolgreiches Anlegen testen
- Testen, ob Tickets mit falscher Nummer nicht eingetragen werden können
- Testen, ob Tickets mit selber Nummer nicht eingetragen werden können
- Testen, ob nicht-authentifizierte User kein Ticket anlegen können.