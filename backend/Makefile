# Backend Makefile — run from backend/ with uv
# .venv is created here (backend/.venv) so your editor can use it

.PHONY: venv install run dev lint clean

# Create .venv in backend/ (current directory) so IDE resolves it
venv:
	uv venv .venv

# Install/sync dependencies into .venv
install: venv
	uv sync

# Run the API server (uses .venv via uv run)
run:
	uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Alias for run
dev: run

# Optional: lint (add ruff or similar to dev-dependencies to use)
lint:
	uv run ruff check . || true

clean:
	rm -rf .venv
	rm -f uv.lock
