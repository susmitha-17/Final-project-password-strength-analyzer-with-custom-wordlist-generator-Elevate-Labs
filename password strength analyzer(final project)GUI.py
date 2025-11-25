# ---------------- PASSWORD STRENGTH ANALYZER + WORDLIST TEST FEATURE ----------------

import tkinter as tk
from tkinter import messagebox, scrolledtext
from zxcvbn import zxcvbn

# ---------- Password Strength Function ----------
def analyze_password():
    password = entry_password.get()

    if not password.strip():
        messagebox.showwarning("Input Missing", "Please enter a password!")
        return

    result = zxcvbn(password)

    score_text = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Strong",
        4: "Very Strong"
    }

    output = f"""
Password Entered: {password}
Strength Score: {result['score']} → {score_text[result['score']]}

Crack Time (online attack): {result['crack_times_display']['online_no_throttling_10_per_second']}
Crack Time (offline attack): {result['crack_times_display']['offline_fast_hashing_1e10_per_second']}
Guesses Required: {result['guesses']}
"""

    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, output)

# ---------- Wordlist Generator ----------
def generate_wordlist():
    name = entry_name.get().lower()
    pet = entry_pet.get().lower()
    year = entry_year.get().lower()

    base_words = []
    if name: base_words.append(name)
    if pet: base_words.append(pet)
    if year: base_words.append(year)

    if not base_words:
        messagebox.showwarning("Input Missing", "Enter at least Name, Pet, or Year!")
        return

    numbers = ["1", "12", "123", "1234", "2023", "2024", "2025"]
    symbols = ["!", "@", "#"]

    wordlist = []

    for word in base_words:
        wordlist.append(word)
        for n in numbers:
            wordlist.append(word + n)
        for s in symbols:
            wordlist.append(word + s)
        for s in symbols:
            for n in numbers:
                wordlist.append(word + s + n)

    text_wordlist.delete(1.0, tk.END)
    text_wordlist.insert(tk.END, "\n".join(wordlist[:200]))
    messagebox.showinfo("Wordlist Created", f"Generated {len(wordlist)} words!")

# ---------- TEST PASSWORD AGAINST GENERATED WORDLIST ----------
def check_password_in_wordlist():
    password = entry_password.get().strip()
    wordlist_text = text_wordlist.get(1.0, tk.END).splitlines()

    if not password:
        messagebox.showwarning("Input Missing", "Enter a password to test!")
        return

    if len(wordlist_text) == 0:
        messagebox.showwarning("Wordlist Missing", "Generate a wordlist first!")
        return

    if password in wordlist_text:
        messagebox.showerror(
            "Weak Password",
            "⚠️ Password FOUND in the generated wordlist!\nIt is easily guessable."
        )
    else:
        messagebox.showinfo(
            "Safe Password",
            "✔️ Password NOT found in the generated wordlist.\nIt is safer than common guesses."
        )

# ---------- GUI Layout ----------
root = tk.Tk()
root.title("Password Strength Analyzer & Wordlist Generator")
root.geometry("650x720")
root.config(bg="#f2f2f2")

# ---------- Password Section ----------
tk.Label(root, text="Enter Password:", font=("Arial", 12, "bold"), bg="#f2f2f2").pack()

entry_password = tk.Entry(root, width=40, show="*", font=("Arial", 12))
entry_password.pack(pady=5)

tk.Button(root, text="Analyze Password", font=("Arial", 12), command=analyze_password).pack(pady=10)

text_output = scrolledtext.ScrolledText(root, width=70, height=10, font=("Arial", 10))
text_output.pack(pady=10)

# ---------- Wordlist Section ----------
tk.Label(root, text="Wordlist Generator", font=("Arial", 14, "bold"), bg="#f2f2f2").pack(pady=10)

frame_inputs = tk.Frame(root, bg="#f2f2f2")
frame_inputs.pack()

tk.Label(frame_inputs, text="Name:", font=("Arial", 11), bg="#f2f2f2").grid(row=0, column=0)
entry_name = tk.Entry(frame_inputs, width=25)
entry_name.grid(row=0, column=1)

tk.Label(frame_inputs, text="Pet:", font=("Arial", 11), bg="#f2f2f2").grid(row=1, column=0)
entry_pet = tk.Entry(frame_inputs, width=25)
entry_pet.grid(row=1, column=1)

tk.Label(frame_inputs, text="Year:", font=("Arial", 11), bg="#f2f2f2").grid(row=2, column=0)
entry_year = tk.Entry(frame_inputs, width=25)
entry_year.grid(row=2, column=1)

tk.Button(root, text="Generate Wordlist", font=("Arial", 12), command=generate_wordlist).pack(pady=10)

text_wordlist = scrolledtext.ScrolledText(root, width=70, height=10, font=("Arial", 10))
text_wordlist.pack(pady=10)

# ---------- NEW BUTTON TO TEST PASSWORD ----------
tk.Button(
    root,
    text="Check Password Against Wordlist",
    font=("Arial", 12, "bold"),
    bg="#d9d9d9",
    command=check_password_in_wordlist
).pack(pady=8)

root.mainloop()