import contextlib
import os

from langfuse import get_client as get_langfuse_client
from langfuse import observe, propagate_attributes

from user_context import get_masked_token
from utils import load_all_datasources


@observe(name="filter-by-criteria")
def tool_filter_sources_by_criteria(
    geographic_scope: str | None = None,
    domain: str | None = None,
    has_api: bool | None = None,
    update_frequency: str | None = None,
    authority_level: str | None = None,
) -> list[dict]:
    """条件筛选"""
    # 传播用户ID到所有子观察
    masked_token = get_masked_token()
    with propagate_attributes(user_id=masked_token) if masked_token else contextlib.nullcontext():
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

        # 添加追踪元数据
        if os.getenv("LANGFUSE_ENABLED", "false").lower() == "true":
            langfuse = get_langfuse_client()
            langfuse.update_current_span(
                input={
                    "geographic_scope": geographic_scope,
                    "domain": domain,
                    "has_api": has_api,
                    "update_frequency": update_frequency,
                    "authority_level": authority_level,
                },
                output={"count": len(results), "results": results},
                metadata={
                    "total_datasources": len(all_sources),
                    "filtered_count": len(results),
                    "filter_criteria_count": sum(
                        [
                            geographic_scope is not None,
                            domain is not None,
                            has_api is not None,
                            update_frequency is not None,
                            authority_level is not None,
                        ]
                    ),
                },
            )

        return results
