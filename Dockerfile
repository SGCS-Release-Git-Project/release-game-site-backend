FROM python:3.13.0
WORKDIR /backend
ADD . .
#ENV OPENAI_API_KEY=******************
#ENV AZURE_OPENAI_API_KEY=********************
#ENV AZURE_OPENAI_ENDPOINT=*************************
RUN apt-get update && apt-get -y upgrade
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8011
CMD ["python", "main.py"]