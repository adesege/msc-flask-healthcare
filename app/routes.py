from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app.forms import SurveyForm
from app.models import SurveyResponse, User
import numpy as np

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html', title='Healthcare Survey Portal')


@bp.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()
    
    if form.validate_on_submit():
        try:
            expenses = form.get_expenses_dict()
            response = SurveyResponse(
                age=form.age.data,
                gender=form.gender.data,
                total_income=form.total_income.data,
                expenses=expenses
            )
            result = response.save()
            
            if result:
                flash('Survey submitted successfully!', 'success')
                return redirect(url_for('main.success'))
            else:
                flash('Error saving survey data. Please try again.', 'error')
                
        except Exception as e:
            current_app.logger.error(f"Error saving survey: {str(e)}")
            flash('An error occurred while submitting your survey. Please try again.', 'error')
    
    return render_template('survey.html', form=form, title='Healthcare Survey')


@bp.route('/success')
def success():
    return render_template('success.html', title='Survey Completed')


@bp.route('/api/responses')
def api_responses():
    try:
        responses = SurveyResponse.find_all()
        data = []
        for response in responses:
            response_dict = response.to_dict()
            response_dict['_id'] = str(response_dict['_id'])
            response_dict['created_at'] = response_dict['created_at'].isoformat()
            data.append(response_dict)
        
        return jsonify({
            'success': True,
            'count': len(data),
            'data': data
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching responses: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@bp.route('/admin/dashboard')
def admin_dashboard():
    try:
        responses = SurveyResponse.find_all()
        
        total_responses = len(responses)
        
        if total_responses == 0:
            stats = {
                'total_responses': 0,
                'avg_age': 0,
                'avg_income': 0,
                'gender_distribution': {},
                'expense_totals': {}
            }
        else:
            avg_age = sum(r.age for r in responses) / total_responses
            avg_income = sum(r.total_income for r in responses) / total_responses
            gender_dist = {}
            for response in responses:
                gender = response.gender
                gender_dist[gender] = gender_dist.get(gender, 0) + 1
            expense_totals = {
                'utilities': sum(r.expenses.get('utilities', 0) for r in responses),
                'entertainment': sum(r.expenses.get('entertainment', 0) for r in responses),
                'school_fees': sum(r.expenses.get('school_fees', 0) for r in responses),
                'shopping': sum(r.expenses.get('shopping', 0) for r in responses),
                'healthcare': sum(r.expenses.get('healthcare', 0) for r in responses)
            }
            
            stats = {
                'total_responses': total_responses,
                'avg_age': round(avg_age, 1),
                'avg_income': round(avg_income, 2),
                'gender_distribution': gender_dist,
                'expense_totals': expense_totals
            }
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in admin dashboard: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@bp.route('/api/generate-sample-data', methods=['POST'])
def generate_sample_data():
    try:
        count = request.args.get('count', 150, type=int)
        override = request.args.get('override', 'false').lower() == 'true'
        
        if count <= 0 or count > 10000:
            return jsonify({
                'success': False,
                'error': 'Count must be between 1 and 10000'
            }), 400
        
        if override:
            current_app.db.survey_responses.delete_many({})
        
        np.random.seed(42)
        
        generated_responses = []
        for i in range(count):
            age = int(np.random.normal(35, 12))
            age = max(18, min(70, age))
            
            gender = np.random.choice(['male', 'female', 'other'], p=[0.45, 0.50, 0.05])
            
            total_income = float(np.random.exponential(3000) + 2000)
            
            expenses = {
                'utilities': float(np.random.exponential(150) + 50),
                'entertainment': float(np.random.exponential(200) + 30),
                'school_fees': float(np.random.exponential(300) * np.random.binomial(1, 0.3)),
                'shopping': float(np.random.exponential(250) + 100),
                'healthcare': float(np.random.exponential(180) + 80)
            }
            
            response = SurveyResponse(
                age=age,
                gender=gender,
                total_income=total_income,
                expenses=expenses
            )
            
            response.save()
            generated_responses.append(response._id)
        
        return jsonify({
            'success': True,
            'message': f'Successfully generated {count} sample survey responses',
            'count': count,
            'override': override,
            'generated_ids': [str(id) for id in generated_responses]
        })
        
    except Exception as e:
        current_app.logger.error(f"Error generating sample data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
