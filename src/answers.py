"""Задание 1. Проверка ответа.

Этот модуль ничего не печатает: он возвращает результат, а печатает exam.py.
Название функции и то, что она принимает, менять нельзя: её вызывают exam.py
и тесты. Меняй тело функции.
"""


def check_answer(question, raw):
    answer = raw.strip().lower()
    correct = question["answer"].strip().lower()
    if answer == "":
        return "нет ответа"
    if question["type"] == "один":
        if answer == correct:
            return "верно"
        else:
            return "неверно"
    elif question["type"] == "несколько":
        user = answer.split(",")
        right = correct.split(",")
        user = [x.strip() for x in user]
        right = [x.strip() for x in right]
        if len(user) == len(right) and sorted(user) == sorted(right):
            return "верно"
        else:
            return "неверно"
    elif question["type"] == "короткий":
        var = correct.split("|")
        if answer in var:
            return "верно"
        else:
            return "неверно"

