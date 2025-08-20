from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional


class SurveyForm(FlaskForm):
    # Personal Information
    age = IntegerField(
        'Age', 
        validators=[DataRequired(), NumberRange(min=18, max=120, message="Age must be between 18 and 120")],
        render_kw={"class": "form-control", "placeholder": "Enter your age"}
    )
    
    gender = SelectField(
        'Gender',
        choices=[('', 'Select Gender'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer_not_to_say', 'Prefer not to say')],
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    
    total_income = FloatField(
        'Total Monthly Income ($)',
        validators=[DataRequired(), NumberRange(min=0, message="Income must be a positive number")],
        render_kw={"class": "form-control", "placeholder": "Enter your total monthly income", "step": "0.01"}
    )
    
    # Expense Categories with Checkboxes and Amount Fields
    utilities_check = BooleanField(
        'Utilities',
        render_kw={"class": "form-check-input"}
    )
    utilities_amount = FloatField(
        'Utilities Amount ($)',
        validators=[Optional(), NumberRange(min=0, message="Amount must be positive")],
        render_kw={"class": "form-control expense-amount", "placeholder": "0.00", "step": "0.01", "disabled": True}
    )
    
    entertainment_check = BooleanField(
        'Entertainment',
        render_kw={"class": "form-check-input"}
    )
    entertainment_amount = FloatField(
        'Entertainment Amount ($)',
        validators=[Optional(), NumberRange(min=0, message="Amount must be positive")],
        render_kw={"class": "form-control expense-amount", "placeholder": "0.00", "step": "0.01", "disabled": True}
    )
    
    school_fees_check = BooleanField(
        'School Fees',
        render_kw={"class": "form-check-input"}
    )
    school_fees_amount = FloatField(
        'School Fees Amount ($)',
        validators=[Optional(), NumberRange(min=0, message="Amount must be positive")],
        render_kw={"class": "form-control expense-amount", "placeholder": "0.00", "step": "0.01", "disabled": True}
    )
    
    shopping_check = BooleanField(
        'Shopping',
        render_kw={"class": "form-check-input"}
    )
    shopping_amount = FloatField(
        'Shopping Amount ($)',
        validators=[Optional(), NumberRange(min=0, message="Amount must be positive")],
        render_kw={"class": "form-control expense-amount", "placeholder": "0.00", "step": "0.01", "disabled": True}
    )
    
    healthcare_check = BooleanField(
        'Healthcare',
        render_kw={"class": "form-check-input"}
    )
    healthcare_amount = FloatField(
        'Healthcare Amount ($)',
        validators=[Optional(), NumberRange(min=0, message="Amount must be positive")],
        render_kw={"class": "form-control expense-amount", "placeholder": "0.00", "step": "0.01", "disabled": True}
    )
    
    submit = SubmitField(
        'Submit Survey',
        render_kw={"class": "btn btn-primary btn-lg"}
    )
    
    def get_expenses_dict(self):
        expenses = {}
        
        if self.utilities_check.data and self.utilities_amount.data is not None:
            expenses['utilities'] = float(self.utilities_amount.data)
        else:
            expenses['utilities'] = 0.0
            
        if self.entertainment_check.data and self.entertainment_amount.data is not None:
            expenses['entertainment'] = float(self.entertainment_amount.data)
        else:
            expenses['entertainment'] = 0.0
            
        if self.school_fees_check.data and self.school_fees_amount.data is not None:
            expenses['school_fees'] = float(self.school_fees_amount.data)
        else:
            expenses['school_fees'] = 0.0
            
        if self.shopping_check.data and self.shopping_amount.data is not None:
            expenses['shopping'] = float(self.shopping_amount.data)
        else:
            expenses['shopping'] = 0.0
            
        if self.healthcare_check.data and self.healthcare_amount.data is not None:
            expenses['healthcare'] = float(self.healthcare_amount.data)
        else:
            expenses['healthcare'] = 0.0
        
        return expenses