FROM python:3.9-alpine

COPY requirements.txt /opt/src/requirements.txt
COPY src/tfsum.py /opt/tfsum.py

RUN apk add --no-cache \
    python3-dev~=3.9 \
    python3~=3.9 \
    py3-pip~=20.3.4 \
    gcc~=10.3.1 \
    musl-dev~=1.2.2 \
    openssl-dev~=1.1.1 \
    libffi-dev~=3.4.2 \
    make~=4.3 \
  && pip3 install --no-cache-dir --requirement /opt/src/requirements.txt \
  && apk del gcc python3-dev musl-dev openssl-dev libffi-dev make

CMD ["python", "/opt/tfsum.py"]
