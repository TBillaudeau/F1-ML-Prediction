FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y

COPY data/ data/
COPY Models/ Models/
COPY streamlit/ streamlit/

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "streamlit/app.py", "--server.port=8501"]