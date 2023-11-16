# 🆗Bot 
A bot written for the Computer Science server on Jagiellonian University, but could also be easily modified for other purposes.


# Installation

Clone the repository to your machine
```sh
git clone git@github.com:KSIUJ/KSI-Bot.git
```

Modify .env file and paste your Discord API token and application ID which can be found in the [Discord developer portal](https://discord.com/developers/applications)
Your token and application ID should be in the .env file in format seen below:
```
DISCORD_TOKEN=EXAMPLETOKEN404F83FDSS
APP_ID=1111111101111101
```

## Python app route
You need to have Python 3.11+ installed

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
