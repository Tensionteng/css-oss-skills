#!/bin/bash
# AI Research Writing Skills - Installation Script
# Interactive installation with global/project-level choice

set -e

REPO_URL="https://github.com/Tensionteng/css-oss-skills.git"
SKILLS=("research-brainstorming" "research-execution" "pdf-reader" "manuscript-writing" "peer-review")

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}🔧 AI Research Writing Skills - 安装${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

# Get home directory
HOME_DIR="$HOME"
if [ -z "$HOME_DIR" ]; then
    HOME_DIR="$(getent passwd "$USER" | cut -d: -f6)"
fi

GLOBAL_DIR="$HOME_DIR/.config/agents/skills"
PROJECT_DIR="./.agents/skills"

# Check if running in interactive mode
if [ -t 0 ] && [ -t 1 ]; then
    # Interactive mode - both stdin and stdout are terminals
    INTERACTIVE=1
else
    INTERACTIVE=0
fi

if [ $INTERACTIVE -eq 1 ]; then
    # Interactive selection
    echo -e "${YELLOW}请选择安装方式：${NC}"
    echo ""
    echo "  1) 全局安装 - 所有项目可用"
    echo "     $GLOBAL_DIR"
    echo ""
    echo "  2) 项目级安装 - 仅当前项目可用"
    echo "     $PROJECT_DIR"
    echo ""
    read -p "请输入选项 (1 或 2，默认: 1): " choice
    choice=${choice:-1}
else
    # Non-interactive mode - show info and use default
    echo ""
    echo -e "${YELLOW}⚠️  检测到非交互式环境 (如 curl | bash)${NC}"
    echo ""
    echo "将使用默认安装方式：全局安装"
    echo "如需项目级安装，请下载脚本后手动运行："
    echo ""
    echo "  wget https://raw.githubusercontent.com/Tensionteng/css-oss-skills/main/install-local.sh"
    echo "  bash install-local.sh"
    echo ""
    choice="1"
fi

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
        echo -e "${YELLOW}无效选项，使用默认全局安装${NC}"
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
cd "$TARGET_DIR" && TARGET_DIR="$(pwd)"

echo -e "${YELLOW}📥 开始下载...${NC}"

# Create temporary directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Clone
echo "  正在克隆仓库..."
if ! git clone --depth 1 "$REPO_URL" "$TEMP_DIR/css-oss-skills" 2>/dev/null; then
    echo -e "${RED}❌ 下载失败，请检查网络连接${NC}"
    exit 1
fi

echo -e "${GREEN}  ✓ 下载完成${NC}"
echo ""

# Check for existing installation
if [ -d "$TARGET_DIR/research-brainstorming" ] || [ -d "$TARGET_DIR/manuscript-writing" ]; then
    echo -e "${YELLOW}⚠️  检测到已存在的 skills，将自动覆盖更新${NC}"
    echo ""
fi

# Install
echo -e "${CYAN}📦 开始安装 skills...${NC}"
echo ""
cd "$TEMP_DIR/css-oss-skills"

for skill in "${SKILLS[@]}"; do
    if [ -d "$skill" ]; then
        if [ -d "$TARGET_DIR/$skill" ]; then
            rm -rf "$TARGET_DIR/$skill"
        fi
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
echo "   /skill:research-brainstorming    头脑风暴"
echo "   /skill:research-execution        实验执行"
echo "   /skill:manuscript-writing        论文写作"
echo "   /skill:peer-review               审稿反馈"
echo "   /skill:pdf-reader                PDF 阅读"
echo ""
