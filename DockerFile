FROM python:3.10.7-slim-bullseye

WORKDIR /usr/src/app 

COPY requirements.txt ./ 
RUN pip3 install --no-cache-dir -r requirements.txt 

COPY keep_alive.py ./
COPY gamesrvbot.py ./ 

CMD [ "python", "./gamesrvbot.py" ] 