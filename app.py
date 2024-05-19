from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import numpy as np

app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'
app.static_url_path = '/static'

# Load the trained linear regression model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/', methods=['GET', 'POST'], endpoint='index')
def index():
    # prediction = None
    if request.method == 'POST':
        # Get the user inputs
        year = int(request.form['year'])
        age = int(request.form['age'])
        gender = int(request.form['gender'])
        hispanic = int(request.form['hispanic'])
        race = int(request.form['race'])
        panel  = int(request.form['panel'])

        # Create a DataFrame with the user inputs
        data = pd.DataFrame({
            'year': [year],
            'hispanic_latino_flag': [1 if hispanic == 1 else 0],
            'hispanic_latino_race': [1 if race == 0 else 0],
            'white': [1 if race == 1 else 0],
            'native_black': [1 if race == 2 else 0],
            'black_american': [1 if race == 3 else 0],
            'american_indian': [1 if race == 4 else 0],
            'asian_pacific_islander': [1 if race == 5 else 0],
            'asian': [1 if race == 6 else 0],
            'native_hawaiian': [1 if race == 7 else 0],
            'panel_any_opioid': [1 if panel == 1 else 0],
            'panel_heroin': [1 if panel == 2 else 0],
            'panel_methadone': [1 if panel == 3 else 0],
            'panel_natural_opioids': [1 if panel == 4 else 0],
            'panel_other_synthetic': [1 if panel == 5 else 0],
            'age_15-24_years': [1 if age == 1 else 0],
            'age_25-34_years': [1 if age == 2 else 0],
            'age_35-44_years': [1 if age == 3 else 0],
            'age_45-54_years': [1 if age == 4 else 0],
            'age_55-64_years': [1 if age == 5 else 0],
            'age_65-74_years': [1 if age == 6 else 0],
            'age_75-84_years': [1 if age == 7 else 0],
            'age_85_years_and_over': [1 if age == 8 else 0],
            'age_under_15_years': [1 if age == 0 else 0],
            'gender_female': [1 if gender == 1 else 0],
            'gender_male': [1 if gender == 0 else 0]
        })

        # Make the prediction
        prediction = model.predict(data)[0]
        prediction = np.round(prediction, 2)
        prediction_string = str(prediction) + ' deaths per 100,000 resident population'
        return render_template('result.html', prediction=prediction_string)
        # return render_template('result.html', prediction=data['hispanic_latino_race'].iloc[0])
        # return render_template('result.html',prediction=data.loc[0])

    return render_template('index.html')

@app.route('/result', endpoint='result')
def results():
    prediction = request.args.get('prediction', None)
    return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
