#!/usr/bin/env python3
import re
from pathlib import Path
from collections import defaultdict

# 子类别映射规则
SUBCATEGORY_MAPPING = {
    # International
    '经济': 'economics',
    'Economics': 'economics',
    '贸易': 'trade',
    'Trade': 'trade',
    '能源': 'energy',
    'Energy': 'energy',
    '健康': 'health',
    'Health': 'health',
    '环境': 'environment',
    'Environment': 'environment',
    '农业': 'agriculture',
    'Agriculture': 'agriculture',
    '发展': 'development',
    'Development': 'development',
    '发展金融': 'development-finance',
    'Development Finance': 'development-finance',
    '教育': 'education',
    'Education': 'education',
    '金融': 'finance',
    'Finance': 'finance',
    '知识产权': 'intellectual-property',
    'Intellectual Property': 'intellectual-property',
    '地球科学': 'earth-science',
    'Earth Science': 'earth-science',
    '生物学': 'biology',
    'Biology': 'biology',
    '化学': 'chemistry',
    'Chemistry': 'chemistry',
    '劳工与社会': 'labour-social',
    'Labour & Social': 'labour-social',
    '交通运输': 'transport',
    'Transport': 'transport',
    '标准与计量': 'standards',
    'Standards & Metrology': 'standards',

    # Countries (regions)
    '北美洲': 'north-america',
    '欧洲': 'europe',
    '亚洲': 'asia',
    '大洋洲': 'oceania',
    '南美洲': 'south-america',
    '非洲': 'africa',

    # Specific countries to regions
    '美国': 'north-america',
    '加拿大': 'north-america',
    '墨西哥': 'north-america',
    '日本': 'asia',
    '韩国': 'asia',
    '新加坡': 'asia',
    '印度': 'asia',
    '英国': 'europe',
    '德国': 'europe',
    '法国': 'europe',
    '欧盟': 'europe',
    '澳大利亚': 'oceania',
    '新西兰': 'oceania',
    '巴西': 'south-america',
    '阿根廷': 'south-america',
    '智利': 'south-america',
    '哥伦比亚': 'south-america',

    # Academic
    '综合性数据仓库': 'repositories',
    '经济学': 'economics',
    '健康医学': 'health',
    '环境科学': 'environment',
    '社会科学': 'social',
    '物理化学': 'physics_chemistry',
    '生命科学': 'biology',

    # Sectors
    '能源领域': 'energy',
    '能源': 'energy',
    '科技创新': 'innovation_patents',
    '专利': 'innovation_patents',
    '教育评估': 'education',
    '农业与食品': 'agriculture_food',
    '农业': 'agriculture_food',
    '金融市场': 'finance_markets',
    '计算机科学与AI': 'computer_science_ai',
    'AI/ML': 'computer_science_ai',
    'ML': 'computer_science_ai',
    '自然语言处理': 'nlp',
    '地球科学与地理信息': 'geoscience_geography',
    '地球科学与地理': 'geoscience_geography',
    '生物与生命科学': 'biology',
    '化学与材料': 'chemistry_materials',
    '社交媒体与网络数据': 'social_media',
    '社交媒体与网络': 'social_media',
    '体育运动': 'sports',
    '交通运输': 'transportation',
    '博物馆与文化遗产': 'museums_culture',
    '博物馆与文化': 'museums_culture',
    '时间序列数据': 'timeseries',
    '网络安全': 'cybersecurity',
    '其他专业领域': 'other',
    '其他领域': 'other',
}

def extract_datasource_full_name(line):
    """Extract full datasource name including Chinese description"""
    line = re.sub(r'^[0-9]+\.\s*', '', line)
    line = re.sub(r'^-\s*', '', line)
    line = re.sub(r'📋\s*', '', line)
    name = re.sub(r'\s*⭐\s*', '', line)
    name = re.sub(r'\s*💎\s*', '', name)
    name = re.sub(r'\s*（[^）]+）\s*$', '', name)
    return name.strip()

def normalize_for_dedup(name):
    """Normalize a datasource name for deduplication comparison"""
    main_part = name.split('-')[0].strip()
    normalized = main_part.lower().strip()
    return normalized

