#!/bin/bash

# 批量数据源处理脚本 - 双Skill模式
#
# 使用两个独立skill完成数据源处理：
#   1. datasource-fetcher: 在临时目录获取数据（隔离执行）
#   2. datasource-publisher: 在主目录更新文档和提交Git
#
# 用法:
#   ./batch-scraper-dual-skill.sh           # 处理全部
#   ./batch-scraper-dual-skill.sh 1 10      # 处理第1行到第10行
#   ./batch-scraper-dual-skill.sh 5         # 从第5行处理到最后

set -euo pipefail

# ============================================================================
# 配置
# ============================================================================

DATASOURCE_FILE="batch-datasources.txt"
OUTPUT_FILE="batch-run-results-dual.md"
LOG_DIR="logs"
MAIN_DIR="$PWD"

# 获取行范围参数
START_LINE=${1:-1}
END_LINE=${2:-999999}

# 创建日志目录
mkdir -p "$LOG_DIR"

# ============================================================================
# 初始化
# ============================================================================

# 初始化输出文件
cat > "$OUTPUT_FILE" << EOF
# 批量数据源处理结果 - 双Skill模式

**开始时间**: $(date '+%Y-%m-%d %H:%M:%S')
**处理范围**: 第 $START_LINE 行到第 $END_LINE 行
**执行模式**: datasource-fetcher (隔离) + datasource-publisher (统一发布)

---

EOF

# 计数器
total=0
success=0
failed=0
declare -a failed_sources
declare -a success_sources

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║         批量数据源处理 - 双Skill模式                            ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 数据源文件: $DATASOURCE_FILE"
echo "📍 处理范围: 第 $START_LINE 行到第 $END_LINE 行"
echo "📄 结果文件: $OUTPUT_FILE"
echo ""
echo "🔄 执行模式:"
echo "   阶段1: datasource-fetcher (临时目录隔离)"
echo "   阶段2: datasource-publisher (统一发布)"
echo ""

# ============================================================================
# 阶段1: 批量获取数据源（使用datasource-fetcher）
# ============================================================================

echo "════════════════════════════════════════════════════════════════"
echo "🚀 阶段1: 批量获取数据源（隔离模式）"
echo "════════════════════════════════════════════════════════════════"
echo ""

