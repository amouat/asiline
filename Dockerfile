FROM python:3

COPY asiline.py /usr/src/app/

ENTRYPOINT [ "python", "/usr/src/app/asiline.py" ]


