import pandas as pd
import csv
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class User:
    """User class for processing healthcare survey data"""
    
    def __init__(self, age, gender, total_income, expenses, user_id=None, created_at=None):
        self.user_id = user_id
        self.age = int(age)
        self.gender = str(gender).lower()
        self.total_income = float(total_income)
        self.expenses = expenses if isinstance(expenses, dict) else {}
        self.created_at = created_at or datetime.now()
        self._validate_data()
    
    def _validate_data(self):
        if self.age < 0 or self.age > 150:
            raise ValueError(f"Invalid age: {self.age}")
        
        if self.total_income < 0:
            raise ValueError(f"Invalid income: {self.total_income}")
        
        for category, amount in self.expenses.items():
            if amount < 0:
                raise ValueError(f"Invalid expense amount for {category}: {amount}")
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'age': self.age,
            'gender': self.gender,
            'total_income': self.total_income,
            'utilities': self.expenses.get('utilities', 0),
            'entertainment': self.expenses.get('entertainment', 0),
            'school_fees': self.expenses.get('school_fees', 0),
            'shopping': self.expenses.get('shopping', 0),
            'healthcare': self.expenses.get('healthcare', 0),
            'total_expenses': self.calculate_total_expenses(),
            'savings': self.calculate_savings(),
            'expense_ratio': self.calculate_expense_ratio(),
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else str(self.created_at)
        }
    
    def to_csv_row(self):
        return [
            self.user_id or '',
            self.age,
            self.gender,
            self.total_income,
            self.expenses.get('utilities', 0),
            self.expenses.get('entertainment', 0),
            self.expenses.get('school_fees', 0),
            self.expenses.get('shopping', 0),
            self.expenses.get('healthcare', 0),
            self.calculate_total_expenses(),
            self.calculate_savings(),
            self.calculate_expense_ratio(),
            self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else str(self.created_at)
        ]
    
    def calculate_total_expenses(self):
        return sum(self.expenses.values())
    
    def calculate_savings(self):
        return self.total_income - self.calculate_total_expenses()
    
    def calculate_expense_ratio(self):
        if self.total_income == 0:
            return 0
        return (self.calculate_total_expenses() / self.total_income) * 100
    
    def get_expense_breakdown(self):
        total_expenses = self.calculate_total_expenses()
        if total_expenses == 0:
            return {category: 0 for category in self.expenses.keys()}
        
        return {
            category: (amount / total_expenses) * 100 
            for category, amount in self.expenses.items()
        }
    
    def get_highest_expense_category(self):
        if not self.expenses:
            return None
        return max(self.expenses.items(), key=lambda x: x[1])
    
    def is_overspending(self):
        return self.calculate_total_expenses() > self.total_income
    
    def get_financial_health_score(self):
        expense_ratio = self.calculate_expense_ratio()
        
        if expense_ratio <= 50:
            return 100
        elif expense_ratio <= 70:
            return 80
        elif expense_ratio <= 90:
            return 60
        elif expense_ratio <= 100:
            return 40
        else:
            return 20
    
    def __str__(self):
        return f"User(age={self.age}, gender={self.gender}, income=${self.total_income:.2f}, expenses=${self.calculate_total_expenses():.2f})"
    
    def __repr__(self):
        return self.__str__()


class UserDataProcessor:
    """Class for processing collections of User data"""
    
    def __init__(self):
        self.users = []
        self.csv_headers = [
            'user_id', 'age', 'gender', 'total_income',
            'utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare',
            'total_expenses', 'savings', 'expense_ratio', 'created_at'
        ]
    
    def add_user(self, user):
        if not isinstance(user, User):
            raise TypeError("Expected User instance")
        self.users.append(user)
    
    def add_users_from_data(self, data_list):
        for data in data_list:
            try:
                if hasattr(data, 'to_dict'):
                    user = User(
                        age=data.age,
                        gender=data.gender,
                        total_income=data.total_income,
                        expenses=data.expenses,
                        user_id=str(data._id),
                        created_at=data.created_at
                    )
                else:
                    user = User(
                        age=data.get('age'),
                        gender=data.get('gender'),
                        total_income=data.get('total_income'),
                        expenses=data.get('expenses', {}),
                        user_id=data.get('_id') or data.get('user_id'),
                        created_at=data.get('created_at')
                    )
                self.add_user(user)
            except (ValueError, KeyError) as e:
                logger.warning(f"Skipping invalid user data: {e}")
                continue
    
    def export_to_csv(self, file_path='./exports/survey_data.csv'):
        if not self.users:
            logger.warning("No users to export")
            return False
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                writer.writerow(self.csv_headers)
                for user in self.users:
                    writer.writerow(user.to_csv_row())
            
            logger.info(f"Successfully exported {len(self.users)} users to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return False
    
    def export_to_pandas(self):
        if not self.users:
            return pd.DataFrame()
        
        data = [user.to_dict() for user in self.users]
        return pd.DataFrame(data)
    
    def get_statistics(self):
        if not self.users:
            return {}
        
        df = self.export_to_pandas()
        
        stats = {
            'total_users': len(self.users),
            'age_stats': {
                'mean': df['age'].mean(),
                'median': df['age'].median(),
                'min': df['age'].min(),
                'max': df['age'].max()
            },
            'income_stats': {
                'mean': df['total_income'].mean(),
                'median': df['total_income'].median(),
                'min': df['total_income'].min(),
                'max': df['total_income'].max()
            },
            'gender_distribution': df['gender'].value_counts().to_dict(),
            'expense_stats': {
                'utilities': df['utilities'].mean(),
                'entertainment': df['entertainment'].mean(),
                'school_fees': df['school_fees'].mean(),
                'shopping': df['shopping'].mean(),
                'healthcare': df['healthcare'].mean()
            },
            'financial_health': {
                'avg_expense_ratio': df['expense_ratio'].mean(),
                'overspending_count': len([u for u in self.users if u.is_overspending()]),
                'avg_savings': df['savings'].mean()
            }
        }
        
        return stats
    
    def get_users_by_criteria(self, **criteria):
        filtered_users = self.users
        
        for key, value in criteria.items():
            if key == 'min_age':
                filtered_users = [u for u in filtered_users if u.age >= value]
            elif key == 'max_age':
                filtered_users = [u for u in filtered_users if u.age <= value]
            elif key == 'gender':
                filtered_users = [u for u in filtered_users if u.gender.lower() == value.lower()]
            elif key == 'min_income':
                filtered_users = [u for u in filtered_users if u.total_income >= value]
            elif key == 'max_income':
                filtered_users = [u for u in filtered_users if u.total_income <= value]
            elif key == 'overspending':
                if value:
                    filtered_users = [u for u in filtered_users if u.is_overspending()]
                else:
                    filtered_users = [u for u in filtered_users if not u.is_overspending()]
        
        return filtered_users
    
    def clear_users(self):
        self.users.clear()
    
    def __len__(self):
        return len(self.users)
    
    def __str__(self):
        return f"UserDataProcessor(users={len(self.users)})"