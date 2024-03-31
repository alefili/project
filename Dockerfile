FROM python:3.12
# Instalez dependinte
RUN apt-get update && apt-get install build-essential graphviz graphviz-dev --assume-yes
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip install flask
# Adaug cod
RUN mkdir /project
ADD project /project
WORKDIR /project
EXPOSE 8000
ENTRYPOINT ["./docker_entrypoint.sh"]
#ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]