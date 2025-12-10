OUTPUT_FILE="batch-run-results.md"

# 创建输出文件并写入标题
echo "# 批量数据源获取结果" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "运行时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

while IFS= read -r datasource; do
    echo "=================================================="
    echo "正在处理: $datasource"

    # 记录到 MD 文件
    echo "## $datasource" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"

    # 执行命令并同时输出到终端和文件
    claude -p --verbose --permission-mode bypassPermissions --model sonnet "为我获取数据源：${datasource}" 2>&1 | tee -a "$OUTPUT_FILE"

    echo '```' >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "---" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

done < <(sed -n '6,6p' /Users/mlamp/project/datasource-hub/batch-datasources-top100.md | grep -v '^$')

echo "运行完成! 结果已保存到: $OUTPUT_FILE"