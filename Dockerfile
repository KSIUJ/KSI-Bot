FROM gorialis/discord.py:minimal

WORKDIR /okbot

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "start.py"]