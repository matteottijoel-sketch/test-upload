#Dieses Quiz zeigt Fragen mit 4 Optionen und prüft die Auswahl
def ask_question(question, options, correct):
    #Frage und Optionen anzeigen
    print("\n" + question)
    for option in options:
        print(option)
    
    user_answer = input("Deine Antwort (a/b/c/d): ").lower().strip()
    if user_answer == correct.lower():
        print("Richtig!")
        return True
    else:
        print(f"Falsch! Die richtige Antwort ist: {correct}.")
        return False
    
#Liste der Fragen, Optionen und Antworten
questions = [
    (
        "Wie heisst die Hauptstadt von den USA?",
        ["a) New York", "b) Washington D.C.", "c) Los Angeles", "d) Chicago"],
        "b"
    ),
    (
        "Was ist die chemische Formel von Wasser?",
        ["a) H2O", "b) CO2", "c) O2", "d) NaCl"],
        "a"
    ),
    (
        "Wer hat die Relativitätstheorie entwickelt?",
        ["a) Isaac Newton", "b) Albert Einstein", "c) Galileo Galilei", "d) Nikola Tesla"],
        "b"
    ),
    (
        "Wer entdeckte das Gesetz der Schwerkraft?",
        ["a) Isaac Newton", "b) Albert Einstein", "c) Marie Curie", "d) Thomas Edison"],
        "a"
    ),
    (
        "Welche Automarke baute das erste Auto?",
        ["a) BMW", "b) Mercedes-Benz", "c) Ford", "d) Volkswagen"],
        "b"
    ),
]

#Diese Funktion liest den gespeicherten Highscore aus der Datei
def read_highscore():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

#Diese Funktion speichert den neuen Highscore in der Datei
def write_highscore(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))


#Diese Funktion führt das Quiz aus und zählt die Punkte
def run_quiz():
    score = 0
    for question, options, correct in questions:
        if ask_question(question, options, correct):
            score += 1
    print(f"\nDu hast {score} von {len(questions)} Fragen richtig beantwortet.")
    highscore = read_highscore()
    if score > highscore:
        print("Neuer Highscore!")
        write_highscore(score)
    else:
        print(f"Der Highscore ist {highscore}.")

#Diese Funktion startet das Quiz und wiederholt es
def main():
    while True:
        run_quiz()
        again = input("\nMöchtest du das Quiz nochmal spielen? (Ja/Nein): ").lower().strip()
        if again != "ja":#beendet das Quiz, wenn der Benutzer nicht "ja" eingibt
            print("Danke fürs Spielen! Auf Wiedersehen!")
            break


if __name__ == "__main__":
    main()

    