FROM ubuntu:16.04

WORKDIR /vip_bot
RUN echo "Asia/Tehraffnss"
RUN apt-get update -y;apt-get install -y python python3.5 python3-pip \
		python-pip tzdata libxml2 apt-utils sqlite3 build-essential;
RUN pip3 install --upgrade pip
RUN echo "Asia/Tehran" > /etc/timezone
ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
RUN echo 1
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./
CMD ["python3.5", "bankofficer/bot/accountofficer_bot.py"]
ENV PYTHONPATH /vip_bot

