import os.path
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import urllib.parse

# app = Flask(__name__)
app = Flask(__name__, template_folder='templates', static_folder='static')



def get_chrome_profile_path():
    if os.name == 'nt': #windows
        base_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
    elif os.name == 'posix':  # macOS/Linux
        base_path = os.path.join(str(Path.home()), '.config', 'google-chrome')
    else:
        raise OSError("Sistema operativo no soportado")

    default_profile = os.path.join(base_path, 'Default')
    if os.path.exists(base_path):
        return  default_profile

    for item in os.listdir(base_path):
        if item.startswith('Profile'):
            return  os.path.join(base_path, item)

    return base_path



# Configuración
WHATSAPP_WEB_URL = "https://web.whatsapp.com/" #Api_whatsapp_web
GROUP_LINK = "https://chat.whatsapp.com/FZR1QblgSn7KBCTArRrMLf"  # Tu enlace de grupo
#CHROME_PROFILE_PATH = "C:\\Users\\AnalistaProgramadorB\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
CHROME_PROFILE_PATH = get_chrome_profile_path()
MESSAGE = f"¡Únete a nuestro grupo! {GROUP_LINK}"  # Mensaje personalizable
COUNTRY_CODE = "502"  # Código para Guatemala



@app.route('/')
def home():
    return render_template('formulario.html')

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
    chrome_options.add_argument("--disable-infobars")
    return webdriver.Chrome(options=chrome_options)


def send_whatsapp_message(driver, phone_number, message):
    try:
        # Abrir chat directo con el número
        formatted_num = f"{COUNTRY_CODE}{phone_number.lstrip('0')}"
        chat_url = f"https://web.whatsapp.com/send?phone={formatted_num}&text={urllib.parse.quote(message)}"
        driver.get(chat_url)

        # Esperar a que cargue el chat
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        time.sleep(3)  # Espera adicional

        # Enviar mensaje
        input_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        input_box.send_keys(Keys.ENTER)
        time.sleep(2)

        return True
    except Exception as e:
        print(f"Error enviando mensaje a {phone_number}: {str(e)}")
        return False


@app.route('/send_invitation', methods=['POST'])
def send_invitation():
    data = request.json
    raw_numbers = data.get('numbers', [])

    if not raw_numbers:
        return jsonify({"error": "Se requieren números en formato: {'numbers': ['12345678']}"}), 400

        # Validar números (8 dígitos sin código de país)
    validated_numbers = []
    for num in raw_numbers:
        clean_num = ''.join(c for c in str(num) if c.isdigit())
        if len(clean_num) == 8:
            validated_numbers.append(clean_num)
        else:
            print(f"Número inválido omitido: {num}")

    if not validated_numbers:
        return jsonify({"error": "Ningún número válido proporcionado (deben ser 8 dígitos)"}), 400

    driver = init_driver()
    try:
        # Iniciar WhatsApp Web
        driver.get(WHATSAPP_WEB_URL)
        time.sleep(15)  # Tiempo para escanear QR (solo primera vez)

        results = {}
        for number in validated_numbers:
            success = send_whatsapp_message(driver, number, MESSAGE)
            results[number] = "success" if success else "failed"
            time.sleep(3)

        return jsonify({
            "status": "completed",
            "results": results,
            "message": f"Procesados {len(validated_numbers)} números"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        driver.quit()


@app.route('/')
def serve_form():
    return send_from_directory('static', 'templates/formulario.html')

if __name__ == '__main__':
    app.run(debug=True)
