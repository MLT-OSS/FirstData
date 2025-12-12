#!/usr/bin/env python3
"""
提取所有数据源的关键信息
用于辅助更新README和任务清单
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def extract_source_info(json_path):
    """从JSON文件提取关键信息"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 提取关键字段
        info = {
            'id': data.get('id', ''),
            'name_en': data.get('name', {}).get('en', ''),
            'name_zh': data.get('name', {}).get('zh', ''),
            'authority': data.get('quality', {}).get('authority_level', 0),
            'data_formats': ', '.join(data.get('data_characteristics', {}).get('formats', [])),
            'access_level': data.get('access', {}).get('access_level', ''),
            'path': str(json_path),
            'relative_path': os.path.relpath(json_path, 'sources')
        }

        # 根据路径确定分类
        parts = Path(json_path).parts
        if 'international' in parts:
            info['category'] = 'international'
            info['subcategory'] = parts[parts.index('international') + 1] if len(parts) > parts.index('international') + 1 else ''
        elif 'china' in parts:
            info['category'] = 'china'
            info['subcategory'] = parts[parts.index('china') + 1] if len(parts) > parts.index('china') + 1 else ''
        elif 'countries' in parts:
            info['category'] = 'countries'
            info['subcategory'] = parts[parts.index('countries') + 1] if len(parts) > parts.index('countries') + 1 else ''
        elif 'academic' in parts:
            info['category'] = 'academic'
            info['subcategory'] = parts[parts.index('academic') + 1] if len(parts) > parts.index('academic') + 1 else ''
        elif 'sectors' in parts:
            info['category'] = 'sectors'
            info['subcategory'] = parts[parts.index('sectors') + 1] if len(parts) > parts.index('sectors') + 1 else ''
        else:
            info['category'] = 'unknown'
            info['subcategory'] = ''

        return info
    except Exception as e:
        print(f"Error processing {json_path}: {e}")
        return None

def main():
    # 找到所有JSON文件
    sources_dir = Path('sources')
    json_files = list(sources_dir.rglob('*.json'))

    print(f"找到 {len(json_files)} 个JSON文件\n")

    # 按分类组织
    by_category = defaultdict(list)
    by_subcategory = defaultdict(lambda: defaultdict(list))

    for json_file in sorted(json_files):
        info = extract_source_info(json_file)
        if info:
            by_category[info['category']].append(info)
            by_subcategory[info['category']][info['subcategory']].append(info)

    # 输出统计
    print("=" * 80)
    print("各分类数据源统计")
    print("=" * 80)
    for category in ['international', 'china', 'countries', 'academic', 'sectors']:
        count = len(by_category.get(category, []))
        print(f"{category:15s}: {count:3d} 个数据源")
    print(f"{'总计':15s}: {len(json_files):3d} 个数据源")
    print()

    # 详细输出每个分类
    for category in ['international', 'china', 'countries', 'academic', 'sectors']:
        if category not in by_category:
            continue

        print("=" * 80)
        print(f"{category.upper()} 分类详情 ({len(by_category[category])} 个)")
        print("=" * 80)

        # 按子分类输出
        for subcategory in sorted(by_subcategory[category].keys()):
            sources = by_subcategory[category][subcategory]
            if not sources:
                continue

            print(f"\n### {subcategory} ({len(sources)} 个)")
            print()

            for idx, source in enumerate(sources, 1):
                # 生成图标
                icon = "⭐💎" if source['authority'] >= 5.0 else "⭐" if source['authority'] >= 4.5 else ""

                # 转换访问类型
                access_map = {
                    'open': '开放',
                    'academic': '学术注册',
                    'registration': '需注册',
                    'subscription': '订阅',
                    'controlled': '受控访问'
                }
                access_zh = access_map.get(source['access_level'], source['access_level'])

                print(f"{idx}. **{source['name_en']}** (`{source['id']}`) {icon}")
                print(f"   - 权威性：{source['authority']}")
                print(f"   - 数据格式：{source['data_formats']}")
                print(f"   - 访问类型：{access_zh}")
                print(f"   - [查看详情]({source['relative_path']})")
                print()

        print()

    # 生成JSON报告
    report = {
        'total': len(json_files),
        'by_category': {cat: len(sources) for cat, sources in by_category.items()},
        'by_subcategory': {}
    }

    for category, subcats in by_subcategory.items():
        report['by_subcategory'][category] = {}
        for subcat, sources in subcats.items():
            report['by_subcategory'][category][subcat] = [
                {
                    'id': s['id'],
                    'name_en': s['name_en'],
                    'name_zh': s['name_zh'],
                    'authority': s['authority'],
                    'data_formats': s['data_formats'],
                    'access_level': s['access_level'],
                    'path': s['relative_path']
                }
                for s in sources
            ]

    # 保存报告
    output_file = 'scripts/sources_report.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=" * 80)
    print(f"详细报告已保存到: {output_file}")
    print("=" * 80)

if __name__ == '__main__':
    main()
