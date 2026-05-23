FROM python:3.11-slim
LABEL authors="vanysis"
WORKDIR /app
# установка зовнішніх бібліотек
RUN pip install numpy numba
COPY main.py .
CMD ["python", "main.py"]