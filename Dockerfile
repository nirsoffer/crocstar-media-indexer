FROM mongo:4.2.5
RUN apt-get update && apt-get install -y \
  python3 \
  exiftool \
  python3-pip
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
RUN mkdir /Nir
COPY ./mongo_client.py /Nir
