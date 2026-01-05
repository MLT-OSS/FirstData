#!/usr/bin/env python3
"""
自动统计数据源并更新所有进度文件

功能：
1. 统计各分类下的数据源数量
2. 计算质量评分
3. 更新 README.md 中的所有进度信息
4. 生成详细的统计报告

使用方法：
    python .claude/skills/datasource-scraper/scripts/update_progress.py
    python .claude/skills/datasource-scraper/scripts/update_progress.py --dry-run  # 仅显示变更，不实际修改
    python .claude/skills/datasource-scraper/scripts/update_progress.py --verbose  # 显示详细信息
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
import argparse
import sys


class ProgressUpdater:
    """进度统计和更新器"""

    def __init__(self, base_dir: Path, dry_run: bool = False, verbose: bool = False):
        self.base_dir = base_dir
        self.sources_dir = base_dir / "sources"
        self.dry_run = dry_run
        self.verbose = verbose

        # 目标文件路径
        self.readme_path = base_dir / "README.md"

        # 统计数据
        self.stats = {
            'total': 0,
            'international': 0,
            'china': 0,
            'countries': 0,
            'academic': 0,
            'sectors': 0,
        }

        # 数据源详细列表
        self.datasources = {
            'international': [],
            'china': [],
            'countries': [],
            'academic': [],
            'sectors': [],
        }

        # 质量评分
        self.quality_scores = []

    def log(self, message: str, force: bool = False):
        """输出日志"""
        if self.verbose or force:
            print(message)

    def scan_datasources(self):
        """扫描所有数据源文件并统计"""
        self.log("🔍 扫描数据源文件...", force=True)

        for category in ['international', 'china', 'countries', 'academic', 'sectors']:
            category_dir = self.sources_dir / category
            if not category_dir.exists():
                continue

            json_files = list(category_dir.rglob("*.json"))
            self.stats[category] = len(json_files)

            self.log(f"  {category}: {len(json_files)} 个文件")

            # 读取每个数据源的详细信息
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # 提取信息
                    ds_info = {
                        'id': data.get('id', ''),
                        'name_zh': data.get('name', {}).get('zh', ''),
                        'name_en': data.get('name', {}).get('en', ''),
                        'authority': data.get('quality', {}).get('authority_level', 0),
                        'file_path': str(json_file.relative_to(self.base_dir))
                    }

                    # 计算平均质量（只使用6个标准评分字段）
                    quality = data.get('quality', {})
                    if quality:
                        # 标准的6个质量评分字段
                        quality_fields = [
                            'authority_level',
                            'methodology_transparency',
                            'update_timeliness',
                            'data_completeness',
                            'documentation_quality',
                            'citation_count'
                        ]
                        # 只提取数值类型的质量评分
                        scores = [
                            quality[field] for field in quality_fields
                            if field in quality and isinstance(quality[field], (int, float))
                        ]
                        if scores:
                            avg_quality = sum(scores) / len(scores)
                            self.quality_scores.append(avg_quality)
                            ds_info['avg_quality'] = avg_quality

                    self.datasources[category].append(ds_info)

                except Exception as e:
                    self.log(f"  ⚠️  读取文件失败: {json_file} - {e}")

        self.stats['total'] = sum(self.stats.values())

        self.log(f"\n✅ 扫描完成，共找到 {self.stats['total']} 个数据源", force=True)
        return self.stats

    def calculate_progress(self) -> Dict[str, float]:
        """计算进度百分比"""
        # 目标数量（从PRD或ROADMAP中获取）
        targets = {
            'total': 950,
            'international': 100,
            'china': 488,
            'countries': 200,
            'academic': 50,
            'sectors': 150,
        }

        progress = {}
        for key, current in self.stats.items():
            target = targets[key]
            progress[key] = round((current / target) * 100) if target > 0 else 0

        return progress

    def calculate_avg_quality(self) -> float:
        """计算平均质量评分"""
        if not self.quality_scores:
            return 5.0
        return round(sum(self.quality_scores) / len(self.quality_scores), 1)

    def generate_report(self) -> str:
        """生成统计报告"""
        progress = self.calculate_progress()
        avg_quality = self.calculate_avg_quality()

        report = []
        report.append("=" * 60)
        report.append("📊 数据源统计报告")
        report.append("=" * 60)
        report.append("")
        report.append(f"总数据源: {self.stats['total']} / 950+ ({progress['total']}%)")
        report.append(f"国际组织: {self.stats['international']} / 100+ ({progress['international']}%)")
        report.append(f"中国数据源: {self.stats['china']} / 488 ({progress['china']}%)")
        report.append(f"各国官方: {self.stats['countries']} / 200+ ({progress['countries']}%)")
        report.append(f"学术研究: {self.stats['academic']} / 50+ ({progress['academic']}%)")
        report.append(f"行业领域: {self.stats['sectors']} / 150+ ({progress['sectors']}%)")
        report.append("")
        report.append(f"平均质量评分: {avg_quality}/5.0")
        report.append("")
        report.append("=" * 60)

        return "\n".join(report)

    def update_readme_badges(self, content: str) -> str:
        """更新README顶部徽章"""
        progress = self.calculate_progress()

        # 更新数据源数量徽章
        pattern_sources = r'\[\!\[Data Sources\]\(https://img\.shields\.io/badge/Data%20Sources-\d+%2F950\+-blue\.svg\)\]'
        replacement_sources = f'[![Data Sources](https://img.shields.io/badge/Data%20Sources-{self.stats["total"]}%2F950+-blue.svg)]'
        content = re.sub(pattern_sources, replacement_sources, content)

        # 更新进度徽章
        pattern_progress = r'\[\!\[Progress\]\(https://img\.shields\.io/badge/Progress-\d+%25-yellow\.svg\)\]'
        replacement_progress = f'[![Progress](https://img.shields.io/badge/Progress-{progress["total"]}%25-yellow.svg)]'
        content = re.sub(pattern_progress, replacement_progress, content)

        # 更新质量评分徽章
        avg_quality = self.calculate_avg_quality()
        pattern_quality = r'\[\!\[Quality Rating\]\(https://img\.shields\.io/badge/Avg%20Quality-[\d.]+%2F5\.0-brightgreen\.svg\)\]'
        replacement_quality = f'[![Quality Rating](https://img.shields.io/badge/Avg%20Quality-{avg_quality}%2F5.0-brightgreen.svg)]'
        content = re.sub(pattern_quality, replacement_quality, content)

        return content

    def update_readme_stats_table(self, content: str) -> str:
        """更新总体统计表格"""
        progress = self.calculate_progress()

        # 构建新的表格内容
        table_lines = [
            "| 指标 | 当前/目标 | 进度 |",
            "|------|-----------|------|",
            f"| **总数据源** | {self.stats['total']} / 950+ | {progress['total']}% |",
            f"| **国际组织** | {self.stats['international']} / 100+ | {progress['international']}% |",
            f"| **各国官方** | {self.stats['countries']} / 200+ | {progress['countries']}% |",
            f"| **中国数据源** | {self.stats['china']} / 488 | {progress['china']}% |",
            f"| **学术研究** | {self.stats['academic']} / 50+ | {progress['academic']}% |",
            f"| **行业领域** | {self.stats['sectors']} / 150+ | {progress['sectors']}% |",
        ]

        new_table = "\n".join(table_lines)

        # 替换表格（从"| 指标 | 当前/目标 | 进度 |"开始，到"| **行业领域**"结束）
        pattern = r'\| 指标 \| 当前/目标 \| 进度 \|.*?\| \*\*行业领域\*\* \|[^\n]*'
        content = re.sub(pattern, new_table, content, flags=re.DOTALL)

        return content

    def update_readme_datasource_lists(self, content: str) -> str:
        """更新已完成数据源列表"""
        # 更新国际组织
        content = self._update_category_list(
            content,
            'international',
            r'#### 🌍 国际组织 \((\d+)个\)',
            f'#### 🌍 国际组织 ({self.stats["international"]}个)'
        )

        # 更新中国数据源
        content = self._update_category_list(
            content,
            'china',
            r'#### 🇨🇳 中国数据源 \((\d+)个\)',
            f'#### 🇨🇳 中国数据源 ({self.stats["china"]}个)'
        )

        # 更新各国官方
        content = self._update_category_list(
            content,
            'countries',
            r'#### 🌎 各国官方 \((\d+)个\)',
            f'#### 🌎 各国官方 ({self.stats["countries"]}个)'
        )

        # 更新学术研究
        content = self._update_category_list(
            content,
            'academic',
            r'#### 🎓 学术研究 \((\d+)个\)',
            f'#### 🎓 学术研究 ({self.stats["academic"]}个)'
        )

        # 更新行业领域
        content = self._update_category_list(
            content,
            'sectors',
            r'#### 🏭 行业领域 \((\d+)个\)',
            f'#### 🏭 行业领域 ({self.stats["sectors"]}个)'
        )

        return content

    def _update_category_list(self, content: str, category: str,
                             header_pattern: str, new_header: str) -> str:
        """更新单个分类的数据源列表"""
        # 只更新标题中的数字
        content = re.sub(header_pattern, new_header, content)
        return content

    def update_readme_project_status(self, content: str) -> str:
        """更新项目状态表格"""
        progress = self.calculate_progress()
        avg_quality = self.calculate_avg_quality()

        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')

        # 构建新的项目状态表格
        status_lines = [
            "| 指标 | 状态 |",
            "|------|------|",
            "| **当前里程碑** | M0 完成 ✅ / M1 进行中 🚧 |",
            f"| **总体进度** | {self.stats['total']} / 950+ ({progress['total']}%) |",
            f"| **完成度** | 国际组织 {progress['international']}%、中国 {progress['china']}%、学术 {progress['academic']}% |",
            f"| **最近更新** | {today} |",
            f"| **质量评分** | ⭐⭐⭐⭐⭐ ({avg_quality}/5.0) |",
        ]

        new_status = "\n".join(status_lines)

        # 替换项目状态表格
        pattern = r'## 📊 项目状态 \| Project Status\s*\n\s*\| 指标 \| 状态 \|.*?\| \*\*质量评分\*\* \|[^\n]*'
        replacement = f"## 📊 项目状态 | Project Status\n\n{new_status}"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        return content

    def update_readme(self) -> bool:
        """更新 README.md"""
        self.log("📝 更新 README.md...", force=True)

        if not self.readme_path.exists():
            self.log("❌ README.md 不存在", force=True)
            return False

        # 读取原内容
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # 执行各项更新
        content = original_content
        content = self.update_readme_badges(content)
        content = self.update_readme_stats_table(content)
        content = self.update_readme_datasource_lists(content)
        content = self.update_readme_project_status(content)

        # 检查是否有变更
        if content == original_content:
            self.log("  ℹ️  没有需要更新的内容", force=True)
            return False

        if self.dry_run:
            self.log("  🔍 [DRY RUN] 检测到变更，但不会实际修改文件", force=True)
            # 显示差异
            self._show_diff(original_content, content)
            return True

        # 写入新内容
        with open(self.readme_path, 'w', encoding='utf-8') as f:
            f.write(content)

        self.log("  ✅ README.md 已更新", force=True)
        return True

    def _show_diff(self, old: str, new: str):
        """显示文件差异（简化版）"""
        old_lines = old.split('\n')
        new_lines = new.split('\n')

        changes = []
        for i, (old_line, new_line) in enumerate(zip(old_lines, new_lines), 1):
            if old_line != new_line:
                changes.append(f"  Line {i}:")
                changes.append(f"    - {old_line[:80]}")
                changes.append(f"    + {new_line[:80]}")

        if changes:
            self.log("\n  变更预览:")
            self.log("\n".join(changes[:20]))  # 只显示前20个变更
            if len(changes) > 20:
                self.log(f"  ... 还有 {len(changes) - 20} 处变更")

    def run(self) -> int:
        """执行完整的更新流程"""
        try:
            # 1. 扫描数据源
            self.scan_datasources()

            # 2. 生成报告
            report = self.generate_report()
            print("\n" + report)

            # 3. 更新 README
            readme_updated = self.update_readme()

            # 4. 总结
            print("\n" + "=" * 60)
            if self.dry_run:
                print("🔍 DRY RUN 模式 - 未进行实际修改")
            else:
                print("✅ 更新完成")

            if readme_updated:
                print(f"📝 README.md: {'检测到变更' if self.dry_run else '已更新'}")
            else:
                print("ℹ️  所有文件已是最新状态")

            print("=" * 60)

            return 0

        except Exception as e:
            print(f"\n❌ 错误: {e}", file=sys.stderr)
            if self.verbose:
                import traceback
                traceback.print_exc()
            return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="自动统计数据源并更新所有进度文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                    # 统计并更新所有文件
  %(prog)s --dry-run          # 仅显示变更，不实际修改
  %(prog)s --verbose          # 显示详细信息
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅显示将要进行的变更，不实际修改文件'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细的执行信息'
    )

    parser.add_argument(
        '--base-dir',
        type=Path,
        default=Path.cwd(),
        help='项目根目录路径（默认：当前目录）'
    )

    args = parser.parse_args()

    # 创建更新器并运行
    updater = ProgressUpdater(
        base_dir=args.base_dir,
        dry_run=args.dry_run,
        verbose=args.verbose
    )

    return updater.run()


if __name__ == '__main__':
    sys.exit(main())
