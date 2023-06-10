# https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry

FROM python:3.11 AS requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

###################

FROM python:3.11 AS prod


RUN adduser worker
USER worker
WORKDIR /home/worker

COPY --chown=worker:worker --from=requirements-stage /tmp/requirements.txt ./requirements.txt
RUN pip install --user --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker ./src ./src

EXPOSE 8082
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8082", "--workers", "10"]