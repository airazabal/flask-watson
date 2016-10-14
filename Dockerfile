FROM python:2.7
MAINTAINER Haad Khan "haad@cerebri.com"
COPY . /server
WORKDIR /server
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["server.py"]
