#!/bin/bash

# 批量数据源处理脚本 - 双Skill模式
#
# 使用两个独立skill完成数据源处理：
#   1. datasource-fetcher: 在临时目录获取数据（隔离执行）
#   2. datasource-publisher: 在主目录更新文档和提交Git
#
# 用法:
#   ./batch-scraper.sh           # 处理全部
#   ./batch-scraper.sh 1 10      # 处理第1行到第10行
#   ./batch-scraper.sh 5         # 从第5行处理到最后

set -euo pipefail

# ============================================================================
# 配置
# ============================================================================

DATASOURCE_FILE="batch-datasource.txt"
OUTPUT_FILE="batch-run-results.md"
LOG_DIR="batch-logs"
TEMP_DIR="batch-temp"
MAIN_DIR="$PWD"

# 获取行范围参数
START_LINE=${1:-1}
END_LINE=${2:-999999}

# 创建日志和临时目录（先删除旧目录）
rm -rf "$LOG_DIR"
mkdir -p "$LOG_DIR"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

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
declare -a datasources_list
declare -a work_dirs_list

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
echo "   步骤1: 创建所有临时工作目录"
echo "   步骤2: 批量执行 datasource-fetcher"
echo "   步骤3: 统一执行 datasource-publisher"
echo ""

# ============================================================================
# 步骤1: 为所有数据源创建临时工作目录
# ============================================================================

echo "════════════════════════════════════════════════════════════════"
echo "📁 步骤1: 创建临时工作目录"
echo "════════════════════════════════════════════════════════════════"
echo ""

# 读取数据源并创建临时目录
while IFS= read -r datasource || [ -n "$datasource" ]; do
    # 跳过空行和注释
    [[ -z "$datasource" || "$datasource" =~ ^#.* ]] && continue

    total=$((total + 1))

    echo "[$total] $datasource"

    # ──────────────────────────────────────────────────────────────────
    # 创建临时工作目录
    # ──────────────────────────────────────────────────────────────────

    # 生成安全的目录名
    safe_name=$(echo "$datasource" | tr ' /.:' '_' | tr -d '()[]{}' | cut -c1-50)
    work_dir="$MAIN_DIR/$TEMP_DIR/ds-${total}-${safe_name}"
    mkdir -p "$work_dir"

    echo "  📁 临时目录: $work_dir"

    # ──────────────────────────────────────────────────────────────────
    # 复制必要文件到临时目录
    # ──────────────────────────────────────────────────────────────────

    echo "  📋 复制项目文件..."
    mkdir -p "$work_dir/.claude/skills"
    cp -r .claude/skills/datasource-fetcher "$work_dir/.claude/skills/" 2>/dev/null || true
    # cp -r scripts "$work_dir/" 2>/dev/null || true
    mkdir -p "$work_dir/sources"

    # ──────────────────────────────────────────────────────────────────
    # 创建数据源名称文件
    # ──────────────────────────────────────────────────────────────────

    echo "  📝 创建 TARGET_DATASOURCE.txt"
    echo "$datasource" > "$work_dir/TARGET_DATASOURCE.txt"

    # 保存到数组
    datasources_list+=("$datasource")
    work_dirs_list+=("$work_dir")

    echo "  ✅ 目录准备完成"
    echo ""

done < <(sed -n "${START_LINE},${END_LINE}p" "$DATASOURCE_FILE")

echo "════════════════════════════════════════════════════════════════"
echo "✅ 步骤1完成: 已创建 $total 个临时工作目录"
echo "════════════════════════════════════════════════════════════════"
echo ""

# ============================================================================
# 步骤2: 批量执行 datasource-fetcher
# ============================================================================

echo "════════════════════════════════════════════════════════════════"
echo "🚀 步骤2: 批量执行 datasource-fetcher"
echo "════════════════════════════════════════════════════════════════"
echo ""

# 遍历每个临时目录执行fetch
for i in "${!work_dirs_list[@]}"; do
    datasource="${datasources_list[$i]}"
    work_dir="${work_dirs_list[$i]}"
    task_num=$((i + 1))

    echo ""
    echo "────────────────────────────────────────────────────────────────"
    echo "[$task_num/$total] 获取: $datasource"
    echo "目录: $work_dir"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "────────────────────────────────────────────────────────────────"

    # 写入markdown
    {
        echo "## [$task_num] $datasource"
        echo ""
        echo "**开始时间**: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "### 数据获取（datasource-fetcher）"
        echo ""
        echo '```'
    } >> "$OUTPUT_FILE"

    # ──────────────────────────────────────────────────────────────────
    # 在临时目录执行datasource-fetcher
    # ──────────────────────────────────────────────────────────────────

    cd "$work_dir"

    echo "🔒 进入隔离环境: $work_dir"
    echo "🤖 执行 datasource-fetcher..."

    # 创建日志文件
    log_file="$MAIN_DIR/$LOG_DIR/task-${task_num}-fetcher.log"

    # 执行Claude命令
    if claude -p --verbose --permission-mode bypassPermissions --model sonnet \
        "请使用 datasource-fetcher skill 获取数据源。

📋 数据源名称已写入当前目录的 TARGET_DATASOURCE.txt 文件中，请先读取该文件获取要处理的数据源名称。

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
            echo "✅ [$task_num] 成功: $datasource"
        else
            failed=$((failed + 1))
            failed_sources+=("$datasource")
            status="⚠️ 部分成功（文件复制失败）"
            echo "⚠️ [$task_num] 部分成功: $datasource"
        fi

    else
        # 执行失败
        cd "$MAIN_DIR"
        failed=$((failed + 1))
        failed_sources+=("$datasource")
        status="❌ 失败"
        echo ""
        echo "❌ [$task_num] 失败: $datasource"
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

done

# ============================================================================
# 步骤2 总结
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "📊 步骤2完成: 数据获取"
echo "════════════════════════════════════════════════════════════════"
echo "总计: $total"
echo "成功: $success"
echo "失败: $failed"
if [ $total -gt 0 ]; then
    echo "成功率: $(awk "BEGIN {printf \"%.1f\", ($success/$total)*100}")%"
fi
echo ""

# 写入步骤2总结
{
    echo ""
    echo "## 📊 步骤2总结: 数据获取"
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
# 步骤3: 统一发布（使用datasource-publisher）
# ============================================================================

if [ $success -gt 0 ]; then
    echo "════════════════════════════════════════════════════════════════"
    echo "📚 步骤3: 统一发布文档和提交Git"
    echo "════════════════════════════════════════════════════════════════"
    echo ""

    {
        echo "## 步骤3: 统一发布（datasource-publisher）"
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
    echo "⚠️  没有成功获取的数据源，跳过发布步骤"
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
    echo "| 步骤 | 状态 |"
    echo "|------|------|"
    echo "| 步骤1: 创建工作目录 | $total 个目录 |"
    echo "| 步骤2: 数据获取 | $success/$total 成功 |"
    echo "| 步骤3: 文档发布 | ${publisher_status:-跳过} |"
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

# 移动结果文件到日志目录
mv "$OUTPUT_FILE" "$LOG_DIR/$OUTPUT_FILE"

echo ""
echo "📄 详细结果: $OUTPUT_FILE"
echo "📁 日志目录: $LOG_DIR/"
echo ""
echo "✨ 全部完成！"
