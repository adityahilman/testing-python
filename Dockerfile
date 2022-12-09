FROM python:alpine

RUN pip3 install boto3 flask slack_sdk
COPY ./app /app
CMD ["python3", "./app/main.py"]