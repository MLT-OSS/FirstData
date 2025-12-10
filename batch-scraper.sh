while IFS= read -r datasource; do
    echo "=================================================="
    echo "正在处理: $datasource"

    # 移除重定向，让 claude 直接输出到当前终端
    claude -p --verbose --permission-mode bypassPermissions --model sonnet "为我获取数据源：${datasource}"

done < <(sed -n '3,5p' /Users/mlamp/project/datasource-hub/batch-datasources-top100.md | grep -v '^$')