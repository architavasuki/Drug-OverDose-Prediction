from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

app = Flask(__name__, template_folder='templates')

# Load the trained linear regression model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the user inputs
    age = int(request.form['age'])
    gender = int(request.form['gender'])
    race = int(request.form['race'])
    hispanic = int(request.form['hispanic'])
    year = int(request.form['year'])

    # Create a DataFrame with the user inputs
    data = pd.DataFrame({'age': [age], 'gender': [gender], 'race': [race], 'hispanic': [hispanic], 'year': [year]})

    # Make the prediction
    prediction = model.predict(data)

    # Return the prediction
    return render_template('result.html', prediction=prediction[0])

if __name__ == '__main__':
    app.run(debug=True)
