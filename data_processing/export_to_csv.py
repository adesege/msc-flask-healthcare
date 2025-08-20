#!/usr/bin/env python3
"""
CSV Export Script for Healthcare Survey Data
This script demonstrates the data processing workflow as required by the assignment
"""

import sys
import os
import logging
from datetime import datetime

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import SurveyResponse
from data_processing.user_processor import User, UserDataProcessor
from app import create_app

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def export_survey_data_to_csv(output_file='./exports/survey_data.csv'):
    """
    Main function to export survey data to CSV
    This demonstrates the complete workflow as required by the assignment
    """
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        try:
            logger.info("Starting CSV export process...")
            
            # Step 1: Fetch all survey responses from MongoDB
            logger.info("Fetching survey responses from MongoDB...")
            survey_responses = SurveyResponse.find_all()
            
            if not survey_responses:
                logger.warning("No survey responses found in database")
                return False
            
            logger.info(f"Found {len(survey_responses)} survey responses")
            
            # Step 2: Create User data processor
            processor = UserDataProcessor()
            
            # Step 3: Loop through collected data and create User objects
            logger.info("Processing survey responses...")
            successful_processed = 0
            
            for response in survey_responses:
                try:
                    # Create User object from survey response
                    user = User(
                        age=response.age,
                        gender=response.gender,
                        total_income=response.total_income,
                        expenses=response.expenses,
                        user_id=str(response._id),
                        created_at=response.created_at
                    )
                    
                    processor.add_user(user)
                    successful_processed += 1
                    
                except Exception as e:
                    logger.error(f"Error processing response {response._id}: {e}")
                    continue
            
            logger.info(f"Successfully processed {successful_processed} users")
            
            # Step 4: Export to CSV file
            logger.info(f"Exporting data to CSV file: {output_file}")
            success = processor.export_to_csv(output_file)
            
            if success:
                logger.info("CSV export completed successfully!")
                
                # Step 5: Generate statistics
                stats = processor.get_statistics()
                print_statistics(stats)
                
                return True
            else:
                logger.error("CSV export failed")
                return False
                
        except Exception as e:
            logger.error(f"Error in export process: {e}")
            return False


def print_statistics(stats):
    """Print formatted statistics"""
    print("\n" + "="*60)
    print("HEALTHCARE SURVEY DATA STATISTICS")
    print("="*60)
    
    print(f"\nTotal Participants: {stats['total_users']}")
    
    print(f"\nAge Statistics:")
    print(f"  Mean Age: {stats['age_stats']['mean']:.1f} years")
    print(f"  Age Range: {stats['age_stats']['min']:.0f} - {stats['age_stats']['max']:.0f} years")
    
    print(f"\nIncome Statistics:")
    print(f"  Mean Income: ${stats['income_stats']['mean']:,.2f}")
    print(f"  Income Range: ${stats['income_stats']['min']:,.2f} - ${stats['income_stats']['max']:,.2f}")
    
    print(f"\nGender Distribution:")
    for gender, count in stats['gender_distribution'].items():
        percentage = (count / stats['total_users']) * 100
        print(f"  {gender.title()}: {count} ({percentage:.1f}%)")
    
    print(f"\nAverage Monthly Expenses:")
    for category, amount in stats['expense_stats'].items():
        print(f"  {category.replace('_', ' ').title()}: ${amount:.2f}")
    
    print(f"\nFinancial Health:")
    print(f"  Average Expense Ratio: {stats['financial_health']['avg_expense_ratio']:.1f}%")
    print(f"  Users Overspending: {stats['financial_health']['overspending_count']}")
    print(f"  Average Monthly Savings: ${stats['financial_health']['avg_savings']:,.2f}")
    
    print("\n" + "="*60)


def export_filtered_data():
    """
    Example function showing how to export filtered data
    This demonstrates advanced data processing capabilities
    """
    app = create_app()
    
    with app.app_context():
        try:
            # Get all responses
            responses = SurveyResponse.find_all()
            processor = UserDataProcessor()
            processor.add_users_from_data(responses)
            
            # Export different filtered datasets
            
            # 1. High income users (>$5000)
            high_income_users = processor.get_users_by_criteria(min_income=5000)
            if high_income_users:
                high_income_processor = UserDataProcessor()
                for user in high_income_users:
                    high_income_processor.add_user(user)
                high_income_processor.export_to_csv('./exports/high_income_users.csv')
                logger.info(f"Exported {len(high_income_users)} high income users")
            
            # 2. Young adults (18-30)
            young_adults = processor.get_users_by_criteria(min_age=18, max_age=30)
            if young_adults:
                young_processor = UserDataProcessor()
                for user in young_adults:
                    young_processor.add_user(user)
                young_processor.export_to_csv('./exports/young_adults.csv')
                logger.info(f"Exported {len(young_adults)} young adult users")
            
            # 3. Users overspending
            overspending_users = processor.get_users_by_criteria(overspending=True)
            if overspending_users:
                overspending_processor = UserDataProcessor()
                for user in overspending_users:
                    overspending_processor.add_user(user)
                overspending_processor.export_to_csv('./exports/overspending_users.csv')
                logger.info(f"Exported {len(overspending_users)} overspending users")
            
        except Exception as e:
            logger.error(f"Error in filtered export: {e}")


def validate_csv_output(csv_file='./exports/survey_data.csv'):
    """
    Validate the generated CSV file
    """
    try:
        import pandas as pd
        
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        print(f"\nCSV Validation Results:")
        print(f"File: {csv_file}")
        print(f"Rows: {len(df)}")
        print(f"Columns: {len(df.columns)}")
        print(f"Columns: {list(df.columns)}")
        
        # Check for missing values
        missing_values = df.isnull().sum()
        if missing_values.sum() > 0:
            print(f"\nMissing values found:")
            for col, count in missing_values.items():
                if count > 0:
                    print(f"  {col}: {count}")
        else:
            print("\nNo missing values found - CSV is clean!")
        
        # Display first few rows
        print(f"\nFirst 3 rows of data:")
        print(df.head(3).to_string())
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating CSV: {e}")
        return False


if __name__ == "__main__":
    """
    Command-line interface for CSV export
    Usage: python export_to_csv.py [output_file]
    """
    
    # Check command line arguments
    output_file = './exports/survey_data.csv'
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    
    # Create exports directory
    os.makedirs('./exports', exist_ok=True)
    
    print("Healthcare Survey Data Export Tool")
    print("=" * 40)
    
    # Run main export
    success = export_survey_data_to_csv(output_file)
    
    if success:
        print(f"\n✅ Data successfully exported to: {output_file}")
        
        # Validate the output
        validate_csv_output(output_file)
        
        # Ask if user wants filtered exports
        try:
            response = input("\nWould you like to generate filtered datasets? (y/n): ")
            if response.lower() in ['y', 'yes']:
                export_filtered_data()
                print("✅ Filtered datasets generated!")
        except KeyboardInterrupt:
            print("\nExport completed.")
    else:
        print("\n❌ Export failed. Check the logs for details.")
        sys.exit(1)