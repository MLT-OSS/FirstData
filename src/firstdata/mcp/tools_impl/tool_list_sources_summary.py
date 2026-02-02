import contextlib
import os

from langfuse import get_client as get_langfuse_client
from langfuse import observe, propagate_attributes

from user_context import get_masked_token
from utils import load_all_datasources


@observe(name="list-sources-summary")
def tool_list_sources_summary(
    country: str | None = None, domain: str | None = None, limit: int = 50
) -> list[dict]:
    """列出数据源概要"""
    # 传播用户ID到所有子观察
    masked_token = get_masked_token()
    print(f"[DEBUG] tool_list_sources_summary - masked_token: {masked_token}")
    with propagate_attributes(user_id=masked_token) if masked_token else contextlib.nullcontext():
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

        # 添加追踪元数据
        if os.getenv("LANGFUSE_ENABLED", "false").lower() == "true":
            langfuse = get_langfuse_client()
            langfuse.update_current_span(
                input={"country": country, "domain": domain, "limit": limit},
                output={"count": len(results), "results": results},
                metadata={
                    "total_datasources": len(all_sources),
                    "filtered_count": len(results),
                },
            )

        return results
