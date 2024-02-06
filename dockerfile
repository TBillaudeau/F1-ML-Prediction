FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y

COPY Models/ Models/
COPY streamlit/ .

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501"]