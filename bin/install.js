#!/usr/bin/env node

/**
 * AI Research Writing Skills - NPX Installation Script
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const SKILLS = [
  'research-brainstorming',
  'research-execution',
  'pdf-reader',
  'manuscript-writing',
  'peer-review'
];

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
  return path.dirname(__dirname);
}

function getGlobalDir() {
  const home = process.env.HOME || process.env.USERPROFILE;
  return path.join(home, '.config', 'agents', 'skills');
}

function getProjectDir() {
  return path.join(process.cwd(), '.agents', 'skills');
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

function prompt(question) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

async function installInteractive() {
  const globalDir = getGlobalDir();
  const projectDir = getProjectDir();

  log('', 'reset');
  log('🔧 AI Research Writing Skills - 安装', 'cyan');
  log('=========================================', 'cyan');
  log('', 'reset');
  log('请选择安装方式：', 'yellow');
  log('', 'reset');
  log('  1) 全局安装 - 所有项目可用');
  log(`     ${globalDir}`);
  log('', 'reset');
  log('  2) 项目级安装 - 仅当前项目可用');
  log(`     ${projectDir}`);
  log('', 'reset');

  const choice = await prompt('请输入选项 (1 或 2，默认: 1): ') || '1';

  let targetDir;
  let installType;

  if (choice === '1') {
    targetDir = globalDir;
    installType = '全局';
  } else if (choice === '2') {
    targetDir = projectDir;
    installType = '项目级';
  } else {
    log('无效选项，使用默认全局安装', 'yellow');
    targetDir = globalDir;
    installType = '全局';
  }

  await performInstall(targetDir, installType);
}

async function performInstall(targetDir, installType) {
  const sourceDir = getSourceDir();

  log('', 'reset');
  log(`📦 安装类型: ${installType}`, 'cyan');
  log(`📍 目标位置: ${targetDir}`, 'cyan');
  log('', 'reset');

  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }
  targetDir = path.resolve(targetDir);

  log('📦 开始安装 skills...', 'cyan');
  log('', 'reset');

  let installed = 0;
  let failed = 0;

  for (const skill of SKILLS) {
    const skillSource = path.join(sourceDir, skill);
    const skillTarget = path.join(targetDir, skill);

    if (fs.existsSync(skillSource)) {
      if (fs.existsSync(skillTarget)) {
        fs.rmSync(skillTarget, { recursive: true, force: true });
      }
      copyDir(skillSource, skillTarget);
      log(`  ✓ ${skill}`, 'green');
      installed++;
    } else {
      log(`  ✗ ${skill} (未找到)`, 'red');
      failed++;
    }
  }

  log('', 'reset');
  log(`✅ 安装完成! 成功: ${installed}`, 'green');
  log('', 'reset');
  log('🚀 使用方法:', 'cyan');
  log('   /skill:research-brainstorming    头脑风暴');
  log('   /skill:research-execution        实验执行');
  log('   /skill:manuscript-writing        论文写作');
  log('   /skill:peer-review               审稿反馈');
  log('   /skill:pdf-reader                PDF 阅读');
  log('', 'reset');
}

async function uninstallInteractive() {
  const globalDir = getGlobalDir();
  const projectDir = getProjectDir();

  // Check what exists
  const globalExists = fs.existsSync(globalDir);
  const projectExists = fs.existsSync(projectDir);

  log('', 'reset');
  log('🗑️  AI Research Writing Skills - 卸载', 'cyan');
  log('=========================================', 'cyan');
  log('', 'reset');

  if (!globalExists && !projectExists) {
    log('⚠️  未检测到已安装的 skills', 'yellow');
    return;
  }

  log('即将删除以下内容：', 'yellow');
  log('', 'reset');

  if (globalExists) {
    log(`  📁 全局: ${globalDir}`);
  }
  if (projectExists) {
    log(`  📁 项目: ${projectDir}`);
  }

  log('', 'reset');
  const confirm = await prompt('确认删除? (yes/no): ');

  if (confirm.toLowerCase() !== 'yes') {
    log('已取消卸载', 'yellow');
    return;
  }

  // Uninstall global
  if (globalExists) {
    log('', 'reset');
    log('🗑️  正在卸载全局 skills...', 'cyan');
    await performUninstall(globalDir, '全局');
    // Try to remove parent directories if empty
    try {
      const agentsDir = path.dirname(globalDir);
      const configDir = path.dirname(agentsDir);
      if (fs.existsSync(globalDir) && fs.readdirSync(globalDir).length === 0) {
        fs.rmdirSync(globalDir);
        if (fs.existsSync(agentsDir) && fs.readdirSync(agentsDir).length === 0) {
          fs.rmdirSync(agentsDir);
          if (fs.existsSync(configDir) && fs.readdirSync(configDir).length === 0) {
            fs.rmdirSync(configDir);
          }
        }
      }
    } catch (e) {
      // Ignore cleanup errors
    }
  }

  // Uninstall project
  if (projectExists) {
    log('', 'reset');
    log('🗑️  正在卸载项目级 skills...', 'cyan');
    await performUninstall(projectDir, '项目级');
    // Try to remove parent directories if empty
    try {
      const agentsDir = path.dirname(projectDir);
      if (fs.existsSync(projectDir) && fs.readdirSync(projectDir).length === 0) {
        fs.rmdirSync(projectDir);
        if (fs.existsSync(agentsDir) && fs.readdirSync(agentsDir).length === 0) {
          fs.rmdirSync(agentsDir);
        }
      }
    } catch (e) {
      // Ignore cleanup errors
    }
  }

  log('', 'reset');
  log('✅ 卸载完成', 'green');
  log('', 'reset');
}

async function performUninstall(targetDir, uninstallType) {
  if (!fs.existsSync(targetDir)) {
    log(`  ⚠️  目录不存在: ${targetDir}`, 'yellow');
    return;
  }

  targetDir = path.resolve(targetDir);
  let uninstalled = 0;

  for (const skill of SKILLS) {
    const skillTarget = path.join(targetDir, skill);
    if (fs.existsSync(skillTarget)) {
      fs.rmSync(skillTarget, { recursive: true, force: true });
      log(`  ✓ ${skill}`, 'green');
      uninstalled++;
    }
  }

  if (uninstalled === 0) {
    log('  未找到已安装的 skills', 'yellow');
  }
}

function isInteractive() {
  // Check if stdin is a TTY (terminal)
  if (!process.stdin.isTTY) {
    return false;
  }
  // Check if stdout is a TTY
  if (!process.stdout.isTTY) {
    return false;
  }
  // Check for CI environments
  if (process.env.CI || process.env.CONTINUOUS_INTEGRATION) {
    return false;
  }
  return true;
}

function showHelp() {
  log('', 'reset');
  log('🔧 AI Research Writing Skills', 'cyan');
  log('=========================================', 'cyan');
  log('', 'reset');
  log('用法:', 'yellow');
  log('  npx github:Tensionteng/css-oss-skills         安装 (交互式选择)');
  log('  npx github:Tensionteng/css-oss-skills uninstall  卸载 (删除全局+项目级)');
  log('', 'reset');
  log('注意:', 'yellow');
  log('  首次运行 npx 时会提示 "Ok to proceed?" 这是 npm 的安全确认，输入 y 即可。');
  log('', 'reset');
}

async function main() {
  try {
    const args = process.argv.slice(2);

    if (args.includes('--help') || args.includes('-h')) {
      showHelp();
      return;
    }

    if (args.includes('uninstall') || args.includes('remove')) {
      await uninstallInteractive();
    } else if (isInteractive()) {
      await installInteractive();
    } else {
      // Non-interactive mode - default to global
      log('', 'reset');
      log('🔧 AI Research Writing Skills - 安装', 'cyan');
      log('=========================================', 'cyan');
      log('', 'reset');
      log('⚠️  检测到非交互式环境', 'yellow');
      log('', 'reset');
      log('将使用默认安装方式：全局安装', 'reset');
      log('', 'reset');
      await performInstall(getGlobalDir(), '全局');
    }
  } catch (error) {
    log(`❌ 错误: ${error.message}`, 'red');
    process.exit(1);
  }
}

main();
