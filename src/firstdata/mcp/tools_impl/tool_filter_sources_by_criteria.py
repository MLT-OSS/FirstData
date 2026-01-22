from utils import load_all_datasources


def tool_filter_sources_by_criteria(
    geographic_scope: str | None = None,
    domain: str | None = None,
    has_api: bool | None = None,
    update_frequency: str | None = None,
    authority_level: str | None = None,
) -> list[dict]:
    """条件筛选"""
    all_sources = load_all_datasources()
    results = []

    for ds in all_sources:
        # 地理范围
        if geographic_scope:
            ds_country = ds.get("country") or ""
            geo_scope = ds.get("geographic_scope", "") or ""

            geo_match = (
                ds_country and geographic_scope.upper() in ds_country.upper()
            ) or geographic_scope.lower() in geo_scope.lower()
            if not geo_match:
                continue

        # 领域过滤
        if domain:
            domains = ds.get("domains", [])
            if not any(domain.lower() in d.lower() for d in domains):
                continue

        # API需求
        if has_api is not None:
            has_api_access = ds.get("api_url") is not None
            if has_api_access != has_api:
                continue

        # 更新频率
        if update_frequency:
            freq = ds.get("update_frequency", "")
            if update_frequency.lower() not in freq.lower():
                continue

        # 权威级别筛选
        if authority_level:
            ds_authority = ds.get("authority_level", "")
            if authority_level.lower() not in ds_authority.lower():
                continue

        results.append(
            {
                "id": ds["id"],
                "name": ds["name"],
                "country": ds.get("country", ""),
                "domains": ds.get("domains", []),
                "has_api": ds.get("api_url") is not None,
                "authority_level": ds.get("authority_level", ""),
                "file_path": ds.get("file_path", ""),
            }
        )

    return results
