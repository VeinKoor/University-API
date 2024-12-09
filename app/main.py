from fastapi import FastAPI
from app.utils import json_to_dict_list # Функция, которая будет возвращать всех студентов
import os # Для настройки относительных путей к JSON
from typing import Optional, List # Передавать значения по умолчанию в параметры пути и запросов
from pydantic import BaseModel # Для создания схем данных



script_dir = os.path.dirname(os.path.abspath(__file__)) # Получаем путь к директории текущего скрипта
path_to_json = os.path.join(script_dir, 'students.json') # Получаем путь к JSON

app = FastAPI()

@app.get('/')
async def home_page():
    return {'message': 'Hello World'}


#Эндпоинт с параметром запроса
@app.get('/students')
async def get_all_students(course: Optional[int] = None): # Optional означает то, что параметр необязательны, и его можно не указывать
    students = json_to_dict_list(path_to_json)
    # Если параметр "курс" не передан, возвращаем список всех студентов
    if course is None:
        return students
    else:
        return_list = []
        # Перебираем каждого студента и сравниваем его курс с тем, который мы передали в адрес
        for student in students:
            if student['course'] == course:
                return_list.append(student)
        return return_list



#Эндпоинт с параметром пути и запроса
@app.get('/students/{course}')
async def get_all_students_course(course: int, major: Optional[str] = None, enrollment_year: Optional[int] = 2018):
    students = json_to_dict_list(path_to_json)
    filtered_students = []
    # Перебираем студентов нужного нам курса
    for student in students:
        if student['course'] == course:
            filtered_students.append(student)
    # Делаем перебор по специальности, если она есть
    if major:
        filtered_students = [student for student in filtered_students if student['major'].lower() == major.lower()]
    # Делаем перебор по году поступления
    if enrollment_year:
        filtered_students = [student for student in filtered_students if student['enrollment_year'] == enrollment_year]

    return filtered_students


# Задание 1 - С параметром запроса
@app.get('/students/id/{id}')
async def get_student_by_id(student_id: int):
    students = json_to_dict_list(path_to_json)
    return_list = []

    for student in students:
        if student['student_id'] == student_id:
            return_list.append(student)

    return return_list


# Задание 2 - С параметром пути
@app.get('/students/id')
async def get_student_by_id_path(student_id: int):
    students = json_to_dict_list(path_to_json)
    return_list = []

    for student in students:
        if student['student_id'] == student_id:
            return_list.append(student)

    return return_list


