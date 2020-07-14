From python:3.6.6

WORKDIR /opt/install
COPY requirements.txt /opt/install/requirements.txt
RUN pip install -r requirements.txt

