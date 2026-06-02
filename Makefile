.PHONY: install dev docker-up docker-down index test

install:
	python -m pip install -r requirements.txt

docker-up:
	docker compose up -d
	@echo "PostgreSQL démarré sur localhost:5432"

docker-down:
	docker compose down

dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

index:
	python -c "from src.rag.indexer import index_knowledge_base; n = index_knowledge_base(force=True); print(f'{n} chunks indexés')"

test-generate:
	@echo "Test de génération CCTP lot électricité..."
	curl -s -X POST http://localhost:8000/api/v1/projects \
		-H "Content-Type: application/json" \
		-d '{"name":"Projet test","type_projet":"neuf","usage":"logement","zone_climatique":"H1a","zone_sismique":"1","pmr":false}' \
		| python -m json.tool
