FROM thrift as code_generation
COPY schema /data
RUN thrift -o /data --gen py /data/ril.thrift



FROM python:3.7-slim
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=0 /data .
COPY server/ .


CMD [ "python", "./server.py" ]