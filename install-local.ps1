# AI Research Writing Skills - Installation Script for Windows
# Supports both global and project-level installation

$REPO_URL = "https://github.com/Tensionteng/css-oss-skills.git"
$SKILLS = @("research-brainstorming", "research-execution", "pdf-reader", "manuscript-writing", "peer-review")

# Colors for output
$Green = "Green"
$Yellow = "Yellow"
$Cyan = "Cyan"
$Red = "Red"

Write-Host "🔧 AI Research Writing Skills - 安装脚本" -ForegroundColor $Cyan
Write-Host "=========================================" -ForegroundColor $Cyan
Write-Host ""

# Determine available installation locations
$GlobalDir = Join-Path $env:USERPROFILE ".config\agents\skills"
$ProjectDir = ".\.agents\skills"
$CurrentDir = Get-Location

# Interactive selection
Write-Host "请选择安装方式：" -ForegroundColor $Yellow
Write-Host ""
Write-Host "  1) 全局安装 (所有项目可用)"
Write-Host "     位置: $GlobalDir"
Write-Host ""
Write-Host "  2) 项目级安装 (仅当前项目可用，可随代码提交)"
Write-Host "     位置: $ProjectDir"
Write-Host "     当前目录: $CurrentDir"
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
        Write-Host "无效选项，使用默认全局安装" -ForegroundColor $Red
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

# Create temporary directory for download
$TempDir = Join-Path $env:TEMP ("ai-research-skills-" + [Guid]::NewGuid().ToString().Substring(0, 8))
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

try {
    # Clone to temporary directory
    Write-Host "  正在克隆仓库..."
    $CloneOutput = Join-Path $TempDir "ai-research-writing-skills"
    
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
    
    # Check if old version exists and show warning
    $existingSkills = $SKILLS | Where-Object { Test-Path (Join-Path $TargetDir $_) }
    if ($existingSkills.Count -gt 0) {
        Write-Host "⚠️ 检测到已存在的 skills，将自动覆盖更新" -ForegroundColor $Yellow
        Write-Host ""
    }
    
    # Install/Update skills
    Write-Host "📦 安装 skills..." -ForegroundColor $Cyan
    
    foreach ($skill in $SKILLS) {
        $sourcePath = Join-Path $CloneOutput $skill
        $targetPath = Join-Path $TargetDir $skill
        
        if (Test-Path $sourcePath -PathType Container) {
            # Remove old version if exists (safe because we already downloaded)
            if (Test-Path $targetPath) {
                Remove-Item -Recurse -Force $targetPath
            }
            # Copy new version
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
    
    if ($InstallType -eq "项目级") {
        $parentDir = Split-Path (Split-Path $TargetDir)
        Write-Host "   Set-Location $parentDir"
    }
    
    Write-Host "   /skill:research-brainstorming"
    Write-Host "   /skill:manuscript-writing"
    Write-Host ""
    Write-Host "💡 提示:" -ForegroundColor $Yellow
    
    if ($InstallType -eq "全局") {
        Write-Host "   - 所有项目都可以使用这些 skills"
        Write-Host "   - 更新：重新运行此脚本即可"
    } else {
        Write-Host "   - 项目级 skills 可以和代码一起提交到 Git"
        Write-Host "   - 团队成员会自动使用相同版本"
        Write-Host "   - 不同项目可以使用不同版本的 skills"
    }
} finally {
    # Cleanup temporary directory
    if (Test-Path $TempDir) {
        Remove-Item -Recurse -Force $TempDir -ErrorAction SilentlyContinue
    }
}
