import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

df = pd.read_csv('Data.csv')
print(df.head(10))

X = df['Study_Hours'].values.reshape(-1, 1)
y = df['Exam_Marks'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

user_input = float(input("Enter the number of study hours: "))
predicted_marks = model.predict(np.array([[user_input]]))
print(f"Predicted Exam Marks: {predicted_marks[0]}")
