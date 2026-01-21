from utils import load_all_datasources


def tool_search_sources_by_keywords(
    keywords: list[str], search_fields: list[str] | None = None, limit: int = 20
) -> list[dict]:
    """关键词搜索"""
    if search_fields is None:
        search_fields = ["all"]
    all_sources = load_all_datasources()
    results = []

    for ds in all_sources:
        matched_fields = []
        score = 0

        for keyword in keywords:
            kw_lower = keyword.lower()

            # 搜索名称
            if "name" in search_fields or "all" in search_fields:
                name_en = ds.get("name", {}).get("en", "").lower()
                name_zh = ds.get("name", {}).get("zh", "").lower()
                if kw_lower in name_en or kw_lower in name_zh:
                    matched_fields.append("name")
                    score += 10

            # 搜索描述
            if "description" in search_fields or "all" in search_fields:
                desc_en = ds.get("description", {}).get("en", "").lower()
                desc_zh = ds.get("description", {}).get("zh", "").lower()
                if kw_lower in desc_en or kw_lower in desc_zh:
                    if "description" not in matched_fields:
                        matched_fields.append("description")
                    score += 5

            # 搜索标签
            if "tags" in search_fields or "all" in search_fields:
                tags = ds.get("tags", [])
                if any(kw_lower in str(tag).lower() for tag in tags):
                    if "tags" not in matched_fields:
                        matched_fields.append("tags")
                    score += 3

            # 搜索内容
            if "content" in search_fields or "all" in search_fields:
                content_en = ds.get("data_content", {}).get("en", [])
                content_zh = ds.get("data_content", {}).get("zh", [])
                all_content = " ".join(content_en + content_zh).lower()
                if kw_lower in all_content:
                    if "content" not in matched_fields:
                        matched_fields.append("content")
                    score += 2

        if matched_fields:
            results.append(
                {
                    "id": ds["id"],
                    "name": ds["name"],
                    "matched_fields": list(set(matched_fields)),
                    "match_score": score,
                    "domains": ds.get("domains", []),
                    "authority_level": ds.get("authority_level", ""),
                    "file_path": ds.get("file_path", ""),
                }
            )

    # 按得分排序
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results[:limit]
