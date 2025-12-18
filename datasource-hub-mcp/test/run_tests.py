#!/usr/bin/env python3
"""
DataSource Hub MCP 自动化测试脚本

运行test_cases.md中定义的所有测试用例，并生成详细的测试报告。
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import uuid
import requests

# 测试用例定义
TEST_CASES = [
    {
        "id": 1,
        "name": "中国宏观经济与货币政策关联分析",
        "query": "我想分析中国近10年的经济增长与货币政策之间的关系。具体来说,我需要研究GDP增长率、货币供应量(M1/M2)、利率变化以及固定资产投资之间的关联性,并评估宽松货币政策对实体经济的传导效果如何。请帮我找到合适的数据源。",
        "expected_sources": ["National Bureau of Statistics of China", "People's Bank of China"],
        "category": "详细测试"
    },
    {
        "id": 2,
        "name": "全球能源转型与碳中和路径分析",
        "query": "我正在研究全球主要经济体的能源转型路径。需要分析以下问题:\n1. 全球可再生能源(太阳能、风能、水电)占比的历史趋势和未来预测\n2. 主要国家(中国、美国、欧盟)的能源消费结构变化\n3. 碳排放数据和各国碳中和承诺的进展\n4. 能源价格(石油、天然气、电力)对能源转型的影响\n\n请推荐权威的能源数据来源。",
        "expected_sources": ["IEA Energy Data", "World Bank Open Data", "BP Statistical Review"],
        "category": "详细测试"
    },
    {
        "id": 3,
        "name": "股票市场技术分析与量化投资策略",
        "query": "我想开发一个股票量化交易策略,需要以下数据:\n1. 美股和A股主要股票的历史价格数据(最好有20年以上历史)\n2. 技术指标数据:移动平均线(SMA/EMA)、相对强弱指标(RSI)、MACD、布林带等\n3. 实时或准实时的股价数据用于回测\n4. 最好有API接口,方便程序化访问\n5. 交易量数据和市场情绪指标\n\n请推荐适合量化交易的数据源。",
        "expected_sources": ["Alpha Vantage API"],
        "category": "详细测试"
    },
    {
        "id": 4,
        "name": "中国外商投资趋势与产业政策分析",
        "query": "我在做一个关于中国外商投资环境的研究报告,需要以下数据:\n1. 近15年中国FDI(外商直接投资)流入的行业分布和国别来源\n2. 中国ODI(对外直接投资)的目的地国家和投资领域\n3. 外商投资企业数量变化趋势\n4. 中国电子商务和零售市场的发展数据\n5. 服务贸易数据,特别是金融服务、信息技术服务等高附加值服务\n6. 双边经贸协定和自贸区政策信息\n\n请帮我找到官方数据源。",
        "expected_sources": ["Ministry of Commerce of China", "National Bureau of Statistics of China"],
        "category": "详细测试"
    },
    {
        "id": 5,
        "name": "新冠疫情对全球卫生系统的影响研究",
        "query": "我在做一个关于新冠疫情对全球公共卫生系统影响的文献综述,需要:\n1. 查找2020-2024年间关于COVID-19的学术文献、临床试验研究\n2. 疫苗研发相关的生物医学文献\n3. 公共卫生政策干预措施的效果评估研究\n4. 疫情对医疗资源分配和医疗系统韧性的影响研究\n5. 需要能够按照主题词(MeSH)、作者、期刊、资助机构等维度检索文献\n\n哪里可以找到这些生物医学文献?",
        "expected_sources": ["PubMed"],
        "category": "详细测试"
    },
    {
        "id": 6,
        "name": "中国房地产市场与地方财政关系研究",
        "query": "在当前中国房地产市场调整的背景下,我想研究房地产低迷对地方政府财政收入的影响程度。具体需要:\n1. 地方政府土地出让收入(土地财政)的历史数据\n2. 房地产相关税收(契税、土地增值税等)占地方财政收入的比重\n3. 房地产开发投资、商品房销售面积和金额等市场数据\n4. 地方政府债务规模和偿债压力指标\n5. 最好有省级或城市级的细分数据,用于区域比较分析\n\n哪些官方数据源可以提供这些信息?",
        "expected_sources": ["National Bureau of Statistics of China", "Ministry of Finance of China"],
        "category": "详细测试"
    },
    {
        "id": 7,
        "name": "全球贫困与发展援助效果评估",
        "query": "我在研究国际发展援助对减贫的实际效果。需要获取:\n1. 全球和各国的贫困率数据(特别是撒哈拉以南非洲地区)\n2. 国际发展援助资金流向数据(按国家、部门、援助类型分类)\n3. 受援国的经济增长、人类发展指数(HDI)、教育和健康指标\n4. 外国直接投资(FDI)数据,用于对比援助与投资的效果\n5. 收入分配不平等数据(基尼系数等)\n6. 数据要能够进行跨国比较,并且时间跨度至少20年\n\n请推荐国际发展领域的权威数据源。",
        "expected_sources": ["World Bank Open Data", "African Development Bank"],
        "category": "详细测试"
    },
    {
        "id": 8,
        "name": "气候变化对农业生产的影响分析",
        "query": "我想研究气候变化对全球粮食安全的影响,需要以下数据:\n1. 全球主要粮食作物(小麦、水稻、玉米)的产量、种植面积、单产数据\n2. 气候数据:温度、降水、极端天气事件频率\n3. 各国农业政策和粮食储备信息\n4. 粮食价格指数和国际粮食贸易数据\n5. 农业技术研发投入和推广数据\n6. 土地利用变化和土壤质量数据\n\n请推荐农业和气候领域的数据源。",
        "expected_sources": ["FAOSTAT", "NOAA Climate Data", "World Bank Open Data"],
        "category": "详细测试"
    },
    {
        "id": 9,
        "name": "金价走势投资分析",
        "query": "调研分析一下金价的走势并给出投资建议",
        "expected_sources": ["Alpha Vantage API", "World Bank Open Data"],
        "category": "简短测试"
    },
    {
        "id": 10,
        "name": "中美贸易关系分析",
        "query": "帮我分析一下中美贸易战对两国进出口的影响,特别是高科技产品领域",
        "expected_sources": ["China Customs", "Ministry of Commerce of China", "U.S. Census Bureau"],
        "category": "简短测试"
    },
    {
        "id": 11,
        "name": "全球能源转型趋势",
        "query": "想了解一下全球可再生能源的发展趋势,哪些国家做得比较好",
        "expected_sources": ["IEA Energy Data", "World Bank Open Data"],
        "category": "简短测试"
    },
    {
        "id": 12,
        "name": "mRNA疫苗文献综述",
        "query": "我需要查找关于mRNA疫苗技术的最新研究文献,做一个文献综述",
        "expected_sources": ["PubMed"],
        "category": "简短测试"
    },
    {
        "id": 13,
        "name": "中国消费市场趋势",
        "query": "分析一下中国电商和线下零售的发展趋势,疫情后消费习惯有什么变化",
        "expected_sources": ["National Bureau of Statistics of China", "Ministry of Commerce of China"],
        "category": "简短测试"
    },
    {
        "id": 14,
        "name": "气候变化对农业影响",
        "query": "研究气候变化会不会影响全球粮食产量,需要各国的农业和气候数据",
        "expected_sources": ["FAOSTAT", "NOAA Climate Data", "IEA Energy Data"],
        "category": "简短测试"
    },
    {
        "id": 15,
        "name": "外资在华投资分析",
        "query": "想看看最近几年外资企业在中国的投资情况,哪些行业更受青睐",
        "expected_sources": ["Ministry of Commerce of China", "National Bureau of Statistics of China"],
        "category": "简短测试"
    },
    {
        "id": 16,
        "name": "人民币汇率分析",
        "query": "人民币对美元汇率最近一年的波动情况,以及影响汇率的主要因素",
        "expected_sources": ["People's Bank of China", "Alpha Vantage API"],
        "category": "简短测试"
    },
    {
        "id": 17,
        "name": "撒哈拉以南非洲贫困研究",
        "query": "想了解撒哈拉以南非洲地区的贫困状况改善了没有,有什么数据支撑",
        "expected_sources": ["World Bank Open Data", "African Development Bank"],
        "category": "简短测试"
    },
    {
        "id": 18,
        "name": "中国电影票房分析",
        "query": "收集整理目前中国电影票房前十的电影的相关资料,横向比较各电影的主题、制作公司、题材、时长等维度,并为我评估出最有可能在未来实现高票房的电影类型",
        "expected_sources": ["National Bureau of Statistics of China", "Ministry of Commerce of China"],
        "category": "简短测试"
    },
    {
        "id": 19,
        "name": "电子竞技赛事数据（负面测试）",
        "query": "我想分析近三年全球主要电竞赛事的观众数据和奖金分布,比如英雄联盟、DOTA2这些比赛",
        "expected_sources": [],
        "category": "负面测试",
        "expected_behavior": "应返回'未找到匹配的数据源'或建议更宽泛的搜索词"
    },
    {
        "id": 20,
        "name": "火星探测气象数据（负面测试）",
        "query": "需要火星表面的温度、气压和风速等气象观测数据,用于研究火星气候",
        "expected_sources": [],
        "category": "负面测试",
        "expected_behavior": "应明确返回'未找到相关数据源',不应推荐地球气候数据"
    }
]


# 全局会话管理
_mcp_session = None


class MCPSession:
    """MCP会话管理"""
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        })
        # 客户端生成session ID
        self.session_id = str(uuid.uuid4())

    def initialize(self) -> bool:
        """初始化MCP会话"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test_client", "version": "1.0"}
                }
            }

            response = self.session.post(self.server_url, json=payload, timeout=30)

            if response.status_code == 200:
                # FastMCP返回session ID在响应头中
                session_id_from_header = response.headers.get('mcp-session-id')
                if session_id_from_header:
                    self.session_id = session_id_from_header
                    return True
                # 如果没有mcp-session-id头，尝试使用客户端生成的ID
                return True

            return False

        except Exception as e:
            print(f"初始化失败: {e}")
            return False

    def call_tool(self, tool_name: str, arguments: dict) -> Tuple[str, float, str]:
        """调用MCP工具"""
        try:
            # FastMCP需要在请求头中包含session ID
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
            if self.session_id:
                headers["mcp-session-id"] = self.session_id

            payload = {
                "jsonrpc": "2.0",
                "id": str(uuid.uuid4()),
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }

            start_time = time.time()
            response = self.session.post(self.server_url, json=payload, headers=headers, timeout=120)
            # 强制使用UTF-8编码，避免requests使用ISO-8859-1导致中文乱码
            response.encoding = 'utf-8'
            elapsed = time.time() - start_time

            if response.status_code != 200:
                return "", elapsed, f"HTTP {response.status_code}: {response.text[:200]}"

            # 解析SSE响应
            result_text = ""
            for line in response.text.split('\n'):
                if line.startswith('data:'):
                    try:
                        data = json.loads(line[5:].strip())
                        if 'result' in data:
                            result = data['result']
                            if isinstance(result, dict):
                                if 'content' in result:
                                    for content in result['content']:
                                        if isinstance(content, dict) and content.get('type') == 'text':
                                            result_text += content.get('text', '')
                                elif 'result' in result:
                                    result_text = str(result['result'])
                            elif isinstance(result, str):
                                result_text = result
                    except json.JSONDecodeError:
                        continue

            return result_text, elapsed, ""

        except requests.Timeout:
            return "", 0.0, "请求超时（120秒）"
        except Exception as e:
            return "", 0.0, f"错误: {type(e).__name__} - {str(e)}"


