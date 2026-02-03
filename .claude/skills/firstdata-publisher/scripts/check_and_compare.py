#!/usr/bin/env python3
"""
数据源文档检查和对比工具
1. 扫描实际的JSON文件
2. 扫描文档中的统计信息
3. 对比差异
4. 生成更新报告
"""

import json
import re
from collections import defaultdict
from pathlib import Path


class DataSourceChecker:
    def __init__(self):
        self.actual_sources = {}  # 实际的JSON文件
        self.doc_entries = {}  # 文档中的条目
        self.doc_stats = {}  # 文档中的统计数字

    def scan_actual_sources(self):
        """扫描实际的JSON文件"""
        print("=" * 80)
        print("步骤1: 扫描实际数据源文件")
        print("=" * 80)

        sources_dir = Path("src/firstdata/sources")
        json_files = list(sources_dir.rglob("*.json"))

        by_category = defaultdict(list)
        by_subcategory = defaultdict(lambda: defaultdict(list))

        for json_file in sorted(json_files):
            try:
                with open(json_file, encoding="utf-8") as f:
                    data = json.load(f)

                # 提取关键信息
                info = {
                    "id": data.get("id", ""),
                    "filename_id": json_file.stem,  # 从文件名提取ID，用于匹配
                    "name_en": data.get("name", {}).get("en", ""),
                    "name_zh": data.get("name", {}).get("zh", ""),
                    "authority": data.get("authority_level", ""),
                    "has_api": data.get("api_url") is not None,
                    "access_level": "open" if data.get("api_url") else "registration",
                    "update_frequency": data.get("update_frequency", ""),
                    "data_content_count": len(data.get("data_content", {}).get("zh", [])),
                    "path": str(json_file.relative_to("src/firstdata/sources")),
                }

                # 确定分类
                parts = json_file.parts
                if "international" in parts:
                    category = "international"
                    subcategory = parts[parts.index("international") + 1]
                elif "china" in parts:
                    category = "china"
                    subcategory = parts[parts.index("china") + 1]
                elif "countries" in parts:
                    category = "countries"
                    subcategory = parts[parts.index("countries") + 1]
                elif "academic" in parts:
                    category = "academic"
                    subcategory = parts[parts.index("academic") + 1]
                elif "sectors" in parts:
                    category = "sectors"
                    subcategory = parts[parts.index("sectors") + 1]
                else:
                    continue

                info["category"] = category
                info["subcategory"] = subcategory

                by_category[category].append(info)
                by_subcategory[category][subcategory].append(info)

            except Exception as e:
                print(f"  ⚠️  错误: {json_file}: {e}")

        self.actual_sources = {
            "total": len(json_files),
            "by_category": {cat: len(sources) for cat, sources in by_category.items()},
            "by_subcategory": dict(by_subcategory),
            "all": by_category,
        }

        print(f"\n✅ 找到 {len(json_files)} 个JSON文件")
        for category, count in sorted(self.actual_sources["by_category"].items()):
            print(f"   {category:15s}: {count:3d} 个")

        return self.actual_sources

    def scan_docs(self):
        """扫描文档中的统计和条目"""
        print("\n" + "=" * 80)
        print("步骤2: 扫描文档中的统计信息")
        print("=" * 80)

        docs_to_check = {
            "international": "src/firstdata/sources/international/README.md",
            "china": "src/firstdata/sources/china/README.md",
            "countries": "src/firstdata/sources/countries/README.md",
            "academic": "src/firstdata/sources/academic/README.md",
            "sectors": "src/firstdata/sources/sectors/README.md",
            "main_readme": "README.md",
        }

        self.doc_entries = defaultdict(lambda: defaultdict(set))
        self.doc_stats = {}

        # 扫描各分类README中的条目
        for category in ["international", "china", "countries", "academic", "sectors"]:
            readme_path = docs_to_check[category]
            if not Path(readme_path).exists():
                print(f"  ⚠️  {readme_path} 不存在")
                continue

            with open(readme_path, encoding="utf-8") as f:
                content = f.read()

            # 查找所有数据源ID（在文件链接中）
            # 匹配模式: [filename.json](path/to/file.json)
            pattern = r"\[([^\]]+\.json)\]\(([^\)]+)\)"
            matches = re.findall(pattern, content)

            for _filename, filepath in matches:
                # 从filepath提取ID（通常是文件名去掉.json）
                source_id = Path(filepath).stem
                self.doc_entries[category]["found"].add(source_id)

            print(f"  {category:15s}: 文档中找到 {len(self.doc_entries[category]['found'])} 个条目")

        # 扫描主要文档中的统计数字
        self._scan_main_readme()

        # 扫描分类README中的统计数字
        self._scan_china_readme()
        self._scan_sectors_readme()
        self._scan_countries_readme()

        return self.doc_entries, self.doc_stats

    def _scan_main_readme(self):
        """扫描主README中的统计"""
        if not Path("README.md").exists():
            return

        with open("README.md", encoding="utf-8") as f:
            content = f.read()

        stats = {}

        # 提取总数（从徽章）
        # Badge 格式: /badge/数据源-126%2F1000+
        badge_match = re.search(r"数据源-(\d+)%2F", content)
        if badge_match:
            stats["total_in_badge"] = int(badge_match.group(1))

        # 提取分类统计（从表格）
        # 匹配: | 总数据源 | 127 / 950+ |
        total_match = re.search(r"\|\s*总数据源\s*\|\s*(\d+)\s*/\s*(\d+)", content)
        if total_match:
            stats["total_in_table"] = int(total_match.group(1))

        # 提取各分类数字
        category_patterns = {
            "international": r"\|\s*国际组织\s*\|\s*(\d+)\s*/\s*(\d+)",
            "countries": r"\|\s*各国官方\s*\|\s*(\d+)\s*/\s*(\d+)",
            "china": r"\|\s*中国数据源\s*\|\s*(\d+)\s*/\s*(\d+)",
            "academic": r"\|\s*学术研究\s*\|\s*(\d+)\s*/\s*(\d+)",
            "sectors": r"\|\s*行业领域\s*\|\s*(\d+)\s*/\s*(\d+)",
        }

        for category, pattern in category_patterns.items():
            match = re.search(pattern, content)
            if match:
                stats[f"{category}_in_table"] = int(match.group(1))

        self.doc_stats["main_readme"] = stats
        print("\n  README.md 统计:")
        print(f"    徽章总数: {stats.get('total_in_badge', 'N/A')}")
        print(f"    表格总数: {stats.get('total_in_table', 'N/A')}")

    def _scan_china_readme(self):
        """扫描src/firstdata/sources/china/README.md中的统计"""
        readme_path = "src/firstdata/sources/china/README.md"
        if not Path(readme_path).exists():
            return

        with open(readme_path, encoding="utf-8") as f:
            content = f.read()

        stats = {}

        # 提取已完成数量（第4行左右）
        completed_match = re.search(r"\*\*已完成\*\*:\s*(\d+)个", content)
        if completed_match:
            stats["completed"] = int(completed_match.group(1))

        # 提取当前完成数（进度条中）
        current_match = re.search(r"当前完成:\s*(\d+)\s*个", content)
        if current_match:
            stats["current"] = int(current_match.group(1))

        self.doc_stats["china_readme"] = stats
        print("\n  src/firstdata/sources/china/README.md 统计:")
        print(f"    已完成: {stats.get('completed', 'N/A')} 个")

    def _scan_sectors_readme(self):
        """扫描src/firstdata/sources/sectors/README.md中的统计"""
        readme_path = "src/firstdata/sources/sectors/README.md"
        if not Path(readme_path).exists():
            return

        with open(readme_path, encoding="utf-8") as f:
            content = f.read()

        stats = {}

        # 提取已完成数量（第5行左右）
        completed_match = re.search(r"\*\*已完成\*\*:\s*(\d+)个", content)
        if completed_match:
            stats["completed"] = int(completed_match.group(1))

        # 提取当前完成数（进度条中）
        current_match = re.search(r"当前完成:\s*(\d+)\s*个", content)
        if current_match:
            stats["current"] = int(current_match.group(1))

        self.doc_stats["sectors_readme"] = stats
        print("\n  src/firstdata/sources/sectors/README.md 统计:")
        print(f"    已完成: {stats.get('completed', 'N/A')} 个")

    def _scan_countries_readme(self):
        """扫描src/firstdata/sources/countries/README.md中的统计"""
        readme_path = "src/firstdata/sources/countries/README.md"
        if not Path(readme_path).exists():
            return

        with open(readme_path, encoding="utf-8") as f:
            content = f.read()

        stats = {}

        # 提取当前完成数（进度条中）
        current_match = re.search(r"当前完成:\s*(\d+)\s*个", content)
        if current_match:
            stats["current"] = int(current_match.group(1))

        self.doc_stats["countries_readme"] = stats
        print("\n  src/firstdata/sources/countries/README.md 统计:")
        print(f"    当前完成: {stats.get('current', 'N/A')} 个")

    def compare(self):
        """对比实际数据源和文档"""
        print("\n" + "=" * 80)
        print("步骤3: 对比差异")
        print("=" * 80)

        report = {"summary": {}, "missing_in_docs": {}, "stats_mismatch": [], "recommendations": []}

        # 1. 对比各分类的数量
        print("\n【数量对比】")
        print(f"{'分类':<15} {'实际':<8} {'文档':<8} {'差异':<8} 状态")
        print("-" * 50)

        for category in ["international", "china", "countries", "academic", "sectors"]:
            actual_count = self.actual_sources["by_category"].get(category, 0)
            doc_count = len(self.doc_entries[category]["found"])
            diff = actual_count - doc_count
            status = "✅" if diff == 0 else "❌"

            print(f"{category:<15} {actual_count:<8} {doc_count:<8} {diff:<8} {status}")

            report["summary"][category] = {
                "actual": actual_count,
                "in_docs": doc_count,
                "diff": diff,
            }

        # 2. 找出文档中缺失的数据源
        print("\n【缺失条目详情】")
        for category in ["international", "china", "countries", "academic", "sectors"]:
            # 使用filename_id来匹配（因为README中使用文件名，不是JSON的id字段）
            actual_ids = {s["filename_id"] for s in self.actual_sources["all"].get(category, [])}
            doc_ids = self.doc_entries[category]["found"]
            missing_ids = actual_ids - doc_ids

            if missing_ids:
                report["missing_in_docs"][category] = []
                print(f"\n{category.upper()} - 缺失 {len(missing_ids)} 个:")

                for source in self.actual_sources["all"][category]:
                    if source["filename_id"] in missing_ids:
                        print(f"  ❌ {source['name_en']} ({source['id']})")
                        print(f"     路径: {source['path']}")
                        report["missing_in_docs"][category].append(source)

        # 3. 对比核心文档中的统计数字
        print("\n【核心文档统计对比】")
        actual_total = self.actual_sources["total"]

        docs_with_stats = [
            ("README.md徽章", self.doc_stats.get("main_readme", {}).get("total_in_badge")),
            ("README.md表格", self.doc_stats.get("main_readme", {}).get("total_in_table")),
        ]

        for doc_name, doc_total in docs_with_stats:
            if doc_total is not None:
                match = "✅" if doc_total == actual_total else "❌"
                print(f"  {doc_name:<20}: {doc_total:>3} (实际: {actual_total}) {match}")

                if doc_total != actual_total:
                    report["stats_mismatch"].append(
                        {"doc": doc_name, "current": doc_total, "should_be": actual_total}
                    )

        # 4. 对比分类README中的统计数字
        print("\n【分类README统计对比】")

        # China README
        actual_china = self.actual_sources["by_category"].get("china", 0)
        china_completed = self.doc_stats.get("china_readme", {}).get("completed")
        if china_completed is not None:
            match = "✅" if china_completed == actual_china else "❌"
            print(
                f"  src/firstdata/sources/china/README.md: {china_completed:>3} (实际: {actual_china}) {match}"
            )
            if china_completed != actual_china:
                report["stats_mismatch"].append(
                    {
                        "doc": "src/firstdata/sources/china/README.md",
                        "current": china_completed,
                        "should_be": actual_china,
                    }
                )

        # Sectors README
        actual_sectors = self.actual_sources["by_category"].get("sectors", 0)
        sectors_completed = self.doc_stats.get("sectors_readme", {}).get("completed")
        if sectors_completed is not None:
            match = "✅" if sectors_completed == actual_sectors else "❌"
            print(
                f"  src/firstdata/sources/sectors/README.md: {sectors_completed:>3} (实际: {actual_sectors}) {match}"
            )
            if sectors_completed != actual_sectors:
                report["stats_mismatch"].append(
                    {
                        "doc": "src/firstdata/sources/sectors/README.md",
                        "current": sectors_completed,
                        "should_be": actual_sectors,
                    }
                )

        # Countries README
        actual_countries = self.actual_sources["by_category"].get("countries", 0)
        countries_current = self.doc_stats.get("countries_readme", {}).get("current")
        if countries_current is not None:
            match = "✅" if countries_current == actual_countries else "❌"
            print(
                f"  src/firstdata/sources/countries/README.md: {countries_current:>3} (实际: {actual_countries}) {match}"
            )
            if countries_current != actual_countries:
                report["stats_mismatch"].append(
                    {
                        "doc": "src/firstdata/sources/countries/README.md",
                        "current": countries_current,
                        "should_be": actual_countries,
                    }
                )

        # 5. 生成更新建议
        print("\n" + "=" * 80)
        print("步骤4: 更新建议")
        print("=" * 80)

        total_missing = sum(len(v) for v in report["missing_in_docs"].values())
        total_stats_issues = len(report["stats_mismatch"])

        print("\n📊 总结:")
        print(f"  • 实际数据源总数: {actual_total}")
        print(f"  • 缺失文档条目: {total_missing} 个")
        print(f"  • 统计数字错误: {total_stats_issues} 处")

        if total_missing > 0:
            print("\n📝 需要更新的文档:")
            for category, missing in report["missing_in_docs"].items():
                if missing:
                    print(f"  • sources/{category}/README.md - 添加 {len(missing)} 个条目")
                    report["recommendations"].append(
                        {
                            "action": "add_entries",
                            "file": f"sources/{category}/README.md",
                            "count": len(missing),
                            "sources": missing,
                        }
                    )

        if total_stats_issues > 0:
            print("\n🔢 需要更新统计数字的文档:")
            files_to_update = {item["doc"].split("(")[0] for item in report["stats_mismatch"]}
            for file in files_to_update:
                print(f"  • {file} - 更新总数为 {actual_total}")
                report["recommendations"].append(
                    {"action": "update_stats", "file": file, "new_total": actual_total}
                )

        return report

    def save_report(self, report):
        """保存对比报告"""
        output_file = ".claude/skills/firstdata-publisher/scripts/comparison_report.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n💾 详细报告已保存: {output_file}")
        return output_file


def main():
    print("数据源文档检查和对比工具")
    print("=" * 80)

    checker = DataSourceChecker()

    # 1. 扫描实际数据源
    checker.scan_actual_sources()

    # 2. 扫描文档
    checker.scan_docs()

    # 3. 对比
    report = checker.compare()

    # 4. 保存报告
    checker.save_report(report)

    print("\n" + "=" * 80)
    print("✅ 检查完成")
    print("=" * 80)


if __name__ == "__main__":
    main()