def clean_section_name(section):
    """Clean section name by removing extra markers and text"""
    if not section:
        return section

    # Remove emoji
    section = re.sub(r'[\U0001F1E0-\U0001F1FF]+\s*', '', section)  # Flags
    section = re.sub(r'[⭐💎📋✅🔶🔷]+', '', section)  # Other emoji

    # Remove patterns like (Xh个), (X个待完成), - 已完成 X/X
    section = re.sub(r'\s*[（\(]\d+[个h][^)）]*[）\)]', '', section)
    section = re.sub(r'\s*-\s*已完成\s*\d+/\d+', '', section)
    section = re.sub(r'\s*-\s*已完成', '', section)

    return section.strip()

def extract_section_title(line):
    """Extract section title from markdown header"""
    # Match headers like: ### 经济 | Economics, #### 能源领域, ### 🇺🇸 美国
    line = line.strip()
    if line.startswith('#'):
        # Remove # symbols
        title = re.sub(r'^#+\s*', '', line)
        # Remove emoji flags
        title = re.sub(r'[\U0001F1E0-\U0001F1FF]+\s*', '', title)
        # Extract text before |
        if '|' in title:
            parts = title.split('|')
            cn_part = clean_section_name(parts[0].strip())
            en_part = clean_section_name(parts[1].strip()) if len(parts) > 1 else ''
            return cn_part, en_part
        cleaned = clean_section_name(title.strip())
        return cleaned, ''
    return None, None

def get_main_category(filename):
    """Get main category from filename"""
    name = Path(filename).stem
    if name == 'international':
        return 'international', '国际组织'
    elif name == 'countries':
        return 'countries', '各国官方'
    elif name == 'academic':
        return 'academic', '学术研究'
    elif name == 'sectors':
        return 'sectors', '行业领域'
    return None, None

def infer_country_region_from_name(datasource_name):
    """Infer country/region from datasource name"""
    name_lower = datasource_name.lower()

    # Oceania (check first to avoid conflicts with "bureau")
    if any(x in name_lower for x in ['australia', 'australian', 'data.gov.au', 'geoscience australia']):
        return 'oceania'
    if any(x in name_lower for x in ['new zealand', 'stats nz', 'data.govt.nz']):
        return 'oceania'

    # North America
    if any(x in name_lower for x in ['canada', 'canadian']):
        return 'north-america'
    if any(x in name_lower for x in ['mexico', 'mexican', 'inegi', 'coneval', 'semarnat', 'datos.gob.mx']):
        return 'north-america'
    # US-specific terms (check for Australia first to avoid false positives)
    if any(x in name_lower for x in ['bureau of labor', 'bureau of economic', 'bureau of meteorology']):
        # Bureau of Meteorology is Australian, but others are US
        if 'meteorology' in name_lower:
            return 'oceania'
        return 'north-america'
    if any(x in name_lower for x in ['united states', 'u.s.', 'us ', 'eia', 'epa', 'cdc',
                                      'sec ', 'uspto', 'nces', 'fred', 'data.gov', 'usda', 'nasa earth']):
        return 'north-america'

    # Europe
    if any(x in name_lower for x in ['european', 'eurostat', 'europeana']):
        return 'europe'
    if any(x in name_lower for x in ['england', 'uk ', 'british', 'data.gov.uk', 'nhs']):
        return 'europe'
    if any(x in name_lower for x in ['germany', 'german', 'france', 'french']):
        return 'europe'

    # Asia
    if any(x in name_lower for x in ['japan', 'japanese', 'e-stat', 'ministry of finance', 'ministry of economy']):
        # Check if it's specifically Japanese context
        if 'ministry' in name_lower:
            return 'asia'
        return 'asia'
    if any(x in name_lower for x in ['korea', 'korean', 'data.go.kr']):
        return 'asia'
    if any(x in name_lower for x in ['singapore', 'singstat', 'data.gov.sg', 'monetary authority of singapore']):
        return 'asia'
    if any(x in name_lower for x in ['india', 'indian', 'data.gov.in', 'niti aayog']):
        return 'asia'

    # South America
    if any(x in name_lower for x in ['brazil', 'brazilian', 'ibge', 'dados.gov.br']):
        return 'south-america'
    if any(x in name_lower for x in ['argentina', 'argentinian']):
        return 'south-america'
    if any(x in name_lower for x in ['chile', 'chilean']):
        return 'south-america'
    if any(x in name_lower for x in ['colombia', 'colombian']):
        return 'south-america'

    return None

