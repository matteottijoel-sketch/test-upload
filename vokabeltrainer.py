import random
from collections import deque

def load_vocabulary(dateiname):
    vokabeln = {}
    with open(dateiname, "r", encoding="utf-8") as datei:
        for zeile in datei:
            zeile = zeile.strip()
            if not zeile:
                continue
            englisch, italienisch = zeile.split(";")
            vokabeln[englisch.strip()] = italienisch.strip()
    return vokabeln

def quiz_vokabeln(vokabeln, fragen=15):
    punkte = 0
    fragen_gestellt = 0
    queue = deque(random.sample(list(vokabeln.items()), len(vokabeln)))
    falsch = []

    while fragen_gestellt < fragen and queue:
        englisch, italienisch = queue.popleft()
        antwort = input(f"Frage {fragen_gestellt + 1}: Wie heißt '{englisch}' auf Italienisch? ")
        if antwort.strip().lower() == italienisch.lower():
            print("Richtig!")
            punkte += 1
        else:
            print(f"Falsch! Die richtige Antwort ist: {italienisch}")
            falsch.append((englisch, italienisch))
        fragen_gestellt += 1
        print()

    if falsch:
        print("Repetitionsrunde!")
        for englisch, italienisch in falsch:
            antwort = input(f"Noch einmal: Wie heisst '{englisch}' auf Italienisch? ")
            if antwort.strip().lower() == italienisch.lower():
                print("Richtig!")
                punkte += 1
            else:
                print(f"Falsch. Die richtige Antwort ist {italienisch}")
            print()

    print(f"Du hast {punkte} von {fragen} Punkten erreicht.")


def main():
    print("Vokabeltrainer lädt...")

    vokabeln_verben = load_vocabulary("vokabeln_verben.txt")
    vokabeln_nomen = load_vocabulary("vokabeln_nomen.txt")
    vokabeln_adjektive = load_vocabulary("vokabeln_adjektive.txt")

    while True:
        print("Vokabeltrainer ist bereit!")
        print("1) Verben üben")
        print("2) Nomen üben")
        print("3) Adjektive üben")
        print("4) Beenden")

        auswahl = input("Wähle 1, 2, 3 oder 4: ")
        if auswahl == "4":
            print("Auf Wiedersehen!")
            break
        elif auswahl == "1":
            vokabeln = vokabeln_verben
        elif auswahl == "2":
            vokabeln = vokabeln_nomen
        elif auswahl == "3":
            vokabeln = vokabeln_adjektive
        else:
            print("Bitte wähle eine gültige Zahl von 1 bis 4.")
            continue

        quiz_vokabeln(vokabeln)


if __name__ == "__main__":
    main()
