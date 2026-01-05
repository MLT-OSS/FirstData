#!/usr/bin/env python3
"""
MCP性能测试脚本
测试各个环节的耗时，找出性能瓶颈
"""

import os
import sys
import time
import json
from pathlib import Path

# 添加server.py所在目录到path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

# 导入server模块的函数
from server import (
    _load_all_datasources,
    datasource_search_agent,
    tool_list_sources_summary,
    tool_search_sources_by_keywords,
    tool_get_source_details,
    tool_filter_sources_by_criteria,
    get_anthropic_client
)


def test_datasource_loading():
    """测试数据源加载性能"""
    print("\n=== 测试1: 数据源加载性能 ===")

    start = time.time()
    datasources = _load_all_datasources()
    elapsed = time.time() - start

    print(f"✓ 加载了 {len(datasources)} 个数据源")
    print(f"✓ 耗时: {elapsed:.3f}秒")
    print(f"✓ 平均每个数据源: {elapsed/len(datasources)*1000:.2f}ms")

    return elapsed, len(datasources)


def test_tool_performance():
    """测试各个工具的执行性能"""
    print("\n=== 测试2: 工具执行性能 ===")

    results = {}

    # 测试1: list_sources_summary
    print("\n测试 list_sources_summary...")
    start = time.time()
    result = tool_list_sources_summary(country="CN", limit=50)
    elapsed = time.time() - start
    results['list_sources_summary'] = elapsed
    print(f"  ✓ 返回 {len(result)} 个结果，耗时: {elapsed:.3f}秒")

    # 测试2: search_sources_by_keywords
    print("\n测试 search_sources_by_keywords...")
    start = time.time()
    result = tool_search_sources_by_keywords(
        keywords=["monetary", "M1", "M2"],
        limit=20
    )
    elapsed = time.time() - start
    results['search_sources_by_keywords'] = elapsed
    print(f"  ✓ 返回 {len(result)} 个结果，耗时: {elapsed:.3f}秒")

    # 测试3: filter_sources_by_criteria
    print("\n测试 filter_sources_by_criteria...")
    start = time.time()
    result = tool_filter_sources_by_criteria(
        geographic_scope="China",
        has_api=True
    )
    elapsed = time.time() - start
    results['filter_sources_by_criteria'] = elapsed
    print(f"  ✓ 返回 {len(result)} 个结果，耗时: {elapsed:.3f}秒")

    # 测试4: get_source_details
    print("\n测试 get_source_details...")
    start = time.time()
    result = tool_get_source_details(["china-pbc", "china-nbs"])
    elapsed = time.time() - start
    results['get_source_details'] = elapsed
    print(f"  ✓ 返回 {len(result)} 个结果，耗时: {elapsed:.3f}秒")

    return results


def test_llm_api_latency():
    """测试LLM API的延迟"""
    print("\n=== 测试3: LLM API延迟 ===")

    try:
        client = get_anthropic_client()
        model = os.getenv("QUERY_UNDERSTANDING_MODEL", "claude-sonnet-4-5-20250929")

        # 简单的测试消息
        start = time.time()
        response = client.messages.create(
            model=model,
            max_tokens=100,
            messages=[{"role": "user", "content": "Hello"}]
        )
        elapsed = time.time() - start

        print(f"✓ 单次LLM调用耗时: {elapsed:.3f}秒")
        print(f"✓ 使用模型: {model}")

        # 检查是否使用自定义base_url
        base_url = os.getenv("ANTHROPIC_BASE_URL")
        if base_url:
            print(f"⚠ 使用自定义API网关: {base_url}")
            print(f"  （这可能影响延迟）")
        else:
            print(f"✓ 使用官方API: https://api.anthropic.com")

        return elapsed

    except Exception as e:
        print(f"✗ LLM API测试失败: {e}")
        return None


def test_agent_search(query: str, description: str):
    """测试完整的Agent搜索性能"""
    print(f"\n=== 测试Agent搜索: {description} ===")
    print(f"查询: {query}")

    # 修改server.py中的agent函数以添加详细日志
    # 这里我们直接调用并计时
    start = time.time()

    try:
        result = datasource_search_agent(query, max_iterations=10)
        elapsed = time.time() - start

        print(f"\n✓ Agent搜索完成")
        print(f"✓ 总耗时: {elapsed:.3f}秒")
        print(f"\n--- Agent返回结果 ---")
        print(result[:500] + "..." if len(result) > 500 else result)

        return elapsed

    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ Agent搜索失败: {e}")
        print(f"✗ 耗时: {elapsed:.3f}秒")
        return elapsed


