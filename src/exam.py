"""Задание 3. Экзамен: разговор с человеком и итог.

Запуск из корня репозитория:  python3 src/exam.py

Функция main в конце файла уже соединяет части экзамена: загружает вопросы,
спрашивает имя, задаёт вопросы по лесенке, подводит итог и записывает результат.
Тела остальных функций этого файла пока простейшие — их пишет тот, кто взял
Задание 3. Как должен выглядеть экран — materials/screen_rus.md.

Этот файл — точка входа: печатает только он.
"""

import sys
from statistics import correlation

import answers
import bank
import ladder

TEAM = "datasets/team.csv"
BANK = "datasets/bank.csv"
RESULTS = "results.csv"
MAX_QUESTIONS = 10


def load_questions():
    """Все вопросы экзамена одним списком: сначала из TEAM, потом из BANK.

    Если файла нет, ошибку FileNotFoundError здесь не перехватывай:
    её перехватывает main.

    Пока тело простейшее: только выданные вопросы.
    """
    main_questions, _ = bank.load_bank(BANK)
    team_questions, _ = bank.load_bank(TEAM)
    return team_questions + main_questions


def read_line():
    """Прочитать одну строку, которую ввёл человек.

    Возвращает строку без перевода строки в конце. Если ввод закончился
    (Ctrl+D), возвращает None.

    Пока тело простейшее: конец ввода не отличается от пустой строки.
    """
    line = sys.stdin.readline()
    if line == "":
        return None
    return  line.rstrip("\n")

    # return sys.stdin.readline().rstrip("\n")


def show_question(number, question):
    """Показать вопрос с номером number, как в materials/screen_rus.md.

    Пока тело простейшее: только текст и варианты.
    """
    print("Вопрос %d из %d" % (number, MAX_QUESTIONS))
    for line in bank.question_lines(question):
        print(line)
    if question["type"] == "один":
        print("Введи номер варианта.")
    elif question["type"] == "несколько":
        print("Введи номера всех верных вариантов через запятую.")
    elif question["type"] == "короткий":
        print("Напиши ответ.")
    elif question["type"] == "нет ответа":
        print("Нет ответа.")
    # for line in bank.question_lines(question):
    #     print(line)


def show_result(result):
    """Показать результат ответа: «Верно.», «Неверно.» или «Нет ответа.».

    Пока тело простейшее: результат как есть.
    """
    if result == "верно":
        print("Верно.")
    elif result == "неверно":
        print("Неверно.")
    elif result == "нет ответа":
        print("Нет ответа.")


def final_level(history):
    """Итоговый уровень по правилу последнего правильного ответа.

    history — список пар (уровень вопроса, результат) в порядке экзамена,
    например [(1, "верно"), (2, "неверно"), (1, "верно")].

    Возвращает уровень последнего вопроса с результатом "верно"
    или None, если верных ответов не было.

    Пока тело простейшее: всегда None.
    """
    last_correct_level = None
    for level, result in history:
        if result == "верно":
            last_correct_level = level
    return last_correct_level


def final_lines(level, history):
    """Строки итога: «Итог: …» и «Почему: …», как в materials/screen_rus.md.

    level — итоговый уровень или None.

    Пока тело простейшее: только первая строка.
    """
    if level is None:
        return["Итог: не определён.","Почему: ни одного правильного ответа."]
    else:
        return ["Итог: уровень %d." % level,
                "Почему: последний правильный ответ — на уровне %d." % level]


def stable_level(history):
    """Задание 6 (дополнительное). Самый высокий уровень, где у человека
    хотя бы два верных ответа, или None.
    """
    #counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    #for level, result in history:
    #    if result == 'верно':
    #        counts[level] += 1
    #result_level = 0
    #for level in counts:
    #    if counts[level] >= 2 and level > result_level:
    #        resilt_level = level
    #if result_level != 0:
    #    return result_level
    #return None
    correct_count = {}
    for level, result in history:
        if result == "верно":
            correct_count[level] = correct_count.get(level,0) + 1
    max_level = None
    for level, count in correct_count.items():
        if count >= 2 and (max_level is None or level > max_level):
            max_level = level
    return max_level

