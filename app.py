# from flask import Flask, render_template, request
# import pandas as pd

# app = Flask(__name__)

# # Load dataset
# df = pd.read_csv("women_safety_data.csv")

# # Create Safety Score if not present
# if 'Safety_Score' not in df.columns:
#     max_rate = df['Crime_Rate_per_100k'].max()
#     df['Safety_Score'] = (
#         100 - (df['Crime_Rate_per_100k'] / max_rate * 100)
#     ).round(2)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/search', methods=['POST'])
# def search():

#     district = request.form['district']

#     result = df[
#         df['District'].str.contains(
#             district,
#             case=False,
#             na=False
#         )
#     ]

#     if result.empty:
#         return render_template(
#             'result.html',
#             district="Not Found",
#             risk="N/A",
#             crime_rate="N/A",
#             score="N/A"
#         )

#     row = result.iloc[0]

#     return render_template(
#         'result.html',
#         district=row['District'],
#         risk=row['Risk_Level'],
#         crime_rate=row['Crime_Rate_per_100k'],
#         score=row['Safety_Score']
#     )


# @app.route('/map')
# def map_page():
#     return render_template('map.html')  
# # @app.route('/chatbot')
# # def chatbot():
# #     return render_template('chatbot.html')

# @app.route('/sakhi-chat')
# def ai_chatbot():
#     return render_template('chatbot.html')

# @app.route('/sos')
# def sos():
#     return render_template('sos.html')    

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map')
def map_page():
    return render_template('map.html')

@app.route('/sakhi-chat')
def sakhi_chat():
    return render_template('chatbot.html')
@app.route('/sos')
def sos():
    return render_template('sos.html')
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)