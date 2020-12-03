FROM python:3.7
ARG PIP_INDEX_URL
WORKDIR /app
EXPOSE 8000
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn","server:app","--host","0.0.0.0","--port","8000"]