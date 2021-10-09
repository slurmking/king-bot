#!/bin/bash
sudo docker build -t king-bot:latest .
sudo docker push slurmking/king-bot


sudo docker run --name king-bot-dev -it king-bot:latest king.py