def test_with_instrumented_agent(query: str):
    """使用instrumented版本测试Agent，记录每次工具调用"""
    print(f"\n=== 详细性能分析 ===")
    print(f"查询: {query}")

    from anthropic import Anthropic

    client = get_anthropic_client()
    model = os.getenv("QUERY_UNDERSTANDING_MODEL", "claude-sonnet-4-5-20250929")

    from server import AGENT_TOOLS, AGENT_SYSTEM_PROMPT, execute_tool

    messages = [{"role": "user", "content": query}]

    iteration = 0
    total_start = time.time()
    llm_times = []
    tool_times = []

    while iteration < 10:
        iteration += 1
        print(f"\n--- 迭代 {iteration} ---")

        # LLM调用计时
        llm_start = time.time()
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=AGENT_SYSTEM_PROMPT,
            tools=AGENT_TOOLS,
            messages=messages
        )
        llm_elapsed = time.time() - llm_start
        llm_times.append(llm_elapsed)
        print(f"  LLM调用耗时: {llm_elapsed:.3f}秒")

        # 检查停止原因
        if response.stop_reason == "end_turn":
            print("  Agent完成")
            break

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            # 执行工具
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  调用工具: {block.name}")

                    tool_start = time.time()
                    result = execute_tool(block.name, block.input)
                    tool_elapsed = time.time() - tool_start
                    tool_times.append((block.name, tool_elapsed))

                    print(f"    耗时: {tool_elapsed:.3f}秒")

                    # 显示结果大小
                    result_str = json.dumps(result, ensure_ascii=False)
                    print(f"    返回数据大小: {len(result_str)} 字符")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_str
                    })

            messages.append({"role": "user", "content": tool_results})
        else:
            print(f"  意外停止: {response.stop_reason}")
            break

    total_elapsed = time.time() - total_start

    # 汇总统计
    print("\n=== 性能汇总 ===")
    print(f"总耗时: {total_elapsed:.3f}秒")
    print(f"\nLLM调用:")
    print(f"  次数: {len(llm_times)}")
    print(f"  总耗时: {sum(llm_times):.3f}秒 ({sum(llm_times)/total_elapsed*100:.1f}%)")
    print(f"  平均: {sum(llm_times)/len(llm_times):.3f}秒")
    print(f"  范围: {min(llm_times):.3f}s - {max(llm_times):.3f}s")

    print(f"\n工具调用:")
    print(f"  次数: {len(tool_times)}")
    print(f"  总耗时: {sum(t[1] for t in tool_times):.3f}秒 ({sum(t[1] for t in tool_times)/total_elapsed*100:.1f}%)")

    # 按工具类型分组
    from collections import defaultdict
    tool_stats = defaultdict(list)
    for name, elapsed in tool_times:
        tool_stats[name].append(elapsed)

    print(f"\n  按工具分类:")
    for tool_name, times in tool_stats.items():
        print(f"    {tool_name}:")
        print(f"      调用次数: {len(times)}")
        print(f"      总耗时: {sum(times):.3f}秒")
        print(f"      平均: {sum(times)/len(times):.3f}秒")


def main():
    """主测试函数"""
    print("=" * 60)
    print("MCP性能测试")
    print("=" * 60)

    # 测试1: 数据源加载
    loading_time, num_sources = test_datasource_loading()

    # 测试2: 工具性能
    tool_times = test_tool_performance()

    # 测试3: LLM API延迟
    llm_latency = test_llm_api_latency()

    # 测试4: 简单Agent搜索
    print("\n" + "=" * 60)
    simple_query_time = test_agent_search(
        "中国人民银行",
        "简单查询"
    )

    # 测试5: 复杂Agent搜索（带详细分析）
    print("\n" + "=" * 60)
    test_with_instrumented_agent(
        "我需要研究中国近10年的货币政策，特别是M1、M2货币供应量和利率数据"
    )

    # 最终总结
    print("\n" + "=" * 60)
    print("性能总结")
    print("=" * 60)
    print(f"\n数据源加载: {loading_time:.3f}秒 ({num_sources}个)")
    print(f"\n工具执行耗时:")
    for tool, elapsed in tool_times.items():
        print(f"  {tool}: {elapsed:.3f}秒")

    if llm_latency:
        print(f"\n单次LLM调用: {llm_latency:.3f}秒")

    print(f"\n简单查询总耗时: {simple_query_time:.3f}秒")

    # 性能瓶颈分析
    print("\n" + "=" * 60)
    print("性能瓶颈分析")
    print("=" * 60)

    base_url = os.getenv("ANTHROPIC_BASE_URL")
    if base_url and "deepminer.ai" in base_url:
        print("⚠ 发现自定义API网关: " + base_url)
        print("  建议: 测试使用官方API是否更快")

    if llm_latency and llm_latency > 2.0:
        print("⚠ LLM API延迟较高 (>2秒)")
        print("  可能原因: 网络延迟、API网关、模型负载")

    print("\n优化建议:")
    print("1. 数据源加载可以在启动时缓存到内存（已实现）")
    print("2. LLM调用是主要耗时，考虑:")
    print("   - 减少迭代次数（简化System Prompt）")
    print("   - 使用更快的模型（如Haiku）")
    print("   - 为简单查询添加快速路径（跳过Agent）")
    print("3. 工具执行很快，不是瓶颈")


if __name__ == "__main__":
    main()
