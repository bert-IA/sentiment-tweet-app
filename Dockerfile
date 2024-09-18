FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader wordnet omw-1.4

COPY ./app /app/app

EXPOSE 8080

ENV PORT=8080
ENV HOST=0.0.0.0

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]