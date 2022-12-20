FROM gorialis/discord.py:minimal

WORKDIR /ok-bot--

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "start.py"]