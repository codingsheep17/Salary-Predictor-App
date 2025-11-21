# Salary Predictor Web App
---

## Features
- **User Authentication**: Secure sign-up and login system with hashed passwords.  
- **Salary Prediction**: Predict salary based on age and years of experience using a trained machine learning model.  
- **Prediction History**: Users can view their last 5 predictions with timestamps.  
- **Responsive & Modern UI**: Styled with **CSS** and maintains consistent theme throughout.  
- **Tech Stack Used**:  
  - **Python**  
  - **Flask**  
  - **Jinja2**  
  - **MySQL**  
  - **NumPy & Pandas**  
  - **scikit-learn**  
  - **joblib**  

---

## Installation & Setup

1. **Clone the repository**
git clone https://github.com/yourusername/salary-predictor.git
cd salary-predictor
Install dependencies

pip install -r requirements.txt
Create .env file with your credentials:

DB_HOST=localhost
DB_USERNAME=root
DB_PASSWORD=yourpassword
DB_NAME=salary_predictor
SECRET_KEY=your_secret_key
Initialize the database using the provided SQL scripts.

Run the Flask app

python app.py
Open in browser

cpp
Copy code
http://127.0.0.1:5000
