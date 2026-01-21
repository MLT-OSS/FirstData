#!/bin/bash
# Quick view script for China data source samples

echo "=========================================="
echo "China Data Sources - Sample Overview"
echo "=========================================="
echo ""

for file in $(find . -name "*.json" -type f | sort); do
    echo "📄 File: $file"
    echo "   ID: $(python -c "import json; print(json.load(open('$file'))['id'])")"
    echo "   Name (EN): $(python -c "import json; print(json.load(open('$file'))['name']['en'])")"
    echo "   Name (ZH): $(python -c "import json; print(json.load(open('$file'))['name']['zh'])")"
    echo "   Authority: $(python -c "import json; q=json.load(open('$file'))['quality']; avg=(q['authority_level']+q['methodology_transparency']+q['update_timeliness']+q['data_completeness']+q['documentation_quality'])/5; print(f'{avg:.1f}/5.0')")"
    echo "   URL: $(python -c "import json; print(json.load(open('$file'))['access']['primary_url'])")"
    echo "   Status: $(python -c "import json; print(json.load(open('$file'))['catalog_metadata']['status'])")"
    echo "   ------------------------------------------"
done

echo ""
echo "Total: $(find . -name "*.json" -type f | wc -l) data sources"
echo "=========================================="
