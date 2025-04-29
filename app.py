from flask import Flask, request, jsonify
import pandas as pd
import joblib
from urllib.parse import urlparse
import re

app = Flask(__name__)

# 모델과 feature 리스트 불러오기
model = joblib.load("url_model_new.pkl")

features = [
    'hostname_length', 'count_dir', 'count-www',
    'url_length', 'fd_length', 'count-', 'count.',
    'tld_length', 'count-digits', 'count='
]

def extract_features(url):
    def fd_length(url):
        try:
            return len(urlparse(url).path.split('/')[1])
        except:
            return 0

    def get_tld_length(url):
        try:
            return len(url.split('.')[-1])
        except:
            return -1

    return {
        'hostname_length': len(urlparse(url).netloc),
        'count_dir': urlparse(url).path.count('/'),
        'count-www': url.count('www'),
        'url_length': len(url),
        'fd_length': fd_length(url),
        'count-': url.count('-'),
        'count.': url.count('.'),
        'tld_length': get_tld_length(url),
        'count-digits': sum(c.isdigit() for c in url),
        'count=': url.count('=')
    }

@app.route('/api/v1/ai/verify', methods=['POST'])
def verify():
    data = request.get_json()
    url = data.get("url", "")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    feature_data = pd.DataFrame([extract_features(url)])[features]
    prediction = model.predict(feature_data)[0]
    return jsonify({"result": int(prediction)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
