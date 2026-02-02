import contextlib
import os

from langfuse import get_client as get_langfuse_client
from langfuse import observe, propagate_attributes

from user_context import get_masked_token
from utils import load_all_datasources


@observe(name="get-source-details")
def tool_get_source_details(source_ids: list[str], fields: list[str] | None = None) -> list[dict]:
    """获取详细信息"""
    # 传播用户ID到所有子观察
    masked_token = get_masked_token()
    with propagate_attributes(user_id=masked_token) if masked_token else contextlib.nullcontext():
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

        # 添加追踪元数据
        if os.getenv("LANGFUSE_ENABLED", "false").lower() == "true":
            langfuse = get_langfuse_client()
            langfuse.update_current_span(
                input={"source_ids": source_ids, "fields": fields},
                output={"count": len(results), "results": results},
                metadata={
                    "requested_count": len(source_ids),
                    "found_count": sum(1 for r in results if "error" not in r),
                    "not_found_count": sum(1 for r in results if "error" in r),
                    "fields_requested": fields if fields else ["all"],
                },
            )

        return results
