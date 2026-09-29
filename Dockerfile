#lightweight version of python image
FROM python:3.11

#stop python from creating .psy(messy cache) file and no need to show unbuffered loggin(logs/error insdie the terminal) info
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
#Install dependenciyes or module
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

#download spaCy model so it will joined with the image cleanely
RUN python -m spacy download en_core_web_lg

#copy the project itself
COPY . .

EXPOSE 8000
