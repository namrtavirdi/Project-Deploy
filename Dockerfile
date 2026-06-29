FROM python:3.11

WORKDIR /app

COPY src/ /app/

RUN pip install --no-cache-dir \
    tensorflow \
    customtkinter \
    numpy \
    pillow \
    opencv-python

CMD ["python", "app.py"]