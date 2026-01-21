"""
数据源访问指令生成工具

为访问指定数据源生成详细的URL访问操作指令
"""

import asyncio
import json
import os
import time

import httpx

from .tool_get_source_details import tool_get_source_details


async def tool_datasource_get_instructions(source_id: str, operation: str, top_k: int = 3) -> str:  # noqa: PLR0915
    """
    为访问指定数据源生成详细的URL访问操作指令

    该工具结合了数据源元数据和指令生成API，返回具体的网站操作步骤。

    Args:
        source_id: 数据源ID，从其他MCP工具获取（如 'hkex-news'、'china-pbc'）
        operation: 具体操作描述（如 '下载智谱AI的招股书'、'查询M2货币供应量'）
        top_k: 返回指令数量，默认3条（范围: 1-5）

    Returns:
        JSON字符串，包含操作指令和相关信息

    使用场景:
        1. 先获取到具体使用什么数据源，通过 datasource_search_llm_agent 等检索方法获取到数据源ID
        2. 再用本工具获取该数据源的具体操作指令
    """
    try:
        # 1. 获取数据源详情
        sources = tool_get_source_details([source_id])
        if not sources or "error" in sources[0]:
            return json.dumps(
                {"error": f"数据源 {source_id} 不存在", "success": False},
                ensure_ascii=False,
                indent=2,
            )

        source = sources[0]

        # 2. 收集数据源中的所有URL（去重）
        urls_to_process = []
        seen_urls = set()

        for url_field in ["website", "data_url", "api_url"]:
            url = source.get(url_field)
            if url and url not in seen_urls:
                urls_to_process.append(url)
                seen_urls.add(url)

        if not urls_to_process:
            return json.dumps(
                {"error": f"数据源 {source_id} 没有可用的URL", "success": False},
                ensure_ascii=False,
                indent=2,
            )

        print(f"[INFO] Processing {len(urls_to_process)} unique URLs for source: {source_id}")

        # 3. 准备指令API请求
        instruction_api_base = (
            os.getenv(
                "INSTRUCTION_API_URL",
                "https://mingjing.mininglamp.com/api/mano-plan/instruction/v1",
            )
            .rstrip("/match")
            .rstrip("/")
        )  # 移除可能的 /match 后缀

        # 4. 异步调用指令API - 为每个URL创建任务
        async with httpx.AsyncClient(timeout=120.0) as client:
            # 4.1 为每个URL创建异步任务
            task_ids = []
            task_metadata = []

            for idx, resource_url in enumerate(urls_to_process):
                request_data = {
                    "category": "查询",
                    "domain": "",  # 留空让API自动识别
                    "resource_path": resource_url,
                    "operation": operation,
                    "top_k": top_k,
                }

                print(f"[INFO] Creating task {idx + 1}/{len(urls_to_process)}: {resource_url}")

                response = await client.post(
                    f"{instruction_api_base}/match_async", json=request_data
                )

                if response.status_code != 200:
                    print(
                        f"[WARNING] Failed to create task for URL {resource_url}: HTTP {response.status_code}"
                    )
                    continue

                result = response.json()
                if not result.get("success"):
                    print(
                        f"[WARNING] Failed to create task for URL {resource_url}: {result.get('message', '未知错误')}"
                    )
                    continue

                task_id = result.get("task_id")
                task_ids.append(task_id)
                task_metadata.append({"task_id": task_id, "url": resource_url})
                print(f"[INFO] Task created: {task_id}")

            if not task_ids:
                return json.dumps(
                    {"error": "所有URL的任务创建均失败", "success": False},
                    ensure_ascii=False,
                    indent=2,
                )

            # 4.2 轮询所有任务的状态
            max_wait = 90  # 最多等待90秒（因为有多个任务）
            start_time = time.time()
            poll_interval = 2  # 每2秒轮询一次
            completed_tasks = {}

            while True:
                elapsed = time.time() - start_time

                if elapsed > max_wait:
                    # 返回已完成的任务（如果有）
                    if completed_tasks:
                        return json.dumps(
                            {
                                "success": True,
                                "data_source": {
                                    "id": source_id,
                                    "name": source.get("name"),
                                    "description": source.get("description"),
                                },
                                "results": list(completed_tasks.values()),
                                "message": f"部分任务超时，返回 {len(completed_tasks)}/{len(task_ids)} 个已完成的任务",
                                "timeout": True,
                            },
                            ensure_ascii=False,
                            indent=2,
                        )
                    else:
                        return json.dumps(
                            {
                                "error": f"所有任务超时（{max_wait}秒）",
                                "success": False,
                                "task_ids": task_ids,
                            },
                            ensure_ascii=False,
                            indent=2,
                        )

                # 检查未完成的任务
                pending_tasks = [
                    meta for meta in task_metadata if meta["task_id"] not in completed_tasks
                ]

                if not pending_tasks:
                    # 所有任务已完成
                    break

                # 轮询每个待处理的任务
                for task_meta in pending_tasks:
                    task_id = task_meta["task_id"]

                    status_resp = await client.get(f"{instruction_api_base}/match_status/{task_id}")

                    if status_resp.status_code != 200:
                        print(
                            f"[WARNING] Failed to query task {task_id[:8]}... status: HTTP {status_resp.status_code}"
                        )
                        continue

                    status_data = status_resp.json()
                    state = status_data.get("state", "UNKNOWN")

                    print(f"[INFO] Task {task_id[:8]}... state: {state} ({elapsed:.1f}s)")

                    if state == "SUCCESS":
                        # 任务成功完成
                        completed_tasks[task_id] = {
                            "url": task_meta["url"],
                            "instructions": status_data.get("result", []),
                            "message": status_data.get("message", ""),
                            "task_id": task_id,
                            "success": True,
                        }
                        print(
                            f"[INFO] Task {task_id[:8]}... completed with {len(completed_tasks[task_id]['instructions'])} instructions"
                        )

                    elif state == "FAILURE":
                        # 任务失败
                        completed_tasks[task_id] = {
                            "url": task_meta["url"],
                            "error": status_data.get("error", "未知错误"),
                            "message": status_data.get("message", ""),
                            "task_id": task_id,
                            "success": False,
                        }
                        print(
                            f"[WARNING] Task {task_id[:8]}... failed: {completed_tasks[task_id]['error']}"
                        )

                # 继续等待
                await asyncio.sleep(poll_interval)

            # 5. 返回所有完成的任务结果
            output = {
                "success": True,
                "data_source": {
                    "id": source_id,
                    "name": source.get("name"),
                    "description": source.get("description"),
                },
                "results": list(completed_tasks.values()),
                "total_urls": len(urls_to_process),
                "completed_tasks": len(completed_tasks),
                "message": f"成功处理 {len(completed_tasks)}/{len(urls_to_process)} 个URL",
            }

            print(f"[INFO] All tasks completed: {len(completed_tasks)}/{len(task_ids)} successful")
            return json.dumps(output, ensure_ascii=False, indent=2)

    except httpx.TimeoutException:
        return json.dumps(
            {"error": "指令API调用超时（120秒）", "success": False}, ensure_ascii=False, indent=2
        )
    except Exception as e:
        print(f"[ERROR] Exception in tool_datasource_get_instructions: {e}")
        import traceback

        traceback.print_exc()
        return json.dumps(
            {"error": f"工具执行失败: {e!s}", "success": False}, ensure_ascii=False, indent=2
        )
