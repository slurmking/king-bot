FROM python:3.8
 
WORKDIR /kingbot
COPY /bot /kingbot
RUN pip install -r requirements.txt
VOLUME /kingbot/setup
ENTRYPOINT ["python"]
CMD ["king.py"]
