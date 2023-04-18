FROM python:3.11-alpine3.17

ARG BUILD_ENV

ENV BUILD_ENV=${BUILD_ENV} \
  POETRY_VERSION=1.4.0

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app/
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$BUILD_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

ADD curator /app/curator/
COPY main.py /app/

CMD ["poetry", "run", "python", "main.py"]