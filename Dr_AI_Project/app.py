import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Setup Gemini (Paatha library simple ga untundi)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Local Data (Idi unte API fail ayina project fail avvadu)
DISEASE_DATA = {
    "fever": "Possible Viral Fever. Take Paracetamol 500mg. Drink plenty of water and rest.",
    "headache": "Tension Headache. Take Saridon or Dolo 650. Rest in a dark, quiet room.",
    "cold": "Common Cold. Take Cetirizine or use Vicks Vaporub. Drink warm fluids.",
    "stomach pain": "Indigestion or Acidity. Take Digene or Pantoprazole. Avoid spicy food.",
    "dizzy": "Possible dehydration or low BP. Drink ORS/Electrol immediately. Sit down and rest.",
    "cough": "Dry/Wet Cough. Syrup: Ascoril or Grilinctus. Honey with warm water helps.",
    "back pain": "Muscle strain. Use Volini spray or take Zerodol-P. Apply hot water bag."
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_dr_ai():
    user_query = request.json.get("message").lower()
    
    # Check local data first (Data Science Approach)
    for disease, info in DISEASE_DATA.items():
        if disease in user_query:
            return jsonify({"answer": f"**Local Diagnosis:** {info} \n\n *Note: Consult a doctor.*"})

    # If not in local, try Gemini
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Dr. AI: {user_query}. Suggest meds & disclaimer.")
        return jsonify({"answer": response.text})
    except Exception:
        return jsonify({"answer": "Dr. AI is busy, but based on common symptoms, please rest and consult a doctor."})

if __name__ == '__main__':
    app.run(debug=True)