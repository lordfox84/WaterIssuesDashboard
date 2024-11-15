from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import json
import time
from threading import Thread

app = Flask(__name__)

# Funkce pro získání dat
def fetch_data():
    url = 'https://www.pvk.cz/aktuality/havarie/#'
    response = requests.get(url)
    data = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('div', class_='havarie sortable')
        
        if table:
            rows = table.find_all('div', class_='hrow')
            headers = [col.get_text(strip=True) for col in rows[0].find_all('div', class_='hcol')]

            for row in rows[1:]:
                columns = row.find_all('div', class_='hcol')
                if columns:
                    row_values = [col.get_text(strip=True) for col in columns]
                    if any("Praha 2" in value for value in row_values):
                        row_dict = dict(zip(headers, row_values))
                        data.append(row_dict)
    return data

# Funkce pro získání aktuálních dat a aktualizaci každou minutu
@app.route('/')
def index():
    data = fetch_data()

    if not data:
        data = [{'message': 'Žádná data k zobrazení.'}]


    return render_template('index.html', data=data)

# Funkce pro pravidelnou aktualizaci
def update_data():
    while True:
        time.sleep(60)  # Čekání 1 minutu
        print("Aktualizuji data...")
        fetch_data()

if __name__ == '__main__':
    # Spuštění aktualizačního vlákna
    thread = Thread(target=update_data)
    thread.daemon = True  # Toto vlákno bude ukončeno při ukončení aplikace
    thread.start()
    
    # Spuštění webové aplikace
    app.run(debug=True, host='0.0.0.0', port=5000)
