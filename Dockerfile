FROM python:3

ENV TZ=America/New_York

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:5000"]