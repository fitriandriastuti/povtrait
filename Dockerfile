FROM python:3.9

WORKDIR /povtrait-app

COPY requirements.txt .

RUN pip install -r requirements.txt

#COPY ./app ./app
COPY . .

CMD ["streamlit", "run","Dashboard.py"]




