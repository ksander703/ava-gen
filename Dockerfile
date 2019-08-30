FROM python:3.4
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN apt-get install gcc
RUN pip install flask==0.10.1 && pip install uwsgi && pip install requests && pip install redis
WORKDIR /app
COPY app /app
COPY cmd.sh /
EXPOSE 9090 9191
user uwsgi
CMD /cmd.sh
