FROM ubuntu:18.04

MAINTAINER zh_l "luzonghaoa@gmail.com"

RUN apt-get update -y && \
apt-get install -y python3-pip python3-dev

RUN apt-get install -y postgresql postgresql-contrib

RUN postgres -c "createdb coin_panel_test"

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

CMD [ "Pipeline/main.py",  "&" ]
CMD [ "Services/app.py"]