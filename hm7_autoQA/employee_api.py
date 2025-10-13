import requests

class EmployeeApi:
    BASE_URL = "http://5.101.50.27:8000"

    def create_employee(self, data: dict):
        """Создание нового сотрудника"""
        url = f"{self.BASE_URL}/employee/create"
        return requests.post(url, json=data)

    def get_employee_info(self, employee_id: int):
        """Получение информации о сотруднике"""
        url = f"{self.BASE_URL}/employee/info"
        params = {"id": employee_id}
        return requests.get(url, params=params)

    def change_employee(self, employee_id: int, data: dict):
        """Изменение данных сотрудника"""
        url = f"{self.BASE_URL}/employee/change"
        payload = {"id": employee_id, **data}
        return requests.patch(url, json=payload)
