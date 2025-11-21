import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import joblib

#accuracy is 88%
data = pd.read_csv("Salary Data.csv")

X = data[["Age", "Years of Experience"]]
Y = data["Salary"]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, Y_train)

age = 18
experience = 4

input_data = pd.DataFrame([[age, experience]],
columns=['Age','Years of Experience'])
value = model.predict(input_data)[0]
print(f"Predicted Salary is ${value:,.2f}")