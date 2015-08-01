FROM python:3

COPY asiline.py /usr/src/app/
WORKDIR /usr/src/app

ENTRYPOINT [ "python", "./asiline.py" ]


