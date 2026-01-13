
FROM python:3.9


WORKDIR /code


# COPY ./requirements.txt /code/requirements.txt

COPY ./src/app /code/app

RUN uv sync


CMD ["fastapi", "run", "app/main.py", "--port", "80"]