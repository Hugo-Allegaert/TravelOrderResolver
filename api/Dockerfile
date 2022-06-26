FROM python:3.9

WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN python3 -m spacy download fr_core_news_sm
 
COPY . .
 
CMD ["uvicorn", "travelapi:app", "--host", "api", "--port", "8000"]