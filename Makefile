

lint:
	uv run ruff check --fix src/ tests/
	uv run ruff format src/ tests/


help:
	@echo "FirstData - 开发命令"
	@echo "========================================"
	@echo ""
	@echo "代码质量 / Code Quality:"
	@echo "  make lint           运行代码检查和自动修复 (ruff)"
	@echo ""
	@echo "项目说明 / About:"
	@echo "  FirstData 是一个全球权威数据源知识库"
	@echo "  提供结构化的元数据和智能 MCP 服务"
	@echo ""
	@echo "更多信息请查看 README.md"
