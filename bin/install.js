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
  } else {
    log('   - 项目级 skills 可以和代码一起提交到 Git');
    log('   - 团队成员会自动使用相同版本');
    log('   - 不同项目可以使用不同版本的 skills');
  }

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

async function main() {
  try {
    // Check if running in non-interactive mode (CI/automated)
    const isCI = process.env.CI || process.env.NODE_ENV === 'production';
    const hasArgs = process.argv.length > 2;

    let targetDir;
    let installType;

    if (hasArgs) {
      // Parse command line arguments
      const args = process.argv.slice(2);
      const globalFlag = args.includes('--global') || args.includes('-g');
      const projectFlag = args.includes('--project') || args.includes('-p');

      if (globalFlag) {
        targetDir = getGlobalDir();
        installType = '全局';
      } else if (projectFlag) {
        targetDir = path.join(process.cwd(), '.agents', 'skills');
        installType = '项目级';
      } else {
        // Default to interactive mode
        const result = await promptInstallType();
        targetDir = result.targetDir;
        installType = result.installType;
      }
    } else if (isCI) {
      // Default to global in CI
      targetDir = getGlobalDir();
      installType = '全局';
    } else {
      // Interactive mode
      const result = await promptInstallType();
      targetDir = result.targetDir;
      installType = result.installType;
    }

    installSkills(targetDir, installType);
  } catch (error) {
    log(`❌ 安装失败: ${error.message}`, 'red');
    process.exit(1);
  }
}

main();
