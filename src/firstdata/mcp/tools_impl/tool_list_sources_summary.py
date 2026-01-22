from utils import load_all_datasources


def tool_list_sources_summary(
    country: str | None = None, domain: str | None = None, limit: int = 50
) -> list[dict]:
    """列出数据源概要"""
    all_sources = load_all_datasources()
    results = []

    for ds in all_sources:
        # 过滤国家
        if country:
            ds_country = ds.get("country") or ""
            geo_scope = ds.get("geographic_scope", "")

            country_match = (ds_country and country.upper() in ds_country.upper()) or (
                country.lower() == "global" and "global" in geo_scope.lower()
            )
            if not country_match:
                continue

        # 过滤领域
        if domain:
            domains = ds.get("domains", [])
            if not any(domain.lower() in d.lower() for d in domains):
                continue

        results.append(
            {
                "id": ds["id"],
                "name": ds["name"],
                "country": ds.get("country", ""),
                "domains": ds.get("domains", []),
                "authority_level": ds.get("authority_level", ""),
                "file_path": ds.get("file_path", ""),
            }
        )

        if len(results) >= limit:
            break

    return results