def stable_lines(level, history):
    """Задание 6 (дополнительное). Строки итога для устойчивого правила."""
    if level is None:
        return ["Итог: не определён.","Почему: ни на одном уровне нет двух верных ответов."]
    level_count = {}
    for level_hist, _ in history:
        if level_hist in level_count:
            level_count[level_hist] += 1
        else:
            level_count[level_hist] = 1

    correct_count = 0
    for level_hist, result in history:
        if level_hist == level and result == "верно":
            correct_count+=1

    lines = ["Итог: уровень %d." % level]
    total_on_level = level_count[level]
    why_line = "Почему: уровень %d — самый высокий, где у тебя %d верных ответа (%d из %d)." % (
    level, correct_count, correct_count, total_on_level)

    next_level = level + 1
    if next_level in level_count:
        total_on_next = level_count[next_level]
        correct_on_next = 0
        for level_hist, result in history:
            if level_hist == next_level and result == "верно":
                correct_on_next += 1
        if correct_on_next == 0:
            why_line += " На уровне %d верных ответов нет (0 из %d)." % (next_level, total_on_next)
        elif correct_on_next > 0:
            why_line += (" На уровне %d только %d верным ответ (%d из %d) — этого мало.") % (
                    next_level, correct_on_next, correct_on_next, total_on_next)

    lines.append(why_line)
    return lines
    #counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    #for l, result in history:
    #    if result == 'Верно':
    #        counts[l] += 1
    #ncounts = {1: 0,
    # 2: 0, 3: 0, 4: 0, 5: 0}
    #for l, result in history:
    #    if result == 'Неверно' or 'Нет ответа':
    #        ncounts[l] += 1
    #return [f"Итог: уровень {level}.\nПочему: уровень {level} - самый высокий, где у тебя {counts[level]} верных ответа #({counts[level]} из {counts[level] + ncounts[level]}). На уровне {level + 1}"]


def save_result(name, level, asked, correct):
    """Дописать строку «имя;уровень;задано;верно» в конец файла RESULTS.

    level — число или None; при None в поле уровня пишется «не определён».

    Пока тело простейшее: ничего не записывается.
    """
    if level is None:
        levelstr = "не определён"
    else:
        levelstr = str(level)
    with open(RESULTS,"a", encoding="utf-8") as file:
        file.write("%s;%s;%d;%d\n" % (name, levelstr, asked, correct))
    return None


def main():
    try:
        questions = load_questions()
    except FileNotFoundError as error:
        print("Файл не найден: %s" % error.filename)
        return 1

    print("Как тебя зовут?")
    name = read_line()
    if name is None:
        print("Экзамен не начат.")
        return 0
    name = name.replace(";", " ").strip() or "без имени"

    stable = "--stable" in sys.argv
    own = '--own' in sys.argv
    level = ladder.START_LEVEL
    asked = []
    history = []
    while len(asked) < MAX_QUESTIONS:
        question = ladder.pick_question(questions, level, asked)
        if question is None:
            break
        asked.append(question["id"])
        print()
        show_question(len(asked), question)
        raw = read_line()
        result = answers.check_answer(question, raw if raw is not None else "")
        show_result(result)
        history.append((question["level"], result))
        if own:
            level = ladder.next_level_own(question['level'], result)
        else:
            level = ladder.next_level(question["level"], result)
        if raw is None:
            break

    if stable:
        result_level = stable_level(history)
        lines = stable_lines(result_level, history)
    else:
        result_level = final_level(history)
        lines = final_lines(result_level, history)
    print()
    for line in lines:
        print(line)
    correct = 0
    for _, result in history:
        if result == "верно":
            correct += 1
    save_result(name, result_level, len(asked), correct)
    return 0


if __name__ == "__main__":
    sys.exit(main())
