#!/bin/bash

# 批量数据源处理脚本 - 自动化处理所有数据源
# 用法:
#   ./batch-scraper.sh           # 处理全部
#   ./batch-scraper.sh 1 10      # 处理第1行到第10行
#   ./batch-scraper.sh 5         # 从第5行处理到最后

# 配置
DATASOURCE_FILE="batch-datasources.txt"
OUTPUT_FILE="batch-run-results.md"
LOG_DIR="logs"

# 获取行范围参数
START_LINE=${1:-1}           # 默认从第1行开始
END_LINE=${2:-999999}        # 默认到最后一行

# 创建日志目录
mkdir -p "$LOG_DIR"

# 初始化输出文件
cat > "$OUTPUT_FILE" << EOF
# 批量数据源处理结果

**开始时间**: $(date '+%Y-%m-%d %H:%M:%S')
**处理范围**: 第 $START_LINE 行到第 $END_LINE 行

---

EOF

# 计数器
total=0
success=0
failed=0
declare -a failed_sources

echo "🚀 开始批量处理数据源..."
echo "📋 数据源文件: $DATASOURCE_FILE"
echo "📍 处理范围: 第 $START_LINE 行到第 $END_LINE 行"
echo "📄 结果文件: $OUTPUT_FILE"
echo ""

# 读取指定范围的行并处理
while IFS= read -r datasource || [ -n "$datasource" ]; do
    # 跳过空行和注释
    [[ -z "$datasource" || "$datasource" =~ ^#.* ]] && continue

    total=$((total + 1))

    echo ""
    echo "================================================"
    echo "[$total] 正在处理: $datasource"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "================================================"

    # 写入markdown
    {
        echo "## [$total] $datasource"
        echo ""
        echo "**开始时间**: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo '```'
    } >> "$OUTPUT_FILE"

    # 创建单独日志
    log_file="$LOG_DIR/$(echo "$datasource" | tr ' /' '_').log"

    # 执行命令（使用独立的 bash 子进程确保每次都是新的 Claude 会话）
    if bash -c "claude -p --verbose --permission-mode bypassPermissions --model sonnet '为我获取数据源：${datasource}，注意严格按照datasource-scraper中的流程运行'" 2>&1 | tee "$log_file" | tee -a "$OUTPUT_FILE"; then
        success=$((success + 1))
        status="✅ 成功"
        echo ""
        echo "✅ 成功处理: $datasource"
    else
        failed=$((failed + 1))
        failed_sources+=("$datasource")
        status="❌ 失败"
        echo ""
        echo "❌ 处理失败: $datasource"
    fi

    {
        echo '```'
        echo ""
        echo "**状态**: $status"
        echo "**结束时间**: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "---"
        echo ""
    } >> "$OUTPUT_FILE"

    sleep 1

done < <(sed -n "${START_LINE},${END_LINE}p" "$DATASOURCE_FILE")

# 生成总结
echo ""
echo "================================================"
echo "📊 批量处理完成"
echo "================================================"
echo "总计: $total"
echo "成功: $success"
echo "失败: $failed"
[ $total -gt 0 ] && echo "成功率: $(awk "BEGIN {printf \"%.1f\", ($success/$total)*100}")%"
echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================"

# 写入总结
{
    echo ""
    echo "# 📊 处理总结"
    echo ""
    echo "**结束时间**: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "| 指标 | 数量 |"
    echo "|------|------|"
    echo "| 总计 | $total |"
    echo "| 成功 | $success |"
    echo "| 失败 | $failed |"
    [ $total -gt 0 ] && echo "| 成功率 | $(awk "BEGIN {printf \"%.1f\", ($success/$total)*100}")% |"
    echo ""
} >> "$OUTPUT_FILE"

# 失败列表
if [ $failed -gt 0 ]; then
    echo ""
    echo "❌ 失败的数据源:"
    echo "## ❌ 失败的数据源" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    for source in "${failed_sources[@]}"; do
        echo "  - $source"
        echo "- $source" >> "$OUTPUT_FILE"
    done
fi

echo ""
echo "📄 详细结果: $OUTPUT_FILE"
echo "📁 日志目录: $LOG_DIR/"
echo ""
echo "✨ 全部完成！"