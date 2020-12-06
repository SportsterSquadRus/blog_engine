FROM python:3

RUN mkdir -p /usr/src/blog_engine

WORKDIR /usr/src/blog_engine

COPY . /usr/src/blog_engine
RUN pip install --no-cache-dir -r /usr/src/blog_engine/requirements.txt

EXPOSE 8000
