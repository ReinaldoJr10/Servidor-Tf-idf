FROM python:3.11-slim
LABEL authors="ReinaldoJr"

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN python montaDadosPlaylist.py

ENV PORT 5000

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["servidor.py"]