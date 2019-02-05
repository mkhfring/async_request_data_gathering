FROM ubuntu:16.04

WORKDIR /vip_bot
RUN mkdir -p /home/vipbot
RUN echo "Asia/Tehraffnss"
RUN apt-get update -y;apt-get install -y python python3.5 python3-pip \
		python-pip tzdata libxml2 apt-utils sqlite3 build-essential;
RUN pip install --upgrade pip
RUN echo "Asia/Tehran" > /etc/timezone
ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
COPY ibm_db-2.0.7.tar.gz /vip_bot
RUN tar -zxvf ibm_db-2.0.7.tar.gz
RUN pip3 install -e ibm_db-2.0.7
RUN echo 1
COPY ./requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY ./ ./
CMD ["python3.5", "bankofficer/bot/accountofficer_bot.py"]
ENV PYTHONPATH /vip_bot

