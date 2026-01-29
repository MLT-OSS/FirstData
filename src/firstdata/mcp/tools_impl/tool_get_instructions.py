"""
数据源访问指令生成工具

为访问指定数据源生成详细的URL访问操作指令
"""

import asyncio
import os
import time

import httpx

from .tool_get_source_details import tool_get_source_details


def _aggregate_instructions(completed_tasks: dict) -> list[dict]:
    """聚合并按 URL 分组指令"""
    # 按 URL 分组
    url_groups = {}
    for task_result in completed_tasks.values():
        url = task_result["url"]
        if task_result.get("instructions"):
            if url not in url_groups:
                url_groups[url] = []
            for inst in task_result["instructions"]:
                url_groups[url].append({
                    "instruction": inst.get("instruction", ""),
                    "score": inst.get("score", 0),
                })

    # 转换为列表格式，按 URL 排序
    result = []
    for url in sorted(url_groups.keys()):
        result.append({
            "url": url,
            "instructions": url_groups[url]
        })

    return result


async def tool_datasource_get_instructions(source_id: str, operation: str, top_k: int = 3) -> dict:
    """
    为访问指定数据源生成详细的URL访问操作指令

    该工具结合了数据源元数据和指令生成API，返回具体的网站操作步骤。

    Args:
        source_id: 数据源ID，从其他MCP工具获取（如 'hkex'、'china-pbc'）
        operation: 具体操作描述（如 '下载智谱AI的招股书'、'查询M2货币供应量'）
        top_k: 返回指令数量，默认3条（范围: 1-5）

    Returns:
        dict: 包含操作指令和相关信息的字典

    使用场景:
        1. 先获取到具体使用什么数据源，通过 datasource_search_llm_agent 等检索方法获取到数据源ID
        2. 再用本工具获取该数据源的具体操作指令
    """
    try:
        # 1. 获取数据源详情
        sources = tool_get_source_details([source_id])
        if not sources or "error" in sources[0]:
            return {"error": f"数据源 {source_id} 不存在"}

        source = sources[0]

        # 2. 收集所有URL（去重）
        urls = list(dict.fromkeys(
            url for field in ["website", "data_url", "api_url"]
            if (url := source.get(field))
        ))

        if not urls:
            return {"error": f"数据源 {source_id} 没有可用的URL"}

        print(f"[INFO] Processing {len(urls)} URLs for {source_id}")

        # 3. 准备API请求
        api_base = os.getenv(
            "INSTRUCTION_API_URL",
            "https://mingjing.mininglamp.com/api/mano-plan/instruction/v1"
        ).rstrip("/match").rstrip("/")

        async with httpx.AsyncClient(timeout=120.0) as client:
            # 4. 并发创建异步任务
            async def create_task(url: str):
                response = await client.post(
                    f"{api_base}/match_async",
                    json={
                        "category": "查询",
                        "domain": "",
                        "resource_path": url,
                        "operation": operation,
                        "top_k": top_k,
                    }
                )
                if response.status_code == 200 and (result := response.json()).get("success"):
                    print(f"[INFO] Task created for {url}")
                    return {"task_id": result["task_id"], "url": url}
                return None

            task_metadata = [t for t in await asyncio.gather(*[create_task(url) for url in urls]) if t]

            if not task_metadata:
                return {"error": "所有URL的任务创建均失败"}

            # 5. 并发轮询任务状态
            completed_tasks = {}
            start_time = time.time()

            while len(completed_tasks) < len(task_metadata):
                if time.time() - start_time > 90:
                    break  # 超时

                # 并发查询所有未完成任务的状态
                async def check_status(meta: dict):
                    task_id = meta["task_id"]
                    if task_id in completed_tasks:
                        return None

                    status_resp = await client.get(f"{api_base}/match_status/{task_id}")
                    if status_resp.status_code != 200:
                        return None

                    status_data = status_resp.json()
                    state = status_data.get("state")

                    if state == "SUCCESS":
                        print(f"[INFO] Task {task_id[:8]} completed")
                        return (task_id, {"url": meta["url"], "instructions": status_data.get("result", [])})
                    elif state == "FAILURE":
                        print(f"[WARNING] Task {task_id[:8]} failed")
                        return (task_id, {"url": meta["url"], "instructions": []})
                    return None

                results = await asyncio.gather(*[check_status(meta) for meta in task_metadata])
                for item in results:
                    if item:
                        task_id, task_data = item
                        completed_tasks[task_id] = task_data

                await asyncio.sleep(2)

            # 6. 聚合并返回结果
            urls = _aggregate_instructions(completed_tasks)

            result = {"source_id": source_id, "urls": urls}

            # 添加明确的状态信息
            if len(completed_tasks) < len(task_metadata):
                result["warning"] = f"部分任务超时，仅返回 {len(completed_tasks)}/{len(task_metadata)} 个结果"

            # 如果没有找到任何指令，提供明确说明
            total_instructions = sum(len(url_data["instructions"]) for url_data in urls)
            if not urls:
                if not completed_tasks:
                    result["message"] = "所有检索任务超时或失败，未能获取任何操作指令"
                else:
                    result["message"] = (
                        f"在数据源 {source_id} 中未找到与操作 '{operation}' 匹配的指令。"
                        "建议尝试更换关键词描述"
                    )

            print(f"[INFO] Completed: {total_instructions} instructions from {len(urls)} URLs")
            return result

    except httpx.TimeoutException:
        return {"error": "指令API调用超时（120秒）"}
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"工具执行失败: {e!s}"}
