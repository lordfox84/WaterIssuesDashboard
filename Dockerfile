# Použijeme oficiální Python base image pro ARM architekturu (pro Raspberry Pi 4)
FROM arm32v7/python:3.10-slim

# Nastavíme pracovní adresář v Docker kontejneru
WORKDIR /app

# Zkopírujeme všechny soubory z místního adresáře do Docker kontejneru
COPY . .

# Nainstalujeme všechny závislosti
RUN pip install --no-cache-dir -r requirements.txt

# Exponujeme port 5000 (Flask aplikace)
EXPOSE 5000

# Spustíme aplikaci (pokud je aplikace Flask)
CMD ["python", "aapp/app.py"]
