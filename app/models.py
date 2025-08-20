from datetime import datetime
from bson import ObjectId
from flask import current_app


class SurveyResponse:
    def __init__(self, age, gender, total_income, expenses, _id=None, created_at=None):
        self._id = _id or ObjectId()
        self.age = int(age)
        self.gender = gender
        self.total_income = float(total_income)
        self.expenses = expenses
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            '_id': self._id,
            'age': self.age,
            'gender': self.gender,
            'total_income': self.total_income,
            'expenses': self.expenses,
            'created_at': self.created_at
        }
    
    def save(self):
        if current_app.db is None:
            raise Exception("Database connection not available")
        
        result = current_app.db.survey_responses.insert_one(self.to_dict())
        self._id = result.inserted_id
        return result
    
    @classmethod
    def find_all(cls):
        if current_app.db is None:
            return []
        
        responses = []
        for doc in current_app.db.survey_responses.find():
            response = cls(
                age=doc['age'],
                gender=doc['gender'],
                total_income=doc['total_income'],
                expenses=doc['expenses'],
                _id=doc['_id'],
                created_at=doc['created_at']
            )
            responses.append(response)
        return responses
    
    @classmethod
    def find_by_id(cls, response_id):
        if current_app.db is None:
            return None
        
        doc = current_app.db.survey_responses.find_one({'_id': ObjectId(response_id)})
        if doc:
            return cls(
                age=doc['age'],
                gender=doc['gender'],
                total_income=doc['total_income'],
                expenses=doc['expenses'],
                _id=doc['_id'],
                created_at=doc['created_at']
            )
        return None
    
    def calculate_total_expenses(self):
        return sum(self.expenses.values())
    
    def get_expense_breakdown(self):
        total = self.calculate_total_expenses()
        if total == 0:
            return {category: 0 for category in self.expenses.keys()}
        
        return {
            category: (amount / total) * 100 
            for category, amount in self.expenses.items()
        }


class User:
    def __init__(self, age, gender, total_income, expenses):
        self.age = int(age)
        self.gender = gender
        self.total_income = float(total_income)
        self.expenses = expenses
    
    def to_dict(self):
        return {
            'age': self.age,
            'gender': self.gender,
            'total_income': self.total_income,
            'expenses': self.expenses,
            'total_expenses': self.calculate_total_expenses()
        }
    
    def to_csv_row(self):
        return [
            self.age,
            self.gender,
            self.total_income,
            self.expenses.get('utilities', 0),
            self.expenses.get('entertainment', 0),
            self.expenses.get('school_fees', 0),
            self.expenses.get('shopping', 0),
            self.expenses.get('healthcare', 0),
            self.calculate_total_expenses()
        ]
    
    def calculate_total_expenses(self):
        return sum(self.expenses.values())
    
    def get_expense_breakdown(self):
        total = self.calculate_total_expenses()
        if total == 0:
            return {category: 0 for category in self.expenses.keys()}
        
        return {
            category: (amount / total) * 100 
            for category, amount in self.expenses.items()
        }