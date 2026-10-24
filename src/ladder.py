"""Задание 2. Выбор следующего вопроса — «лесенка».

Этот модуль ничего не печатает. Названия функций и то, что они принимают,
менять нельзя: их вызывают exam.py и тесты. Меняй тела функций.
Как устроена лесенка и где она ломается — materials/ladder_rus.md.
"""

START_LEVEL = 1


def next_level(level, result):
    """Уровень следующего вопроса.

    level — уровень, на котором был вопрос; result — "верно", "неверно"
    или "нет ответа".

    После "верно" — на единицу выше, после "неверно" — на единицу ниже,
    но не ниже 1 и не выше 5. После "нет ответа" уровень не меняется.

    Пока тело не написано, уровень не меняется никогда.
    """
    if result == 'верно':
        return min(level + 1, 5)
    if result == 'неверно':
        return max(level - 1, 1)
    return level


def pick_question(questions, level, asked):
    """Следующий вопрос.

    questions — список вопросов (сначала вопросы команды, потом выданные);
    level — нужный уровень; asked — список id уже заданных вопросов.

    Возвращает первый по порядку в списке вопрос нужного уровня, которого
    нет в asked. Если на этом уровне вопросов не осталось — ближайший уровень;
    при равном расстоянии — тот, что ниже. Если не осталось совсем — None.

    Пока тело не написано, функция берёт первый незаданный вопрос,
    не глядя на уровень.
    """
    distance = 0
    while distance < 5:
        for i in [level - distance, level + distance]:
            for question in questions:
                if question['level'] == i and question['id'] not in asked:
                    return question
        distance += 1
    return None

def next_level_own(level, history):
    streak_correct = 0
    streak_wrong = 0
    current_level = level

    for result in history:
        if result == 'верно':
            streak_correct += 1
            streak_wrong = 0
            if streak_correct == 2:
                current_level == 1
                if current_level > 5:
                    current_level = 5
                streak_correct = 0
        elif result == 'неверно':
            streak_wrong += 1
            streak_correct = 0
            if streak_wrong == 2:
                current_level -= 1
                if current_level < 1:
                    current_level = 1
                streak_wrong = 0
    return current_level