# 读取并处理数据源
while IFS= read -r datasource || [ -n "$datasource" ]; do
    # 跳过空行和注释
    [[ -z "$datasource" || "$datasource" =~ ^#.* ]] && continue

    total=$((total + 1))

    echo ""
    echo "────────────────────────────────────────────────────────────────"
    echo "[$total] 处理: $datasource"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "────────────────────────────────────────────────────────────────"

    # 写入markdown
    {
        echo "## [$total] $datasource"
        echo ""
        echo "**开始时间**: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "### 阶段1: 数据获取（datasource-fetcher）"
        echo ""
        echo '```'
    } >> "$OUTPUT_FILE"

    # ──────────────────────────────────────────────────────────────────
    # 创建临时工作目录
    # ──────────────────────────────────────────────────────────────────

    # 生成安全的目录名
    safe_name=$(echo "$datasource" | tr ' /.:' '_' | tr -d '()[]{}' | cut -c1-50)
    work_dir=$(mktemp -d -t "ds-${safe_name}-XXXXXX")

    echo "📁 临时目录: $work_dir"

    # ──────────────────────────────────────────────────────────────────
    # 复制必要文件到临时目录
    # ──────────────────────────────────────────────────────────────────

    echo "📋 复制项目文件..."
    cp -r .claude/skills/datasource-fetcher "$work_dir/.claude/skills/" 2>/dev/null || mkdir -p "$work_dir/.claude/skills/datasource-fetcher" && cp -r .claude/skills/datasource-fetcher/* "$work_dir/.claude/skills/datasource-fetcher/"
    cp -r scripts "$work_dir/" 2>/dev/null || true
    mkdir -p "$work_dir/sources"

    # 复制现有数据源（用于upsert检测）
    cp -r sources/* "$work_dir/sources/" 2>/dev/null || true

    # ──────────────────────────────────────────────────────────────────
    # 在临时目录执行datasource-fetcher
    # ──────────────────────────────────────────────────────────────────

    cd "$work_dir"

    echo "🔒 进入隔离环境"
    echo "🤖 执行 datasource-fetcher..."

    # 创建日志文件
    log_file="$MAIN_DIR/$LOG_DIR/task-${total}-fetcher.log"

    # 执行Claude命令
    if claude -p --verbose --permission-mode bypassPermissions --model sonnet \
        "请使用 datasource-fetcher skill 获取数据源：${datasource}

⚠️ 重要提示：
- 当前在临时隔离目录中执行
- 只需完成数据获取和验证（步骤1-6）
- 不要更新文档，不要提交Git
- 生成的JSON文件将被外部脚本收集

请开始处理。" \
        2>&1 | tee "$log_file" | tee -a "$MAIN_DIR/$OUTPUT_FILE"; then

        # ──────────────────────────────────────────────────────────────
        # 执行成功，复制JSON文件回主目录
        # ──────────────────────────────────────────────────────────────

        echo ""
        echo "✅ 数据获取成功"
        echo "📦 复制JSON文件回主目录..."

        cd "$MAIN_DIR"

        # 使用rsync同步JSON文件
        if rsync -av --include='*.json' --include='*/' --exclude='*' \
            "$work_dir/sources/" "./sources/" 2>&1 | grep -v "sending incremental"; then

            success=$((success + 1))
            success_sources+=("$datasource")
            status="✅ 成功"
            echo "✅ [$total] 成功: $datasource"
        else
            failed=$((failed + 1))
            failed_sources+=("$datasource")
            status="⚠️ 部分成功（文件复制失败）"
            echo "⚠️ [$total] 部分成功: $datasource"
        fi

    else
        # 执行失败
        cd "$MAIN_DIR"
        failed=$((failed + 1))
        failed_sources+=("$datasource")
        status="❌ 失败"
        echo ""
        echo "❌ [$total] 失败: $datasource"
    fi

    # ──────────────────────────────────────────────────────────────────
    # 清理临时目录
    # ──────────────────────────────────────────────────────────────────

    echo "🗑️  清理临时目录"
    rm -rf "$work_dir"

    # 写入结果
    {
        echo '```'
        echo ""
        echo "**状态**: $status"
        echo "**结束时间**: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "---"
        echo ""
    } >> "$OUTPUT_FILE"

    # 任务间隔
    sleep 1

done < <(sed -n "${START_LINE},${END_LINE}p" "$DATASOURCE_FILE")

# ============================================================================
# 阶段1 总结
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "📊 阶段1完成: 数据获取"
echo "════════════════════════════════════════════════════════════════"
echo "总计: $total"
echo "成功: $success"
echo "失败: $failed"
if [ $total -gt 0 ]; then
    echo "成功率: $(awk "BEGIN {printf \"%.1f\", ($success/$total)*100}")%"
fi
echo ""

# 写入阶段1总结
{
    echo ""
    echo "## 📊 阶段1总结: 数据获取"
    echo ""
    echo "| 指标 | 数量 |"
    echo "|------|------|"
    echo "| 总计 | $total |"
    echo "| 成功 | $success |"
    echo "| 失败 | $failed |"
    if [ $total -gt 0 ]; then
        echo "| 成功率 | $(awk "BEGIN {printf \"%.1f\", ($success/$total)*100}")% |"
    fi
    echo ""
} >> "$OUTPUT_FILE"

# ============================================================================
# 阶段2: 统一发布（使用datasource-publisher）
# ============================================================================

if [ $success -gt 0 ]; then
    echo "════════════════════════════════════════════════════════════════"
    echo "📚 阶段2: 统一发布文档和提交Git"
    echo "════════════════════════════════════════════════════════════════"
    echo ""

    {
        echo "## 阶段2: 统一发布（datasource-publisher）"
        echo ""
        echo "**开始时间**: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo '```'
    } >> "$OUTPUT_FILE"

    # 执行datasource-publisher
    log_file="$LOG_DIR/publisher.log"

    echo "🤖 执行 datasource-publisher..."
    echo ""

    if claude -p --verbose --permission-mode bypassPermissions --model sonnet \
        "请使用 datasource-publisher skill 发布所有更改

📊 本次批处理新增了 $success 个数据源：
$(printf '- %s\n' "${success_sources[@]}")

请：
1. 检测sources目录的变化
2. 更新所有相关文档（README、tasks、sources/*/README.md）
3. 生成索引
4. 提交到Git

请开始处理。" \
        2>&1 | tee "$log_file" | tee -a "$OUTPUT_FILE"; then

        echo ""
        echo "✅ 文档发布成功"
        publisher_status="✅ 成功"
    else
        echo ""
        echo "❌ 文档发布失败"
        publisher_status="❌ 失败"
    fi

    {
        echo '```'
        echo ""
        echo "**状态**: $publisher_status"
        echo "**结束时间**: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
    } >> "$OUTPUT_FILE"

else
    echo "⚠️  没有成功获取的数据源，跳过发布阶段"
fi

# ============================================================================
# 最终总结
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ 批量处理完成"
echo "════════════════════════════════════════════════════════════════"
echo "总计: $total"
echo "成功: $success"
echo "失败: $failed"
if [ $total -gt 0 ]; then
    echo "成功率: $(awk "BEGIN {printf \"%.1f\", ($success/$total)*100}")%"
fi
echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "════════════════════════════════════════════════════════════════"

# 写入最终总结
{
    echo ""
    echo "# 📊 最终总结"
    echo ""
    echo "**结束时间**: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "| 阶段 | 状态 |"
    echo "|------|------|"
    echo "| 阶段1: 数据获取 | $success/$total 成功 |"
    echo "| 阶段2: 文档发布 | ${publisher_status:-跳过} |"
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
