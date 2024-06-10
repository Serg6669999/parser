# parser
# install dependencies

    pip3 install -r requirements.txt

# create .env file
    see example .env.example

#start database

    docker compose up -d --build

# save file data to the DB
    python run.py save test_prog1.csv

# get data
    python run.py get