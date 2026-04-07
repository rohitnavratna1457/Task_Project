# accounts/services.py

from datetime import date, datetime

class IllustrationService:

    def execute(self, data):

        self.validate(data)
        data = self.normalize(data)
        age = self.calculate_age(data['dob'])
        illustration = self.generate_illustration(data, age)

        return {
            "age": age,
            "illustration": illustration
        }

    def validate(self, data):
        if data['premium'] <= 0:
            raise ValueError("Premium must be greater than 0")

        if data['term'] <= 0:
            raise ValueError("Invalid term")

        if data['sum_assured'] <= 0:
            raise ValueError("Invalid sum assured")

        if data['frequency'] not in ['yearly', 'monthly']:
            raise ValueError("Invalid frequency")

        age = self.calculate_age(data['dob'])
        if age < 18:
            raise ValueError("Minimum age is 18")

    def calculate_age(self, dob):
        today = date.today()
        return today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )

    def normalize(self, data):
        if data['frequency'] == 'monthly':
            data['premium'] = data['premium'] * 12
        return data

    def generate_illustration(self, data, age):

        premium = data['premium']
        term = data['term']
        sum_assured = data['sum_assured']

        rows = []
        total_premium = 0

        for year in range(1, term + 1):
            total_premium += premium
            bonus = total_premium * 0.05
            maturity = sum_assured + bonus

            rows.append({
                "year": year,
                "age": age + year,
                "premium_paid": total_premium,
                "bonus": round(bonus, 2),
                "maturity": round(maturity, 2)
            })

        return rows