FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

#ADD . /app

WORKDIR /app
COPY . .

# RUN uv build
RUN apt-get -y update
RUN apt-get -y install git

# RUN uv sync --locked
RUN uv sync

CMD ["uv", "run", "vgdb_efgi.py"]