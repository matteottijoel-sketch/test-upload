import os
import random
import tkinter as tk

# Der Ordner, in dem diese Datei liegt.
# Das verwenden wir, damit die Vokabeldateien immer korrekt gefunden werden.
script_dir = os.path.dirname(os.path.abspath(__file__))

# Hauptfenster der Tkinter-Anwendung.
root = tk.Tk()
root.title("Joel's Vokabeltrainer")
root.geometry("450x340")

label = tk.Label(root, text="Joel's Vokabeltrainer", font=("Arial", 18))
label.pack(pady=15)
status_label = tk.Label(root, text="Wähle eine Kategorie", font=("Arial", 12))
status_label.pack(pady=5)

current_questions = []
current_index = 0
score = 0
wrong_answers = []
current_category = ""
quiz_amount = 15
repetition_mode = False


# Lade die Vokabeln aus einer Textdatei.
# Jede Zeile hat das Format: Englisch;Italienisch
def load_vocabulary(dateiname):
    vokabeln = {}
    dateipfad = os.path.join(script_dir, dateiname)
    with open(dateipfad, "r", encoding="utf-8") as datei:
        for zeile in datei:
            zeile = zeile.strip()
            if not zeile:
                continue
            englisch, italienisch = zeile.split(";")
            vokabeln[englisch.strip()] = italienisch.strip()
    return vokabeln

vokabeln_verben = load_vocabulary("vokabeln_verben.txt")
vokabeln_nomen = load_vocabulary("vokabeln_nomen.txt")
vokabeln_adjektive = load_vocabulary("vokabeln_adjektive.txt")

menu_frame = tk.Frame(root)
quiz_frame = tk.Frame(root)

question_label = tk.Label(quiz_frame, text="", font=("Arial", 14), wraplength=420)
question_label.pack(pady=15)

answer_entry = tk.Entry(quiz_frame, font=("Arial", 12), width=30)
answer_entry.pack(pady=5)

# Prüfe die eingegebene Antwort und speichere falsche Antworten für später.
def check_answer(event=None):
    global score, wrong_answers
    antwort = answer_entry.get().strip().lower()
    englisch, italienisch = current_questions[current_index]
    correct = italienisch.lower()

    if antwort == correct:
        score += 1
        feedback_label.config(text="Richtig!", fg="green")
    else:
        wrong_answers.append((englisch, italienisch))
        feedback_label.config(text=f"Falsch! Die richtige Antwort ist: {italienisch}", fg="red")

    submit_button.config(text="Weiter", command=next_question)


def submit_or_continue(event=None):
    if submit_button["text"] == "Weiter":
        submit_button.invoke()
    else:
        check_answer()

root.bind("<Return>", submit_or_continue)

submit_button = tk.Button(quiz_frame, text="Antwort prüfen", command=check_answer)
submit_button.pack(pady=10)

feedback_label = tk.Label(quiz_frame, text="", font=("Arial", 11))
feedback_label.pack(pady=5)

progress_label = tk.Label(quiz_frame, text="", font=("Arial", 10))
progress_label.pack(pady=3)

score_label = tk.Label(quiz_frame, text="", font=("Arial", 10))
score_label.pack(pady=3)

back_button = tk.Button(quiz_frame, text="Zurück zum Menü", command=lambda: show_menu())
back_button.pack(pady=10)


def show_menu():
    quiz_frame.pack_forget()
    menu_frame.pack(pady=20)
    status_label.config(text="Wähle eine Kategorie")
    feedback_label.config(text="")
    progress_label.config(text="")
    score_label.config(text="")
    answer_entry.config(state="normal")
    answer_entry.delete(0, tk.END)
    submit_button.config(text="Antwort prüfen", command=check_answer)


# Starte das Quiz für die gewählte Kategorie.
# Hier werden die Fragen gemischt und die erste Frage vorbereitet.
def start_quiz(kategorie):
    global current_questions, current_index, score, wrong_answers, current_category
    current_category = kategorie
    if kategorie == "Verben":
        vokabeln = vokabeln_verben
    elif kategorie == "Nomen":
        vokabeln = vokabeln_nomen
    else:
        vokabeln = vokabeln_adjektive

    frage_liste = list(vokabeln.items())
    random.shuffle(frage_liste)
    current_questions = frage_liste[: min(quiz_amount, len(frage_liste))]
    current_index = 0
    score = 0
    wrong_answers = []

    menu_frame.pack_forget()
    quiz_frame.pack(pady=10)
    status_label.config(text=f"{kategorie} ausgewählt")
    show_question()


# Zeige die aktuelle Frage im Quiz an.
def show_question():
    if current_index < len(current_questions):
        englisch, _ = current_questions[current_index]
        question_label.config(text=f"Wie heißt '{englisch}' auf Italienisch?")
        progress_label.config(text=f"Frage {current_index + 1} von {len(current_questions)}")
        score_label.config(text=f"Punkte: {score}")
        feedback_label.config(text="")
        answer_entry.config(state="normal")
        answer_entry.delete(0, tk.END)
        answer_entry.focus()
        submit_button.config(text="Antwort prüfen", command=check_answer)

    else:
        finish_quiz()


# Gehe zur nächsten Frage.
def next_question():
    global current_index
    current_index += 1
    show_question()


# Beende das erste Quiz und starte ggf. die Wiederholungsrunde.
def finish_quiz():
    global repetition_mode, current_questions, current_index
    total = len(current_questions)
    if wrong_answers and not repetition_mode:
        question_label.config(text=f"Du hast {score} von {total} Punkten. Jetzt kommt die Wiederholungsrunde für {len(wrong_answers)} falsche Antworten.")
        progress_label.config(text="Repetitionsrunde")
        score_label.config(text=f"Punkte bisher: {score}")
        feedback_label.config(text="Drücke Weiter, um die Wiederholungsrunde zu starten.")
        submit_button.config(text="Weiter", command=start_repetition)
        answer_entry.config(state="disabled")

       

    else:
        result_text = f"Fertig! Du hast insgesamt {score} Punkte erzielt."
        if repetition_mode:
            result_text += "\nDie Wiederholungsrunde ist abgeschlossen."
        question_label.config(text=result_text)
        progress_label.config(text="")
        score_label.config(text="")
        feedback_label.config(text="Drücke 'Zurück zum Menü', um neu zu starten.")
        submit_button.config(text="Nochmal versuchen", command=lambda: start_quiz(current_category))
        answer_entry.config(state="disabled")


# Starte die Wiederholungsrunde mit den zuvor falschen Antworten.
def start_repetition():
    global current_questions, current_index, repetition_mode, wrong_answers
    repetition_mode = True
    current_questions = wrong_answers.copy()
    current_index = 0
    wrong_answers = []
    feedback_label.config(text="")
    score_label.config(text=f"Punkte bisher: {score}")
    show_question()


button_verben = tk.Button(menu_frame, text="Verben üben", width=20, command=lambda: start_quiz("Verben"))
button_nomen = tk.Button(menu_frame, text="Nomen üben", width=20, command=lambda: start_quiz("Nomen"))
button_adjektive = tk.Button(menu_frame, text="Adjektive üben", width=20, command=lambda: start_quiz("Adjektive"))
button_beenden = tk.Button(menu_frame, text="Beenden", command=root.quit)


button_verben.pack(pady=5)
button_nomen.pack(pady=5)
button_adjektive.pack(pady=5)
button_beenden.pack(pady=5)

menu_frame.pack(pady=20)
root.mainloop()

