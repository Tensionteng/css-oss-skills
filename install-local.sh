#!/bin/bash
# AI Research Writing Skills - Installation Script
# Supports both global and project-level installation

set -e

REPO_URL="https://github.com/Tensionteng/css-oss-skills.git"
SKILLS=("research-brainstorming" "research-execution" "pdf-reader" "manuscript-writing" "peer-review")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🔧 AI Research Writing Skills - 安装脚本${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

# Get home directory
HOME_DIR="$HOME"
if [ -z "$HOME_DIR" ]; then
    HOME_DIR="$(getent passwd "$USER" | cut -d: -f6)"
fi

# Determine available installation locations
GLOBAL_DIR="$HOME_DIR/.config/agents/skills"
PROJECT_DIR="./.agents/skills"

# Interactive selection
echo -e "${YELLOW}请选择安装方式：${NC}"
echo ""
echo "  1) 全局安装 (所有项目可用)"
echo "     位置: $GLOBAL_DIR"
echo ""
echo "  2) 项目级安装 (仅当前项目可用，可随代码提交)"
echo "     位置: $PROJECT_DIR"
echo ""

# Default to option 1 if no input
read -p "请输入选项 (1 或 2，默认: 1): " choice
choice=${choice:-1}

case "$choice" in
    1)
        TARGET_DIR="$GLOBAL_DIR"
        INSTALL_TYPE="全局"
        ;;
    2)
        TARGET_DIR="$PROJECT_DIR"
        INSTALL_TYPE="项目级"
        ;;
    *)
        echo -e "${RED}❌ 无效选项，使用默认全局安装${NC}"
        TARGET_DIR="$GLOBAL_DIR"
        INSTALL_TYPE="全局"
        ;;
esac

echo ""
echo -e "${CYAN}安装类型: $INSTALL_TYPE${NC}"
echo -e "${CYAN}目标位置: $TARGET_DIR${NC}"
echo ""

# Create target directory
mkdir -p "$TARGET_DIR"

# Convert to absolute path
cd "$TARGET_DIR" && TARGET_DIR="$(pwd)"

echo -e "${YELLOW}📥 开始下载...${NC}"

# Create temporary directory for download
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Clone to temporary directory
echo "  正在克隆仓库..."
git clone --depth 1 "$REPO_URL" "$TEMP_DIR/ai-research-writing-skills" 2>/dev/null || {
    echo -e "${RED}❌ 下载失败，请检查网络连接${NC}"
    exit 1
}

echo -e "${GREEN}  ✓ 下载完成${NC}"
echo ""

# Check if old version exists and show warning
if [ -d "$TARGET_DIR/research-brainstorming" ] || [ -d "$TARGET_DIR/manuscript-writing" ]; then
    echo -e "${YELLOW}⚠️  检测到已存在的 skills，将自动覆盖更新${NC}"
    echo ""
fi

# Install/Update skills
echo -e "${CYAN}📦 安装 skills...${NC}"
cd "$TEMP_DIR/ai-research-writing-skills"

for skill in "${SKILLS[@]}"; do
    if [ -d "$skill" ]; then
        # Remove old version if exists (safe because we already downloaded)
        if [ -d "$TARGET_DIR/$skill" ]; then
            rm -rf "$TARGET_DIR/$skill"
        fi
        # Copy new version
        cp -r "$skill" "$TARGET_DIR/"
        echo -e "  ${GREEN}✓${NC} $skill"
    else
        echo -e "  ${RED}✗${NC} $skill (未找到)"
    fi
done

echo ""
echo -e "${GREEN}✅ 安装完成!${NC}"
echo ""
echo -e "${YELLOW}📍 Skills 位置: $TARGET_DIR${NC}"
echo ""
echo -e "${CYAN}🚀 使用方法:${NC}"

if [ "$INSTALL_TYPE" = "项目级" ]; then
    echo "   cd $(dirname $(dirname "$TARGET_DIR"))"
fi

echo "   /skill:research-brainstorming"
echo "   /skill:manuscript-writing"
echo ""
echo -e "${YELLOW}💡 提示:${NC}"

if [ "$INSTALL_TYPE" = "全局" ]; then
    echo "   - 所有项目都可以使用这些 skills"
    echo "   - 更新：重新运行此脚本即可"
else
    echo "   - 项目级 skills 可以和代码一起提交到 Git"
    echo "   - 团队成员会自动使用相同版本"
    echo "   - 不同项目可以使用不同版本的 skills"
fi
