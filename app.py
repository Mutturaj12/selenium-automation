# app.py
from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder='static')

DEEPSEEK_API_KEY = 'sk-345968e7cd4d4c93a81e10f8c1387db7'

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/generate', methods=['POST'])
def generate_code():
    data = request.get_json()
    url = data.get("url")
    user_flow = data.get("user_flow")

    if not url or not user_flow:
        return jsonify({"error": "Missing URL or User Flow"}), 400

    full_prompt = f"""
    You are an expert Selenium Python developer.

    Generate Python Selenium code that:
    1. Opens this website: {url}
    2. {user_flow}

    Requirements:
    - Use try-except-finally structure for every action
    - Use WebDriverWait with Xpaths only
    - Add delays (time.sleep(2)) after every action
    - Add print statements after each action
    - Use ChromeOptions to suppress:
      - Popups
      - Password manager prompts
      - Infobars ("Chrome is being controlled...")
      - Certificate errors
      - Notifications
    - Handle unexpected alerts/popups if they occur
    - Set implicit wait of 10 seconds
    - Maximize browser window
    - Disable Chrome Password Manager
    - Use advanced options:
      --disable-popup-blocking
      --disable-infobars
      --disable-autofill-passwords
      --ignore-certificate-errors
      --disable-notifications
      --excludeSwitches=enable-automation
      --disable-blink-features=AutomationControlled
      prefs: disable password service and manager
    - Include alert dismissal logic
    - Use graceful driver.quit()
    - Output should be ready to copy-paste and run without modification

    Special Instructions:
    - If any element cannot be clicked due to overlap (e.g., 'element click intercepted'), scroll it into view using JavaScript.
    - If an element is still not clickable, use JavaScript to perform the click: driver.execute_script("arguments[0].click();", element)
    - If there are known overlaying elements like <div id="fixedban">, remove or hide them using JavaScript:
      driver.execute_script("document.getElementById('fixedban').remove();")
    - Always verify that the user flow completes even in presence of fixed banners or overlays
    """

    deepseek_url = "https://api.deepseek.com/v1/chat/completions" 
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    payload = {
        "model": "deepseek-coder",
        "messages": [
            {"role": "system", "content": "You are an expert in Python Selenium automation."},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(deepseek_url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            code_block = result['choices'][0]['message']['content']
            code_clean = code_block.replace("```python", "").replace("```", "").strip()
            return jsonify({"code": code_clean})
        else:
            return jsonify({"error": f"DeepSeek Error: {response.text}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)