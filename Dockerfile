FROM mongo:4.2.5
RUN apt-get update && apt-get install -y \
  python3 \
  ffmpeg \
  exiftool \
  python \
  python-pip \
  python3-pip
COPY requirements.txt /tmp
COPY requirements-python2.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
RUN pip install -r /tmp/requirements-python2.txt
RUN mkdir /Nir
COPY ./mongo_client.py /Nir
