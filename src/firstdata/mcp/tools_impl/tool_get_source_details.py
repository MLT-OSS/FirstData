from utils import load_all_datasources


def tool_get_source_details(source_ids: list[str], fields: list[str] | None = None) -> list[dict]:
    """获取详细信息"""
    if fields is None:
        fields = ["all"]
    all_sources = load_all_datasources()
    results = []

    for source_id in source_ids:
        ds = next((s for s in all_sources if s["id"] == source_id), None)
        if not ds:
            results.append({"id": source_id, "error": "Not found"})
            continue

        if "all" in fields:
            results.append(ds)
        else:
            filtered = {"id": ds["id"], "name": ds["name"]}
            for field in fields:
                if field in ds:
                    filtered[field] = ds[field]
            results.append(filtered)

    return results
