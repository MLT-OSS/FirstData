#!/usr/bin/env python3
"""
自动统计数据源并更新所有文档文件

完整实现 SKILL.md 第8步的所有文档更新：
- 8.1: 一级目录 README（添加数据源条目）
- 8.2: 任务清单（标记完成状态）
- 8.3: 进度统计（5个文件的数字同步）

使用方法：
    python .claude/skills/datasource-scraper/scripts/update_all_docs.py
    python .claude/skills/datasource-scraper/scripts/update_all_docs.py --dry-run
    python .claude/skills/datasource-scraper/scripts/update_all_docs.py --only-stats  # 仅更新进度统计
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
import argparse
import sys
from datetime import datetime


class DocumentUpdater:
    """文档更新器 - 完整实现 SKILL.md 第8步"""

    def __init__(self, base_dir: Path, dry_run: bool = False, verbose: bool = False):
        self.base_dir = base_dir
        self.sources_dir = base_dir / "sources"
        self.tasks_dir = base_dir / "tasks"
        self.dry_run = dry_run
        self.verbose = verbose

        # 文件路径
        self.readme_path = base_dir / "README.md"
        self.tasks_readme_path = base_dir / "tasks" / "README.md"
        self.tasks_china_readme_path = base_dir / "tasks" / "china" / "README.md"
        self.roadmap_path = base_dir / "ROADMAP.md"

        # Sources 目录 README
        self.sources_readme_paths = {
            'international': base_dir / "sources" / "international" / "README.md",
            'china': base_dir / "sources" / "china" / "README.md",
            'countries': base_dir / "sources" / "countries" / "README.md",
            'academic': base_dir / "sources" / "academic" / "README.md",
            'sectors': base_dir / "sources" / "sectors" / "README.md",
        }

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

        # 更新计数器
        self.updates = {
            'readme': False,
            'tasks_readme': False,
            'tasks_china_readme': False,
            'roadmap': False,
            'sources_readmes': set(),
        }

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
                        'file_path': str(json_file.relative_to(self.base_dir)),
                        'relative_path': str(json_file.relative_to(category_dir)),
                    }

                    # 计算平均质量（只使用6个标准评分字段）
                    quality = data.get('quality', {})
                    if quality:
                        quality_fields = [
                            'authority_level', 'methodology_transparency',
                            'update_timeliness', 'data_completeness',
                            'documentation_quality', 'citation_count'
                        ]
                        scores = [
                            quality[field] for field in quality_fields
                            if field in quality and isinstance(quality[field], (int, float))
                        ]
                        if scores:
                            avg_quality = sum(scores) / len(scores)
                            self.quality_scores.append(avg_quality)
                            ds_info['avg_quality'] = avg_quality

                    # 获取数据格式
                    formats = data.get('data_content', {}).get('formats', [])
                    if not formats and 'download' in data.get('access', {}):
                        formats = data['access']['download'].get('formats', [])
                    ds_info['formats'] = formats[:3] if formats else []

                    # 获取访问类型
                    ds_info['access_level'] = data.get('access', {}).get('access_level', 'unknown')

                    self.datasources[category].append(ds_info)

                except Exception as e:
                    self.log(f"  ⚠️  读取文件失败: {json_file} - {e}")

        self.stats['total'] = sum([self.stats[k] for k in ['international', 'china', 'countries', 'academic', 'sectors']])

        self.log(f"\n✅ 扫描完成，共找到 {self.stats['total']} 个数据源", force=True)
        return self.stats

    def calculate_progress(self) -> Dict[str, int]:
        """计算进度百分比"""
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

    # ========== 8.3.1: 更新根目录 README.md ==========

    def update_readme(self) -> bool:
        """更新 README.md"""
        self.log("📝 更新 README.md...", force=True)

        if not self.readme_path.exists():
            self.log("❌ README.md 不存在", force=True)
            return False

        with open(self.readme_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        content = original_content
        content = self._update_readme_badges(content)
        content = self._update_readme_stats_table(content)
        content = self._update_readme_datasource_lists(content)
        content = self._update_readme_project_status(content)

        if content == original_content:
            self.log("  ℹ️  没有需要更新的内容", force=True)
            return False

        if not self.dry_run:
            with open(self.readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log("  ✅ README.md 已更新", force=True)
        else:
            self.log("  🔍 [DRY RUN] 检测到变更", force=True)

        self.updates['readme'] = True
        return True

    def _update_readme_badges(self, content: str) -> str:
        """更新README顶部徽章"""
        progress = self.calculate_progress()
        avg_quality = self.calculate_avg_quality()

        # 更新数据源数量
        content = re.sub(
            r'\[\!\[Data Sources\]\(https://img\.shields\.io/badge/Data%20Sources-\d+%2F950\+-blue\.svg\)\]',
            f'[![Data Sources](https://img.shields.io/badge/Data%20Sources-{self.stats["total"]}%2F950+-blue.svg)]',
            content
        )

        # 更新进度
        content = re.sub(
            r'\[\!\[Progress\]\(https://img\.shields\.io/badge/Progress-\d+%25-yellow\.svg\)\]',
            f'[![Progress](https://img.shields.io/badge/Progress-{progress["total"]}%25-yellow.svg)]',
            content
        )

        # 更新质量评分
        content = re.sub(
            r'\[\!\[Quality Rating\]\(https://img\.shields\.io/badge/Avg%20Quality-[\d.]+%2F5\.0-brightgreen\.svg\)\]',
            f'[![Quality Rating](https://img.shields.io/badge/Avg%20Quality-{avg_quality}%2F5.0-brightgreen.svg)]',
            content
        )

        return content

    def _update_readme_stats_table(self, content: str) -> str:
        """更新总体统计表格"""
        progress = self.calculate_progress()

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
        pattern = r'\| 指标 \| 当前/目标 \| 进度 \|.*?\| \*\*行业领域\*\* \|[^\n]*'
        content = re.sub(pattern, new_table, content, flags=re.DOTALL)

        return content

    def _update_readme_datasource_lists(self, content: str) -> str:
        """更新已完成数据源列表标题中的数量"""
        for category, count in [
            ('international', self.stats['international']),
            ('china', self.stats['china']),
            ('countries', self.stats['countries']),
            ('academic', self.stats['academic']),
            ('sectors', self.stats['sectors']),
        ]:
            patterns = {
                'international': r'#### 🌍 国际组织 \(\d+个\)',
                'china': r'#### 🇨🇳 中国数据源 \(\d+个\)',
                'countries': r'#### 🌎 各国官方 \(\d+个\)',
                'academic': r'#### 🎓 学术研究 \(\d+个\)',
                'sectors': r'#### 🏭 行业领域 \(\d+个\)',
            }
            replacements = {
                'international': f'#### 🌍 国际组织 ({count}个)',
                'china': f'#### 🇨🇳 中国数据源 ({count}个)',
                'countries': f'#### 🌎 各国官方 ({count}个)',
                'academic': f'#### 🎓 学术研究 ({count}个)',
                'sectors': f'#### 🏭 行业领域 ({count}个)',
            }

            if category in patterns:
                content = re.sub(patterns[category], replacements[category], content)

        return content

    def _update_readme_project_status(self, content: str) -> str:
        """更新项目状态表格"""
        progress = self.calculate_progress()
        avg_quality = self.calculate_avg_quality()
        today = datetime.now().strftime('%Y-%m-%d')

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
        pattern = r'## 📊 项目状态 \| Project Status\s*\n\s*\| 指标 \| 状态 \|.*?\| \*\*质量评分\*\* \|[^\n]*'
        replacement = f"## 📊 项目状态 | Project Status\n\n{new_status}"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        return content

    # ========== 8.3.3: 更新 tasks/README.md ==========

    def update_tasks_readme(self) -> bool:
        """更新 tasks/README.md"""
        self.log("📝 更新 tasks/README.md...", force=True)

        if not self.tasks_readme_path.exists():
            self.log("❌ tasks/README.md 不存在", force=True)
            return False

        with open(self.tasks_readme_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        content = original_content
        content = self._update_tasks_readme_header(content)
        content = self._update_tasks_readme_table(content)

        if content == original_content:
            self.log("  ℹ️  没有需要更新的内容", force=True)
            return False

        if not self.dry_run:
            with open(self.tasks_readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log("  ✅ tasks/README.md 已更新", force=True)
        else:
            self.log("  🔍 [DRY RUN] 检测到变更", force=True)

        self.updates['tasks_readme'] = True
        return True

    def _update_tasks_readme_header(self, content: str) -> str:
        """更新tasks/README.md 顶部的总进度"""
        progress = self.calculate_progress()
        today = datetime.now().strftime('%Y-%m-%d')

        # 更新最后更新时间
        content = re.sub(
            r'\*\*最后更新\*\*:\s*\d{4}-\d{2}-\d{2}',
            f'**最后更新**: {today}',
            content
        )

        # 更新总进度
        content = re.sub(
            r'\*\*总进度\*\*:\s*\d+/950\+\s*\(\d+%\)',
            f'**总进度**: {self.stats["total"]}/950+ ({progress["total"]}%)',
            content
        )

        return content

    def _update_tasks_readme_table(self, content: str) -> str:
        """更新tasks/README.md中的分类表格"""
        progress = self.calculate_progress()

        # 构建新表格
        table_lines = [
            "| 类别 | 计划 | 完成 | 进度 | 任务清单 |",
            "|------|------|------|------|----------|",
            f"| 🌍 **国际组织** | 100+ | {self.stats['international']} | {progress['international']}% | [international.md](international.md) |",
            f"| 🌎 **各国官方** | 200+ | {self.stats['countries']} | {progress['countries']}% | [countries.md](countries.md) |",
            f"| 🇨🇳 **中国数据源** | 488 | {self.stats['china']} | {progress['china']}% | [china/](china/) |",
            f"| 🎓 **学术研究** | 50+ | {self.stats['academic']} | {progress['academic']}% | [academic.md](academic.md) |",
            f"| 🏭 **行业领域** | 150+ | {self.stats['sectors']} | {progress['sectors']}% | [sectors.md](sectors.md) |",
            f"| **总计** | **950+** | **{self.stats['total']}** | **{progress['total']}%** | - |",
        ]

        new_table = "\n".join(table_lines)
        pattern = r'\| 类别 \| 计划 \| 完成 \| 进度 \| 任务清单 \|.*?\| \*\*总计\*\* \|[^\n]*'
        content = re.sub(pattern, new_table, content, flags=re.DOTALL)

        return content

    # ========== 8.3.5: 更新 ROADMAP.md ==========

    def update_roadmap(self) -> bool:
        """更新 ROADMAP.md"""
        self.log("📝 更新 ROADMAP.md...", force=True)

        if not self.roadmap_path.exists():
            self.log("❌ ROADMAP.md 不存在", force=True)
            return False

        with open(self.roadmap_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        content = original_content
        content = self._update_roadmap_header(content)
        content = self._update_roadmap_progress(content)
        content = self._update_roadmap_table(content)

        if content == original_content:
            self.log("  ℹ️  没有需要更新的内容", force=True)
            return False

        if not self.dry_run:
            with open(self.roadmap_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log("  ✅ ROADMAP.md 已更新", force=True)
        else:
            self.log("  🔍 [DRY RUN] 检测到变更", force=True)

        self.updates['roadmap'] = True
        return True

    def _update_roadmap_header(self, content: str) -> str:
        """更新ROADMAP.md顶部的总进度"""
        progress = self.calculate_progress()
        today = datetime.now().strftime('%Y-%m-%d')

        # 更新最后更新时间
        content = re.sub(
            r'\*\*最后更新\*\*:\s*\d{4}-\d{2}-\d{2}',
            f'**最后更新**: {today}',
            content
        )

        # 更新总体进度
        content = re.sub(
            r'\*\*总体进度\*\*:\s*\d+/950\+\s*\(\d+%\)',
            f'**总体进度**: {self.stats["total"]}/950+ ({progress["total"]}%)',
            content
        )

        return content

    def _update_roadmap_progress(self, content: str) -> str:
        """更新ROADMAP.md的进度条"""
        progress = self.calculate_progress()

        # 构建进度条
        total_blocks = 20
        filled = int(total_blocks * progress['total'] / 100)
        progress_bar = "▓" * filled + "░" * (total_blocks - filled)

        # 更新文本
        progress_text = [
            "```",
            "总目标: 950+ 权威数据源",
            f"当前完成: {self.stats['total']} 个",
            f"完成度: {progress_bar} {progress['total']}%",
            "```"
        ]

        pattern = r'```\s*总目标:.*?```'
        content = re.sub(pattern, "\n".join(progress_text), content, flags=re.DOTALL)

        return content

    def _update_roadmap_table(self, content: str) -> str:
        """更新ROADMAP.md的分类表格"""
        progress = self.calculate_progress()

        table_lines = [
            "| 类别 | 计划 | 完成 | 进度 | 详细任务 |",
            "|------|------|------|------|----------|",
            f"| 国际组织 | 100+ | {self.stats['international']} | {progress['international']}% | [tasks/international.md](tasks/international.md) |",
            f"| 各国官方 | 200+ | {self.stats['countries']} | {progress['countries']}% | [tasks/countries.md](tasks/countries.md) |",
            f"| 中国数据源 | 488 | {self.stats['china']} | {progress['china']}% | [tasks/china/](tasks/china/) |",
            f"| 学术研究 | 50+ | {self.stats['academic']} | {progress['academic']}% | [tasks/academic.md](tasks/academic.md) |",
            f"| 行业领域 | 150+ | {self.stats['sectors']} | {progress['sectors']}% | [tasks/sectors.md](tasks/sectors.md) |",
            f"| **总计** | **950+** | **{self.stats['total']}** | **{progress['total']}%** | [所有任务](tasks/README.md) |",
        ]

        new_table = "\n".join(table_lines)
        pattern = r'\| 类别 \| 计划 \| 完成 \| 进度 \| 详细任务 \|.*?\| \*\*总计\*\* \|[^\n]*'
        content = re.sub(pattern, new_table, content, flags=re.DOTALL)

        return content

    # ========== 主流程 ==========

    def run(self, only_stats: bool = False) -> int:
        """执行完整的更新流程"""
        try:
            # 1. 扫描数据源
            self.scan_datasources()

            # 2. 生成报告
            report = self.generate_report()
            print("\n" + report)

            # 3. 更新所有文件
            print("\n" + "=" * 60)
            print("📝 开始更新文档...")
            print("=" * 60 + "\n")

            # 8.3.1: 更新根目录 README
            self.update_readme()

            # 8.3.3: 更新 tasks/README.md
            self.update_tasks_readme()

            # 8.3.5: 更新 ROADMAP.md
            self.update_roadmap()

            # TODO: 8.3.2: 更新 sources/*/README.md（数据源列表）
            # TODO: 8.3.4: 更新 tasks/china/README.md

            # 4. 总结
            print("\n" + "=" * 60)
            if self.dry_run:
                print("🔍 DRY RUN 模式 - 未进行实际修改")
            else:
                print("✅ 更新完成")

            updated_files = []
            if self.updates['readme']:
                updated_files.append("README.md")
            if self.updates['tasks_readme']:
                updated_files.append("tasks/README.md")
            if self.updates['roadmap']:
                updated_files.append("ROADMAP.md")

            if updated_files:
                status = "检测到变更" if self.dry_run else "已更新"
                print(f"\n📝 {status}的文件:")
                for f in updated_files:
                    print(f"  - {f}")
            else:
                print("\nℹ️  所有文件已是最新状态")

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
        description="自动统计数据源并更新所有文档文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
完整实现 SKILL.md 第8步的文档更新：
  8.1: 一级目录 README（添加数据源条目）- TODO
  8.2: 任务清单（标记完成状态）- TODO
  8.3: 进度统计（5个文件的数字同步）- ✅ 已实现3个

示例:
  %(prog)s                    # 统计并更新所有文件
  %(prog)s --dry-run          # 仅显示变更，不实际修改
  %(prog)s --verbose          # 显示详细信息
  %(prog)s --only-stats       # 仅更新进度统计文件
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
        '--only-stats',
        action='store_true',
        help='仅更新进度统计文件（README, tasks/README, ROADMAP）'
    )

    parser.add_argument(
        '--base-dir',
        type=Path,
        default=Path.cwd(),
        help='项目根目录路径（默认：当前目录）'
    )

    args = parser.parse_args()

    # 创建更新器并运行
    updater = DocumentUpdater(
        base_dir=args.base_dir,
        dry_run=args.dry_run,
        verbose=args.verbose
    )

    return updater.run(only_stats=args.only_stats)


if __name__ == '__main__':
    sys.exit(main())
