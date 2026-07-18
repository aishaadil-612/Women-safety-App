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
import os
import re
import json
import urllib.request
import urllib.error
from flask import Flask, render_template, request, jsonify

# Load environment variables manually from .env if present
def load_env_manually():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                match = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*["\']?(.*?)["\']?\s*$', line)
                if match:
                    key, val = match.groups()
                    os.environ[key] = val

load_env_manually()

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

def load_safety_data():
    context = "OFFICIAL STATE SAFETY SCORES:\n"
    # 1. Parse states from templates/index.html
    try:
        path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            state_pattern = r'"state"\s*:\s*"([^"]+)"\s*,\s*"safety_score"\s*:\s*([0-9.]+)\s*,\s*"risk_level"\s*:\s*"([^"]+)"\s*,\s*"crime_rate"\s*:\s*([0-9.]+)'
            matches = re.findall(state_pattern, content)
            for state, score, risk, rate in matches:
                context += f"- {state}: Safety Score={score}/100, Risk={risk}, Crime Rate={rate} per 100K\n"
    except Exception as e:
        print("Error parsing states in load_safety_data:", e)

    # 2. Parse cities from templates/chatbot.html
    try:
        path = os.path.join(os.path.dirname(__file__), 'templates', 'chatbot.html')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            city_pattern = r'"([^"]+)"\s*:\s*\{\s*state\s*:\s*"([^"]+)"\s*,\s*score\s*:\s*([0-9.]+)\s*,\s*level\s*:\s*"([^"]+)"\s*,\s*crimes\s*:\s*([0-9.]+)\s*\}'
            matches = re.findall(city_pattern, content)
            if matches:
                context += "\nOFFICIAL CITY SAFETY SCORES:\n"
                for city, state, score, level, crimes in matches:
                    context += f"- {city.title()} (in {state.title()}): Safety Score={score}/100, Risk={level.upper()}, Reported Crimes={crimes}/yr\n"
    except Exception as e:
        print("Error parsing cities in load_safety_data:", e)
        
    return context

@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        data = request.get_json() or {}
        user_message = data.get('message', '')
        system_prompt = data.get('system', "You are a helpful safety assistant.")
        
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            return jsonify({"error": "GROQ_API_KEY not configured in backend .env file"}), 500
        
        # Load app states/cities safety dataset to feed as context for LLM
        safety_context = load_safety_data()
        enhanced_system_prompt = (
            f"{system_prompt}\n\n"
            "Below is the official safety dataset for states and cities in India from our platform database. "
            "When users ask about the safety, crime rates, or risk levels of states or cities in India, "
            "you MUST use this specific data in your response to answer accurately. Do not invent safety scores; "
            "reference our database scores exactly.\n\n"
            f"{safety_context}"
        )
        
        # Payload setup using Groq Llama 3.3 model
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": enhanced_system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 1000
        }
        
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(payload).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            reply = res_data['choices'][0]['message']['content']
            return jsonify({"reply": reply})
            
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8')
        print("Groq HTTP Error:", e.code, err_msg)
        try:
            err_json = json.loads(err_msg)
            message = err_json.get('error', {}).get('message', 'Groq API Error')
        except:
            message = f"HTTP Error {e.code}"
        return jsonify({"error": message}), 500
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)