from fastapi import FastAPI
from app.utils import json_to_dict_list # Функция, которая будет возвращать всех студентов
import os # Для настройки относительных путей к JSON
from typing import Optional, List # Передавать значения по умолчанию в параметры пути и запросов
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError # Для создания схем данных
from enum import Enum # Для создания перечислений
from datetime import datetime, date # Для работы с датами
import re # Для использования регулярных выражений

script_dir = os.path.dirname(os.path.abspath(__file__)) # Получаем путь к директории текущего скрипта
path_to_json = os.path.join(script_dir, 'students.json') # Получаем путь к JSON


# Класс для перечисления факультетов, наследование от str и Enum для создания перечисления, где каждый член является строкой
class Major(str, Enum):
    informatics = "Информатика"
    economics = "Экономика"
    law = "Право"
    medicine = "Медицина"
    engineering = "Инженерия"
    languages = "Языки"



# Класс для описания модели студента
class Student(BaseModel):
    """
    Описание полей

    Default - это то значение, которое в поле будет использоваться по умолчанию. Если мы передадим значение «…»
    аргументом этого параметра, то это будет значить, что данное значение обязательно.
    В связи с этим, часто указание «default» игнорируется и запись начинается с …
    """

    student_id: str
    phone_number: str = Field(..., description='Номер телефона в международном формате, начинающийся с "+"')
    first_name: str = Field(..., min_length=1, max_length=50, description='Имя студента, от 1 до 50 символов')
    last_name: str = Field(..., min_length=1, max_length=50, description='Фамилия студента, от 1 до 50 символов')
    date_of_birth: date = Field(..., description='Дата рождения студента в формате ГГГГ-ММ-ДД')
    email: EmailStr = Field(..., description='Электронная почта студента')
    address: str = Field(..., min_length=10, max_length=200, description='Адрес студента, не более 200 символов')
    enrollment_year: int = Field(..., ge=2002, description='Год поступления, не меньше 2002')
    major: Major = Field(..., description='Специальность студента')
    course: int = Field(..., ge=1, le=5, description='Курс, в диапазоне от 1 до 5')
    special_notes: Optional[str] = Field(..., max_length=500, description='Дополнительные заметки, не более 500 символов')



    # Внутренние валидаторы
    @field_validator('phone_number') # В декоратор передаем название поля, в котором будем проверять валидность
    @classmethod
    def validate_phone_number(cls, values: str) -> str: # Первым аргументом мы передаем класс, а второй аргумент - это то значение, валидность которого мы будем проверять
        if not re.match(r'^\+\d{1,15}$', values):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return values # Возвращаем либо значение, либо ошибку


    @field_validator("date_of_birth") # В декоратор передаем название поля, в котором будем проверять валидность
    @classmethod
    def validate_date_of_birth(cls, values: date): # Первым аргументом мы передаем класс, а второй аргумент - это то значение, валидность которого мы будем проверять
        if values and values >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return values # Возвращаем либо значение, либо ошибку





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