def get_mcp_session() -> MCPSession:
    """获取或创建MCP会话"""
    global _mcp_session
    if _mcp_session is None:
        _mcp_session = MCPSession("http://localhost:8001/mcp")
        if not _mcp_session.initialize():
            print("⚠️ 警告: MCP会话初始化失败，尝试继续...")
    return _mcp_session


def call_mcp_tool(query: str) -> Tuple[str, float, str]:
    """
    通过HTTP调用MCP服务器工具

    Returns:
        (response_text, elapsed_time, error_message)
    """
    try:
        session = get_mcp_session()
        # FastMCP工具参数需要包装在params中
        return session.call_tool("datasource_search_llm_agent", {"params": {"query": query}})
    except Exception as e:
        return "", 0.0, f"错误: {type(e).__name__} - {str(e)}"


def extract_datasources_from_response(response: str) -> List[str]:
    """从响应中提取推荐的数据源名称"""
    datasources = []

    # 简单的提取逻辑：查找表格中的数据源名称
    # 这里使用简单的字符串匹配
    lines = response.split('\n')
    for line in lines:
        # 查找表格行（包含|符号）
        if '|' in line and not line.strip().startswith('|---'):
            # 提取名称列（通常是第二列）
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 2:
                # 名称可能包含<br>标签
                name = parts[2].replace('<br>', ' ').strip()
                if name and name != '名称' and name != '...':
                    datasources.append(name)

    return datasources


