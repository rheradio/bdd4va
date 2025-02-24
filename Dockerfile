FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test \
    && apt-get update && apt-get install -y \
    gcc-9 \
    libstdc++6

WORKDIR /home
RUN git clone https://github.com/rheradio/bdd4va \
    && python3 -mpip install ./bdd4va

COPY example.py .
ENTRYPOINT ["python3", "example.py"]