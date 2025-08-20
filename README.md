# Healthcare Survey Application

A Flask-based web application for collecting and analyzing healthcare spending data. This survey tool gathers participant information to analyze income and spending patterns for healthcare industry research.

## Project Overview

This application provides:

- Flask application for data collection
- MongoDB for data persistence  
- Python classes for data manipulation
- Jupyter notebook with analysis
- Docker containerization with nginx reverse proxy
- MongoDB Express web interface

## Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone and Setup**
   ```bash
   git clone https://github.com/adesege/msc-flask-healthcare.git
   cd msc-flask-healthcare
   cp .env.example .env
   ```

2. **Run with Docker Compose**
   ```bash
   # Start main application and database
   docker compose up -d
   
   # View logs
   docker compose logs -f
   ```

3. **Access the Application**
   - Web Application: http://localhost:4500 or http://healthcare-flask.fadojutimi.com:4500/
   - Jupyter Notebook: http://localhost:4500/jupyter/ (token: healthcare-analysis) or http://healthcare-flask.fadojutimi.com:4500/jupyter
   - MongoDB Express: http://localhost:8081/mongo/ (admin/pass)
   - Health Check: http://localhost:4500/health

### Option 2: Local Development

1. **Setup Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Setup MongoDB**
   ```bash
   # Install and start MongoDB locally
   # macOS with Homebrew:
   brew install mongodb-community
   brew services start mongodb-community
   
   # Or use Docker:
   docker run -d -p 27017:27017 --name mongodb mongo:7.0
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

4. **Run the Application**
   ```bash
   python run.py
   ```

## Data Analysis

### Running Jupyter Notebook

1. **With Docker Compose (Nginx Routed)**
   ```bash
   docker compose up -d
   # Access at: http://localhost:4500/jupyter/ (token: healthcare-analysis)
   ```

2. **Local Jupyter**
   ```bash
   jupyter notebook notebooks/data_analysis.ipynb
   ```

### Data Export

**Note**: Due to permissions restrictions in production environments, exported files are stored in `/tmp/` directory.

```bash
# Export survey data to CSV
python data_processing/export_to_csv.py
```

## Analysis Features

The Jupyter notebook provides comprehensive analysis including:

1. **Income Analysis by Age**
   - Age groups with highest average income
   - Income distribution visualizations
   - Trend analysis and correlations

2. **Gender Spending Patterns**
   - Spending distribution across categories by gender
   - Comparative analysis between genders
   - Statistical summaries and insights

3. **Healthcare Insights**
   - Healthcare spending vs income correlation
   - Age-based healthcare spending patterns
   - Top healthcare spenders analysis

4. **Interactive Visualizations**
   - Plotly charts for data exploration
   - Exportable charts for presentations
   - Executive summary dashboard

## API Endpoints

### Survey Data
- `GET /` - Survey form homepage
- `POST /survey` - Submit survey data
- `GET /success` - Success page
- `GET /api/responses` - Get all survey responses (JSON)
- `GET /admin/dashboard` - Admin statistics
- `GET /api/generate-sample-data` - Seed the database with sample data

## Configuration

### Environment Variables
See `.env.example` for all available configuration options.

### MongoDB Configuration
- **Local**: `mongodb://localhost:27017/healthcare_survey`
- **Docker**: `mongodb://mongodb:27017/healthcare_survey`