def run_test_case(test_case: Dict) -> Dict:
    """运行单个测试用例"""
    print(f"运行测试 {test_case['id']}: {test_case['name']}...")

    response, elapsed, error = call_mcp_tool(test_case['query'])

    if error:
        return {
            "test_id": test_case['id'],
            "name": test_case['name'],
            "category": test_case['category'],
            "status": "ERROR",
            "error": error,
            "elapsed_time": 0.0
        }

    # 提取推荐的数据源
    recommended = extract_datasources_from_response(response)
    expected = test_case.get('expected_sources', [])

    # 评估结果
    if test_case['category'] == '负面测试':
        # 负面测试：不应找到数据源
        status = "PASS" if len(recommended) == 0 or "未找到" in response else "FAIL"
    else:
        # 正面测试：检查是否推荐了期望的数据源
        matches = sum(1 for exp in expected if any(exp.lower() in rec.lower() for rec in recommended))
        coverage = matches / len(expected) if expected else 0
        status = "PASS" if coverage >= 0.5 else "PARTIAL" if coverage > 0 else "FAIL"

    return {
        "test_id": test_case['id'],
        "name": test_case['name'],
        "category": test_case['category'],
        "status": status,
        "query": test_case['query'],
        "expected_sources": expected,
        "recommended_sources": recommended,
        "response": response,
        "elapsed_time": elapsed,
        "coverage": matches / len(expected) if expected else None
    }


