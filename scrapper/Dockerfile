FROM python:3.8.10
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U flask-cors

#run im bash mode
CMD ["python", "app.py"]