#!/usr/bin/env node

/**
 * AI Research Writing Skills - NPX Installation Script
 * Supports both global and project-level installation
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

const SKILLS = [
  'research-brainstorming',
  'research-execution',
  'pdf-reader',
  'manuscript-writing',
  'peer-review'
];

// Colors for terminal output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[0;31m',
  green: '\x1b[0;32m',
  yellow: '\x1b[1;33m',
  cyan: '\x1b[0;36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function getSourceDir() {
  // When running via npx, we're inside the cloned repo
  // The source skills are in the same directory as this script's parent
  return path.dirname(__dirname);
}

function getGlobalDir() {
  const home = process.env.HOME || process.env.USERPROFILE;
  return path.join(home, '.config', 'agents', 'skills');
}

function copyDir(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function installSkills(targetDir, installType) {
  const sourceDir = getSourceDir();

  log('', 'reset');
  log(`📦 安装类型: ${installType}`, 'cyan');
  log(`📍 目标位置: ${targetDir}`, 'cyan');
  log('', 'reset');

  // Create target directory
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  // Convert to absolute path
  targetDir = path.resolve(targetDir);

  log('📦 开始安装 skills...', 'cyan');
  log('', 'reset');

  let installed = 0;
  let failed = 0;

  for (const skill of SKILLS) {
    const skillSource = path.join(sourceDir, skill);
    const skillTarget = path.join(targetDir, skill);

    if (fs.existsSync(skillSource)) {
      // Remove old version if exists
      if (fs.existsSync(skillTarget)) {
        fs.rmSync(skillTarget, { recursive: true, force: true });
      }

      // Copy new version
      copyDir(skillSource, skillTarget);
      log(`  ✓ ${skill}`, 'green');
      installed++;
    } else {
      log(`  ✗ ${skill} (未找到)`, 'red');
      failed++;
    }
  }

  log('', 'reset');
  log(`✅ 安装完成! 成功: ${installed}, 失败: ${failed}`, 'green');
  log('', 'reset');
  log(`📍 Skills 位置: ${targetDir}`, 'yellow');
  log('', 'reset');
  log('🚀 使用方法:', 'cyan');

  if (installType === '项目级') {
    const parentDir = path.dirname(path.dirname(targetDir));
    log(`   cd ${parentDir}`);
  }

  log('   /skill:research-brainstorming');
  log('   /skill:manuscript-writing');
  log('   /skill:peer-review');
  log('', 'reset');
  log('💡 提示:', 'yellow');

  if (installType === '全局') {
    log('   - 所有项目都可以使用这些 skills');
    log('   - 更新：重新运行 npx github:Tensionteng/css-oss-skills');
    log('   - 卸载：npx github:Tensionteng/css-oss-skills uninstall');
  } else {
    log('   - 项目级 skills 可以和代码一起提交到 Git');
    log('   - 团队成员会自动使用相同版本');
    log('   - 不同项目可以使用不同版本的 skills');
  }

  log('', 'reset');
}

function uninstallSkills(targetDir, uninstallType) {
  log('', 'reset');
  log(`🗑️  卸载类型: ${uninstallType}`, 'cyan');
  log(`📍 目标位置: ${targetDir}`, 'cyan');
  log('', 'reset');

  if (!fs.existsSync(targetDir)) {
    log(`⚠️  目录不存在: ${targetDir}`, 'yellow');
    log('可能已经被卸载，或从未安装。', 'reset');
    return;
  }

  targetDir = path.resolve(targetDir);

  log('🗑️  开始卸载 skills...', 'cyan');
  log('', 'reset');

  let uninstalled = 0;
  let notFound = 0;

  for (const skill of SKILLS) {
    const skillTarget = path.join(targetDir, skill);

    if (fs.existsSync(skillTarget)) {
      fs.rmSync(skillTarget, { recursive: true, force: true });
      log(`  ✓ ${skill}`, 'green');
      uninstalled++;
    } else {
      log(`  ⚠️  ${skill} (未安装)`, 'yellow');
      notFound++;
    }
  }

  log('', 'reset');
  log(`✅ 卸载完成! 成功: ${uninstalled}, 未安装: ${notFound}`, 'green');
  log('', 'reset');

  if (uninstallType === '项目级') {
    // For project-level, also try to remove the parent .agents directory if empty
    const agentsDir = path.dirname(targetDir);
    try {
      const remaining = fs.readdirSync(agentsDir);
      if (remaining.length === 0) {
        fs.rmdirSync(agentsDir);
        log(`📍 已清理空目录: ${agentsDir}`, 'yellow');
      }
    } catch (e) {
      // Ignore errors
    }
  }

  log('', 'reset');
  log('💡 提示:', 'yellow');
  log('   如需重新安装，运行：', 'reset');
  log('   npx github:Tensionteng/css-oss-skills', 'cyan');
  log('', 'reset');
}

function promptInstallType() {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const globalDir = getGlobalDir();
    const projectDir = path.join(process.cwd(), '.agents', 'skills');

    log('', 'reset');
    log('🔧 AI Research Writing Skills - 安装脚本', 'cyan');
    log('=========================================', 'cyan');
    log('', 'reset');
    log('请选择安装方式：', 'yellow');
    log('', 'reset');
    log('  1) 全局安装 (所有项目可用)');
    log(`     位置: ${globalDir}`);
    log('', 'reset');
    log('  2) 项目级安装 (仅当前项目可用，可随代码提交)');
    log(`     位置: ${projectDir}`);
    log('', 'reset');

    rl.question('请输入选项 (1 或 2，默认: 1): ', (answer) => {
      rl.close();
      const choice = answer.trim() || '1';

      switch (choice) {
        case '1':
          resolve({ targetDir: globalDir, installType: '全局' });
          break;
        case '2':
          resolve({ targetDir: projectDir, installType: '项目级' });
          break;
        default:
          log('无效选项，使用默认全局安装', 'yellow');
          resolve({ targetDir: globalDir, installType: '全局' });
      }
    });
  });
}

function isInteractive() {
  // Check if stdin is a TTY (terminal)
  if (!process.stdin.isTTY) {
    return false;
  }
  // Check for CI environments
  if (process.env.CI || process.env.CONTINUOUS_INTEGRATION) {
    return false;
  }
  // Check if running via npx/npm install (npm sets these)
  if (process.env.npm_config_global || process.env.INIT_CWD) {
    // We're being run as an npm script, check if stdin is still available
    if (!process.stdin.isTTY) {
      return false;
    }
  }
  return true;
}

function showHelp() {
  log('', 'reset');
  log('🔧 AI Research Writing Skills - 安装脚本', 'cyan');
  log('=========================================', 'cyan');
  log('', 'reset');
  log('用法: npx github:Tensionteng/css-oss-skills [命令] [选项]', 'yellow');
  log('', 'reset');
  log('命令:', 'cyan');
  log('  (无)          安装 skills');
  log('  uninstall     卸载 skills');
  log('', 'reset');
  log('选项:', 'cyan');
  log('  --global, -g    全局操作 (默认，所有项目可用)');
  log('  --project, -p   项目级操作 (仅当前项目可用)');
  log('  --help, -h      显示帮助信息');
  log('', 'reset');
  log('示例:', 'cyan');
  log('  npx github:Tensionteng/css-oss-skills              # 安装（全局）');
  log('  npx github:Tensionteng/css-oss-skills --project    # 安装（项目级）');
  log('  npx github:Tensionteng/css-oss-skills uninstall    # 卸载（全局）');
  log('  npx github:Tensionteng/css-oss-skills uninstall --project  # 卸载（项目级）');
  log('', 'reset');
}

async function main() {
  try {
    const args = process.argv.slice(2);
    const hasArgs = args.length > 0;
    const interactive = isInteractive();

    // Check for help
    if (args.includes('--help') || args.includes('-h')) {
      showHelp();
      return;
    }

    // Check for uninstall command
    const isUninstall = args.includes('uninstall') || args.includes('remove');
    
    // Filter out command to get flags
    const flags = args.filter(arg => arg !== 'uninstall' && arg !== 'remove');
    const globalFlag = flags.includes('--global') || flags.includes('-g');
    const projectFlag = flags.includes('--project') || flags.includes('-p');

    let targetDir;
    let operationType;

    if (hasArgs && !isUninstall) {
      // Install with flags
      if (globalFlag) {
        targetDir = getGlobalDir();
        operationType = '全局';
      } else if (projectFlag) {
        targetDir = path.join(process.cwd(), '.agents', 'skills');
        operationType = '项目级';
      } else {
        // Unknown args - show help and default
        showHelp();
        log('非交互式环境自动使用全局安装', 'yellow');
        log('', 'reset');
        
        targetDir = getGlobalDir();
        operationType = '全局';
      }
    } else if (isUninstall) {
      // Uninstall mode
      if (projectFlag) {
        targetDir = path.join(process.cwd(), '.agents', 'skills');
        operationType = '项目级';
      } else {
        // Default to global for uninstall
        targetDir = getGlobalDir();
        operationType = '全局';
      }
      uninstallSkills(targetDir, operationType);
      return;
    } else if (!interactive) {
      // Non-interactive install mode - default to global
      log('', 'reset');
      log('🔧 AI Research Writing Skills - 安装脚本', 'cyan');
      log('=========================================', 'cyan');
      log('', 'reset');
      log('检测到非交互式环境，使用默认全局安装', 'yellow');
      log('', 'reset');
      
      targetDir = getGlobalDir();
      operationType = '全局';
    } else {
      // Interactive install mode
      const result = await promptInstallType();
      targetDir = result.targetDir;
      operationType = result.installType;
    }

    installSkills(targetDir, operationType);
  } catch (error) {
    log(`❌ 操作失败: ${error.message}`, 'red');
    process.exit(1);
  }
}

main();
