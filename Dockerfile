FROM python:3.8
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN mkdir /ru_wiki_tables
RUN mkdir /ru_wiki_tables/titles
RUN mkdir /ru_wiki_tables/datasets
ADD . /ru_wiki_tables
WORKDIR /ru_wiki_tables
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]