FROM python:3.8-buster
ADD aggregator.py /
RUN pip install mysql-connector-python && \
    pip install pandas && \
    pip install pika && \
    pip install numpy
CMD ["python3", "-u", "./aggregator.py"]