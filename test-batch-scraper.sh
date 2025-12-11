#!/bin/bash

# 测试版本 - 验证进程独立性
# 用法: ./test-batch-scraper.sh

# 配置
DATASOURCE_FILE="batch-datasources.txt"
OUTPUT_FILE="test-run-results.md"
LOG_DIR="test-logs"

# 只处理前3个数据源进行测试
START_LINE=1
END_LINE=3

# 创建日志目录
mkdir -p "$LOG_DIR"

# 初始化输出文件
cat > "$OUTPUT_FILE" << EOF
# 批量数据源处理测试结果

**开始时间**: $(date '+%Y-%m-%d %H:%M:%S')

---

EOF

# 计数器
total=0

echo "🧪 开始测试批量处理..."
echo "📋 数据源文件: $DATASOURCE_FILE"
echo "📍 测试范围: 前 3 个数据源"
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

    # 记录当前所有 bash 进程
    echo "📊 执行前的 bash 进程:"
    ps aux | grep -E "bash|claude" | grep -v grep | awk '{print "  PID: " $2 " - " $11 " " $12 " " $13 " " $14}'

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

    # 测试命令：使用真实的 Claude 命令，只是简化提示词（与 batch-scraper.sh 使用相同的 bash -c 方式）
    echo "🔄 启动独立 Claude 进程处理..."
    if bash -c "claude -p --verbose --permission-mode bypassPermissions --model sonnet 'echo 数据源名字: ${datasource}'" 2>&1 | tee "$log_file" | tee -a "$OUTPUT_FILE"; then
        status="✅ 成功"
        echo ""
        echo "✅ 成功处理: $datasource"
    else
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

    # 记录执行后的进程
    echo "📊 执行后的 bash 进程:"
    ps aux | grep -E "bash|claude" | grep -v grep | awk '{print "  PID: " $2 " - " $11 " " $12 " " $13 " " $14}'

    echo "⏱️  等待 2 秒后继续..."
    sleep 2

done < <(sed -n "${START_LINE},${END_LINE}p" "$DATASOURCE_FILE")

# 生成总结
echo ""
echo "================================================"
echo "📊 测试完成"
echo "================================================"
echo "总计处理: $total 个数据源"
echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================"
echo ""
echo "📄 测试结果: $OUTPUT_FILE"
echo "📁 日志目录: $LOG_DIR/"
echo ""
echo "✨ 测试完成！请检查每次执行是否使用了不同的 PID"
