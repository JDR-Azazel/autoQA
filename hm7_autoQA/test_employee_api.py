import requests

BASE_URL = "http://5.101.50.27:8000"
CLIENT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoYXJyeXBvdHRlciIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc2MDE0MTQxNn0.GzGwtxG8lAPfH3IspZuYSmmgWuVxL8fHyhhYvwRJxUU"  # если API требует токен


class EmployeeApi:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def create_employee(self, first_name, last_name, middle_name=None, company_id=None,
                        email=None, phone=None, birthdate=None, is_active=True):
        url = f"{self.base_url}/employee/create"
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "company_id": company_id,
            "middle_name": middle_name,
            "email": email,
            "phone": phone,
            "birthdate": birthdate,
            "is_active": is_active
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return payload  # возвращаем данные, которые отправили, ID получим через list

    def list_employees(self, company_id):
        url = f"{self.base_url}/employee/list/{company_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_employee_id_by_email(self, company_id, email):
        employees = self.list_employees(company_id)
        for emp in employees:
            if emp.get("email") == email:
                return emp.get("id")
        raise ValueError(f"Сотрудник с email {email} не найден")

    def get_employee_info(self, employee_id):
        url = f"{self.base_url}/employee/info/{employee_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def update_employee(self, employee_id, last_name=None, email=None, phone=None, is_active=None):
        url = f"{self.base_url}/employee/change/{employee_id}?client_token={CLIENT_TOKEN}"
        payload = {}
        if last_name is not None:
            payload["last_name"] = last_name
        if email is not None:
            payload["email"] = email
        if phone is not None:
            payload["phone"] = phone
        if is_active is not None:
            payload["is_active"] = is_active
        response = requests.patch(url, json=payload)
        response.raise_for_status()
        return response.json()


# ===================== Тесты =====================

import pytest

api = EmployeeApi()


def test_create_employee():
    """Тест: создание нового сотрудника"""
    employee_data = api.create_employee(
        first_name="John",
        last_name="Doe",
        middle_name="Edward",
        company_id=1,
        email="johndoe@example.com",
        phone="+1234567890",
        birthdate="1990-01-15",
        is_active=True
    )

    # Проверяем, что данные совпадают
    assert employee_data["first_name"] == "John"
    assert employee_data["last_name"] == "Doe"
    print("Тест пройден: сотрудник успешно создан")


def test_get_employee_info():
    """Тест: получение информации о сотруднике"""
    email = "alicebrown@example.com"
    company_id = 2

    # Создаем сотрудника
    api.create_employee(
        first_name="Alice",
        last_name="Brown",
        middle_name="Marie",
        company_id=company_id,
        email=email,
        phone="+9876543210",
        birthdate="1988-05-22",
        is_active=True
    )

    # Получаем ID через список
    employee_id = api.get_employee_id_by_email(company_id, email)

    # Получаем данные сотрудника
    employee = api.get_employee_info(employee_id)
    assert employee["first_name"] == "Alice"
    assert employee["last_name"] == "Brown"
    print("Тест пройден: информация о сотруднике получена")


def test_update_employee():
    """Тест: изменение данных о сотруднике"""
    email = "bobsmith@example.com"
    company_id = 3

    # Создаем сотрудника
    api.create_employee(
        first_name="Bob",
        last_name="Smith",
        middle_name="James",
        company_id=company_id,
        email=email,
        phone="+1357924680",
        birthdate="1985-07-30",
        is_active=True
    )

    # Получаем ID через список
    employee_id = api.get_employee_id_by_email(company_id, email)

    # Обновляем фамилию и email
    updated = api.update_employee(employee_id, last_name="Johnson", email="bob.johnson@example.com")
    assert updated["last_name"] == "Johnson"
    assert updated["email"] == "bob.johnson@example.com"
    print("Тест пройден: данные сотрудника обновлены")
