FROM python:alpine3.17

LABEL Maintainer="Javad Naghiloo"

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
CMD ["python", "./scholar.py"]