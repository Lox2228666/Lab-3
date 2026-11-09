"""Лабораторная работа №3. Вариант 10. Генератор условных ключей."""

import random
import string
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


BASE_DIR = Path(__file__).resolve().parent
YELLOW = "#F7EF00"
DARK = "#101115"
PANEL = "#1C1F25"
WHITE = "#F1F1F1"


def make_key(number):
    """Создать ключ из шестизначного числа по правилам варианта 10."""
    if len(number) != 6 or any(char not in string.digits for char in number):
        raise ValueError("Введите ровно шесть цифр (0–9).")

    # Цифры 4–6 идут в первый блок, 1–3 — во второй.
    # Внутри каждого блока цифры перемешиваются случайным образом.
    digits_first = "".join(random.sample(number[3:6], 3))
    digits_second = "".join(random.sample(number[:3], 3))

    letters_first = "".join(random.choices(string.ascii_uppercase, k=2))
    letters_second = "".join(random.choices(string.ascii_uppercase, k=2))

    first = digits_first + letters_first
    second = digits_second + letters_second
    total = int(digits_first) + int(digits_second)
    return f"{first}-{second} {total:04d}"


def generate():
    try:
        result_var.set(make_key(input_field.get().strip()))
    except ValueError as error:
        messagebox.showwarning("Неверный ввод", str(error))
        return
    status_var.set("КЛЮЧ СГЕНЕРИРОВАН")


def copy_key():
    key = result_var.get()
    if not key:
        messagebox.showinfo("Информация", "Сначала сгенерируйте ключ.")
        return
    window.clipboard_clear()
    window.clipboard_append(key)
    status_var.set("КЛЮЧ СКОПИРОВАН")


window = tk.Tk()
window.title("Cyberpunk 2077 — Key Generator | Lab 3")
window.geometry("800x710")
window.resizable(False, False)
window.configure(bg=DARK)

# Изображение является фоном всего окна, а не отдельным баннером.
background_path = BASE_DIR / "cyberpunk_background.png"
try:
    background_img = tk.PhotoImage(file=str(background_path))
except (tk.TclError, OSError) as error:
    messagebox.showerror("Нет изображения", f"Не удалось открыть {background_path.name}:\n{error}")
    window.destroy()
    raise SystemExit(1)

canvas = tk.Canvas(window, width=800, height=710, borderwidth=0,
                   highlightthickness=0, bg=DARK)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_img, anchor="nw")
canvas.create_rectangle(0, 0, 800, 7, fill=YELLOW, outline=YELLOW)

canvas.create_text(400, 267, text="KEY GENERATOR",
                   font=("Consolas", 17, "bold"), fill=YELLOW)
canvas.create_text(400, 338, text="ACCESS TERMINAL",
                   font=("Consolas", 23, "bold"), fill=YELLOW)
canvas.create_text(400, 392, text="Введите шестизначное десятичное число",
                   font=("Segoe UI", 11), fill=WHITE)

input_field = tk.Entry(window, font=("Consolas", 18), justify="center",
                       bg=PANEL, fg=WHITE, insertbackground=YELLOW,
                       relief="flat", borderwidth=0)
canvas.create_window(400, 431, window=input_field, width=240, height=46)
input_field.focus_set()

generate_btn = tk.Button(window, text="СГЕНЕРИРОВАТЬ КЛЮЧ",
                         command=generate, bg=YELLOW, fg=DARK,
                         activebackground="#DDD700", activeforeground=DARK,
                         font=("Consolas", 13, "bold"),
                         relief="flat", borderwidth=0, cursor="hand2")
canvas.create_window(400, 504, window=generate_btn, width=265, height=54)

canvas.create_rectangle(65, 548, 735, 617, fill=PANEL, outline="")
result_var = tk.StringVar()
result_label = tk.Label(window, textvariable=result_var,
                        font=("Consolas", 23, "bold"),
                        fg=YELLOW, bg=PANEL)
canvas.create_window(400, 583, window=result_label, width=650, height=55)

copy_btn = tk.Button(window, text="Копировать ключ", command=copy_key,
                     bg=DARK, fg=WHITE, activebackground=PANEL,
                     activeforeground=YELLOW, relief="flat", borderwidth=0,
                     font=("Segoe UI", 10), cursor="hand2")
canvas.create_window(400, 645, window=copy_btn, width=165, height=28)

status_var = tk.StringVar(value="ОЖИДАНИЕ ВВОДА")
status_label = tk.Label(window, textvariable=status_var,
                        font=("Consolas", 9), bg=DARK, fg=YELLOW)
canvas.create_window(400, 681, window=status_label, width=200, height=25)

window.bind("<Return>", lambda event: generate())
window.mainloop()