def map_subcategory(section_cn, section_en, main_category, datasource_name=''):
    """Map section title to subcategory path"""
    # For countries, try to infer from datasource name first
    if main_category == 'countries':
        inferred_region = infer_country_region_from_name(datasource_name)
        if inferred_region:
            return inferred_region

    # Try Chinese first
    if section_cn in SUBCATEGORY_MAPPING:
        return SUBCATEGORY_MAPPING[section_cn]
    # Try English
    if section_en in SUBCATEGORY_MAPPING:
        return SUBCATEGORY_MAPPING[section_en]

    # Partial matching for compound titles
    for key, value in SUBCATEGORY_MAPPING.items():
        if key in section_cn or key in section_en:
            return value

    return 'other'

def find_datasources_with_categories():
    """Find all datasources with their categories"""
    datasources_dict = {}  # normalized_name -> (full_name, main_cat, sub_cat, cn_name, en_name)
    tasks_dir = Path('/Users/mlamp/project/datasource-hub/tasks')

    invalid_patterns = [
        r'^\*\*', r'^选择任务', r'^状态', r'^待', r'^已',
        r'^详细清单', r'^\d+个$', r'^[（\(]', r'^更新', r'→',
    ]

    # Process main task files
    for md_file in [tasks_dir / 'international.md', tasks_dir / 'countries.md',
                     tasks_dir / 'academic.md', tasks_dir / 'sectors.md']:
        if not md_file.exists():
            continue

        main_cat, main_cat_cn = get_main_category(md_file)
        if not main_cat:
            continue

        current_section_cn = ''
        current_section_en = ''

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                for line in f:
                    # Check for section headers
                    section_cn, section_en = extract_section_title(line)
                    if section_cn:
                        current_section_cn = section_cn
                        current_section_en = section_en
                        continue

                    # Check for datasources
                    if '📋' in line and (line.strip().startswith('-') or re.match(r'^\d+\.', line.strip())):
                        if '待完成' in line or '待开始' in line:
                            continue

                        full_name = extract_datasource_full_name(line)

                        # Skip invalid entries
                        skip = False
                        for pattern in invalid_patterns:
                            if re.search(pattern, full_name):
                                skip = True
                                break

                        if not skip and full_name and len(full_name) > 3:
                            norm_key = normalize_for_dedup(full_name)
                            sub_cat = map_subcategory(current_section_cn, current_section_en, main_cat, full_name)

                            # Keep the longer/more detailed version
                            if norm_key not in datasources_dict or len(full_name) > len(datasources_dict[norm_key][0]):
                                datasources_dict[norm_key] = (
                                    full_name,
                                    main_cat,
                                    sub_cat,
                                    main_cat_cn,
                                    current_section_cn
                                )

        except Exception as e:
            print(f"Error processing {md_file}: {e}")

    # Sort by datasource name
    sorted_items = sorted(datasources_dict.values(), key=lambda x: x[0])
    return sorted_items

if __name__ == '__main__':
    datasources = find_datasources_with_categories()

    # Write to file with categories
    output_file = '/Users/mlamp/project/datasource-hub/batch-datasource.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for full_name, main_cat, sub_cat, main_cat_cn, section_cn in datasources:
            # Format: Datasource Name | main/sub | 主类别/子类别
            category_path = f"{main_cat}/{sub_cat}"
            # Clean the Chinese category name
            section_cn_clean = clean_section_name(section_cn)
            category_cn = f"{main_cat_cn}/{section_cn_clean}" if section_cn_clean else main_cat_cn
            f.write(f"{full_name} | {category_path} | {category_cn}\n")

    print(f"✅ Found {len(datasources)} datasources with categories")
    print(f"✅ Written to {output_file}")
    print("\n=== 前15个数据源（带类别） ===")
    for i, (name, main, sub, main_cn, sec_cn) in enumerate(datasources[:15], 1):
        cat_path = f"{main}/{sub}"
        cat_cn = f"{main_cn}/{sec_cn}" if sec_cn else main_cn
        print(f"{i}. {name}")
        print(f"   📁 {cat_path} | {cat_cn}")

    print("\n=== 类别统计 ===")
    cat_stats = defaultdict(int)
    for _, main_cat, sub_cat, _, _ in datasources:
        cat_stats[f"{main_cat}/{sub_cat}"] += 1

    for cat, count in sorted(cat_stats.items(), key=lambda x: -x[1])[:20]:
        print(f"{cat}: {count}")
