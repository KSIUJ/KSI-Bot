# 🆗Bot 
A bot written for the Computer Science server on Jagiellonian University, but could also be easily modified for other purposes.


# Installation

Clone the repository to your machine
```sh
git clone https://github.com/OK-bot-team/uj-discord-bot.git
```
or using ssh
```sh
git clone git@github.com:OK-bot-team/uj-discord-bot.git
```

Modify .env file and paste your Discord API token and application ID which can be found in the [Discord developer portal](https://discord.com/developers/applications)
Your token and application ID should be in the .env file in format seen below:
```
DISCORD_TOKEN=<your token should be here>
APP_ID=<your app id should be here>
```

## Python app route
Install depedendencies 
```
pip install -r requirements.txt
```
start the application
```
python3 start.py
```

## Docker route

You need to have [Docker](https://docs.docker.com/get-docker/) software installed

navigate to the okbot root repository (where start.py is located)
```
docker-compose up
```

done, there should be 2 containers running, 1 for the database and second for the bot python application.
