FROM python:3.11

WORKDIR /erpigram

COPY ./requirements/prod.txt /erpigram/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /erpigram/requirements.txt
COPY ./src /erpigram/src
COPY ./static /erpigram/static
COPY ./app.py /erpigram/app.py
COPY ./main.py /erpigram/main.py
COPY ./config.py /erpigram/config.py
# VOLUME ./ergram.sqlite /erpigram/ergram.sqlite  TODO: fix

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
# CMD ["python", "main.py"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
