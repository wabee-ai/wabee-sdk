.PHONY: build

build:
	@echo "Building..."
	@./scripts/generate_protos.sh
	poetry build