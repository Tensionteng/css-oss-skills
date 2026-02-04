# AI Research Writing Skills - Installation Script for Windows
# Interactive installation with global/project-level choice

$REPO_URL = "https://github.com/Tensionteng/css-oss-skills.git"
$SKILLS = @("research-brainstorming", "research-execution", "pdf-reader", "manuscript-writing", "peer-review")

$Green = "Green"
$Yellow = "Yellow"
$Cyan = "Cyan"
$Red = "Red"

Write-Host ""
Write-Host "🔧 AI Research Writing Skills - 安装" -ForegroundColor $Cyan
Write-Host "=========================================" -ForegroundColor $Cyan
Write-Host ""

$GlobalDir = Join-Path $env:USERPROFILE ".config\agents\skills"
$ProjectDir = ".\.agents\skills"

# Interactive selection
Write-Host "请选择安装方式：" -ForegroundColor $Yellow
Write-Host ""
Write-Host "  1) 全局安装 - 所有项目可用"
Write-Host "     $GlobalDir"
Write-Host ""
Write-Host "  2) 项目级安装 - 仅当前项目可用"
Write-Host "     $ProjectDir"
Write-Host ""

$choice = Read-Host "请输入选项 (1 或 2，默认: 1)"
if ([string]::IsNullOrWhiteSpace($choice)) {
    $choice = "1"
}

switch ($choice) {
    "1" {
        $TargetDir = $GlobalDir
        $InstallType = "全局"
    }
    "2" {
        $TargetDir = $ProjectDir
        $InstallType = "项目级"
    }
    default {
        Write-Host "无效选项，使用默认全局安装" -ForegroundColor $Yellow
        $TargetDir = $GlobalDir
        $InstallType = "全局"
    }
}

Write-Host ""
Write-Host "安装类型: $InstallType" -ForegroundColor $Cyan
Write-Host "目标位置: $TargetDir" -ForegroundColor $Cyan
Write-Host ""

# Create target directory
New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
$TargetDir = Resolve-Path $TargetDir

Write-Host "📥 开始下载..." -ForegroundColor $Yellow

# Create temporary directory
$TempDir = Join-Path $env:TEMP ("ai-research-skills-" + [Guid]::NewGuid().ToString().Substring(0, 8))
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

try {
    Write-Host "  正在克隆仓库..."
    $CloneOutput = Join-Path $TempDir "css-oss-skills"
    
    try {
        git clone --depth 1 $REPO_URL $CloneOutput 2>&1 | Out-Null
        if (-not $?) {
            throw "Git clone failed"
        }
    } catch {
        Write-Host "❌ 下载失败，请检查网络连接或 Git 是否已安装" -ForegroundColor $Red
        exit 1
    }
    
    Write-Host "  ✓ 下载完成" -ForegroundColor $Green
    Write-Host ""
    
    # Check for existing installation
    $existingSkills = $SKILLS | Where-Object { Test-Path (Join-Path $TargetDir $_) }
    if ($existingSkills.Count -gt 0) {
        Write-Host "⚠️  检测到已存在的 skills，将自动覆盖更新" -ForegroundColor $Yellow
        Write-Host ""
    }
    
    # Install
    Write-Host "📦 开始安装 skills..." -ForegroundColor $Cyan
    Write-Host ""
    
    foreach ($skill in $SKILLS) {
        $sourcePath = Join-Path $CloneOutput $skill
        $targetPath = Join-Path $TargetDir $skill
        
        if (Test-Path $sourcePath -PathType Container) {
            if (Test-Path $targetPath) {
                Remove-Item -Recurse -Force $targetPath
            }
            Copy-Item -Recurse $sourcePath $TargetDir
            Write-Host "  ✓ $skill" -ForegroundColor $Green
        } else {
            Write-Host "  ✗ $skill (未找到)" -ForegroundColor $Red
        }
    }
    
    Write-Host ""
    Write-Host "✅ 安装完成!" -ForegroundColor $Green
    Write-Host ""
    Write-Host "📍 Skills 位置: $TargetDir" -ForegroundColor $Yellow
    Write-Host ""
    Write-Host "🚀 使用方法:" -ForegroundColor $Cyan
    Write-Host "   /skill:research-brainstorming    头脑风暴"
    Write-Host "   /skill:research-execution        实验执行"
    Write-Host "   /skill:manuscript-writing        论文写作"
    Write-Host "   /skill:peer-review               审稿反馈"
    Write-Host "   /skill:pdf-reader                PDF 阅读"
    Write-Host ""
} finally {
    # Cleanup
    if (Test-Path $TempDir) {
        Remove-Item -Recurse -Force $TempDir -ErrorAction SilentlyContinue
    }
}
