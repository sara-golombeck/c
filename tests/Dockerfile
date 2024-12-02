# בחר תמונה שמכילה Python
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "--maxfail=5", "--disable-warnings"]
