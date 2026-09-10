from datetime import datetime

project_name = "Космический хакатон"
max_participants = int(input("Введите количество мест для участников: "))
current_participants = int(input("Введите количество зарегистрированных участников: "))
application_deadline = datetime.strptime(input("Введите крайний срок подачи заявлений(yyyy-mm-dd): "), "%Y-%m-%d").date()

user_name = "Иван Петров"
user_already_applied = False

is_available = (current_participants < max_participants and datetime.today().date() <= application_deadline and not user_already_applied)

def get_application_status(is_available):
    if is_available:
        return "Заявка может быть подана"
    return "Подача заявки невозможна"

print(f"Проект: {project_name}")
print(f"Максимум участников: {max_participants}")
print(f"Уже зарегистрировано: {current_participants}")
print(f"Дедлайн подачи заявок: {application_deadline}")
print(f"Пользователь: {user_name}")
print(get_application_status(is_available))