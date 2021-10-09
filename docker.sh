#!/bin/bash
sudo docker build -t king-bot:dev .
sudo rm kingbot.tar
sudo docker save -o kingbot.tar king-bot
sudo chmod -R 777 kingbot.tar

