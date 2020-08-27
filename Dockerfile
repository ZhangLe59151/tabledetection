FROM ubuntu:16.04
MAINTAINER zhangle "zhanglenus@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev && \
    apt-get install -y libgl1-mesa-glx && \
    pip3 install --upgrade pip

COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN pip3 install -r requirements.txt
COPY . /
ENTRYPOINT ["python3"]
CMD ["data/voc2coco.py"]  