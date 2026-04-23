FROM ghcr.io/astral-sh/uv@sha256:b6007a73910218ab068c7a9a7fb91e68f97017ab486af0ecd00403561a64e573
WORKDIR /opt

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_INSTALL_DIR=/python UV_PYTHON_PREFERENCE=only-managed

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev
RUN uv sync --frozen --no-install-project --dev

COPY . .

RUN uv sync --frozen --dev

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "./src/python_api/main.py"]
