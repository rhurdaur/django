""" 
App-spezische Validierungsfunktionen


Aufgabe: einen weiteren Validator für das name-Feld von Event. 
Das Feld muss mindestens einen Buchstaben [a-zA-Z] beinhalten
"""

import re
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError


def bad_word_filter(wordlist: list[str], field_value: str) -> None:
    """Prüft, ob ein nicht-erlaubtes Wort in field_value vorkommt.

    Args:
        wordlist (list[str]): Liste mit verbotenen Wörtern
        field_value (str): Feld Text

    Raises:
        ValidationError
    """
    for word in wordlist:
        if word in field_value:
            raise ValidationError(f"Das Wort {word} ist nicht erlaubt!")


def datetime_in_future(date_value) -> None:
    """Prüfen, ob ein Datum mindestens 1 Stunde in der Zukunft liegt."""
    if date_value < timezone.now() + timedelta(hours=1):
        raise ValidationError("Der Zeitpunkt muss in der Zukunft liegen (+1h)")


def validate_name(value):
    if not re.search(r"[a-zA-Z]+", value):
        raise ValidationError("Der Name muss auch Buchstaben beinhalten")
