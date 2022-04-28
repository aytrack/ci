FROM registry-mirror.pingcap.net/library/python:3.8
ADD . /root/
RUN chmod +x /root/tcctl
RUN pip3 install -r /root/sync-version/requirements.txt