def generate_report(results: List[Dict], output_file: Path):
    """生成Markdown格式的测试报告"""

    # 统计结果
    total = len(results)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    partial = sum(1 for r in results if r['status'] == 'PARTIAL')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    errors = sum(1 for r in results if r['status'] == 'ERROR')

    avg_time = sum(r['elapsed_time'] for r in results) / total if total > 0 else 0

    # 生成报告
    lines = []
    lines.append("# DataSource Hub MCP 测试报告\n")
    lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append(f"**MCP服务器**: DataSource Hub Agent v0.1.0\n")
    lines.append("")

    # 总结
    lines.append("## 测试总结\n")
    lines.append(f"- **总测试数**: {total}")
    lines.append(f"- **通过**: {passed} ({passed/total*100:.1f}%)")
    lines.append(f"- **部分通过**: {partial} ({partial/total*100:.1f}%)")
    lines.append(f"- **失败**: {failed} ({failed/total*100:.1f}%)")
    lines.append(f"- **错误**: {errors} ({errors/total*100:.1f}%)")
    lines.append(f"- **平均响应时间**: {avg_time:.2f}秒\n")

    # 按类别统计
    lines.append("## 分类统计\n")
    categories = {}
    for r in results:
        cat = r['category']
        if cat not in categories:
            categories[cat] = {'total': 0, 'pass': 0}
        categories[cat]['total'] += 1
        if r['status'] == 'PASS':
            categories[cat]['pass'] += 1

    lines.append("| 类别 | 通过率 | 通过/总数 |")
    lines.append("|------|--------|-----------|")
    for cat, stats in categories.items():
        rate = stats['pass'] / stats['total'] * 100
        lines.append(f"| {cat} | {rate:.1f}% | {stats['pass']}/{stats['total']} |")
    lines.append("")

    # 详细结果
    lines.append("## 详细测试结果\n")

    for result in results:
        lines.append(f"### Test Case {result['test_id']}: {result['name']}\n")
        lines.append(f"**状态**: {'✅ PASS' if result['status'] == 'PASS' else '⚠️ PARTIAL' if result['status'] == 'PARTIAL' else '❌ FAIL' if result['status'] == 'FAIL' else '🔴 ERROR'}")
        lines.append(f"**类别**: {result['category']}")
        lines.append(f"**响应时间**: {result['elapsed_time']:.2f}秒\n")

        if result['status'] == 'ERROR':
            lines.append(f"**错误信息**: {result['error']}\n")
        else:
            lines.append("**查询**:")
            lines.append("```")
            lines.append(result['query'])
            lines.append("```\n")

            if result.get('expected_sources'):
                lines.append("**期望数据源**:")
                for src in result['expected_sources']:
                    lines.append(f"- {src}")
                lines.append("")

            if result.get('recommended_sources'):
                lines.append("**推荐数据源**:")
                for src in result['recommended_sources']:
                    # 检查是否匹配期望
                    matched = any(exp.lower() in src.lower() for exp in result.get('expected_sources', []))
                    prefix = "✅" if matched else "  "
                    lines.append(f"{prefix} {src}")
                lines.append("")

            if result.get('coverage') is not None:
                lines.append(f"**覆盖率**: {result['coverage']*100:.1f}%\n")

            lines.append("<details>")
            lines.append("<summary>完整响应</summary>\n")
            lines.append("```")
            lines.append(result['response'][:2000] + "..." if len(result['response']) > 2000 else result['response'])
            lines.append("```")
            lines.append("</details>\n")

        lines.append("---\n")

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\n测试报告已生成: {output_file}")


def main():
    """主函数"""
    print("=" * 60)
    print("DataSource Hub MCP 自动化测试")
    print("=" * 60)
    print(f"测试用例总数: {len(TEST_CASES)}")
    print("开始测试...\n")

    results = []

    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n[{i}/{len(TEST_CASES)}] ", end="")
        result = run_test_case(test_case)
        results.append(result)

        # 显示简单结果
        status_icon = {
            'PASS': '✅',
            'PARTIAL': '⚠️',
            'FAIL': '❌',
            'ERROR': '🔴'
        }
        print(f"{status_icon[result['status']]} {result['status']} ({result['elapsed_time']:.1f}s)")

        # 避免请求过快
        time.sleep(1)

    # 生成报告
    print("\n" + "=" * 60)
    print("生成测试报告...")
    output_file = Path(__file__).parent / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    generate_report(results, output_file)

    # 显示总结
    passed = sum(1 for r in results if r['status'] == 'PASS')
    print(f"\n测试完成! 通过率: {passed}/{len(results)} ({passed/len(results)*100:.1f}%)")


if __name__ == "__main__":
    main()
