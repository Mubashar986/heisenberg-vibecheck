#!/usr/bin/env node

/**
 * ⚗️ Heisenberg // VibeCheck CLI
 * Universal 1-shot unpacker, local gatekeeper, and policy validator for AI agents.
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const BANNER = `
 ⚗️  H E I S E N B E R G  //  V I B E C H E C K
 ===============================================
  99.1% Pure Governance Engine for AI Agents
`;

function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();

  if (isDirectory) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(src).forEach((childItemName) => {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

function installGitHook(targetDir) {
  const gitDir = path.join(targetDir, '.git');
  if (!fs.existsSync(gitDir)) {
    return false;
  }

  const hooksDir = path.join(gitDir, 'hooks');
  if (!fs.existsSync(hooksDir)) {
    fs.mkdirSync(hooksDir, { recursive: true });
  }

  const hookFile = path.join(hooksDir, 'pre-commit');
  const hookScript = `#!/usr/bin/env bash
# ⚗️ Heisenberg Vibe-Check Pre-Commit Gate
if command -v python3 &>/dev/null; then
  python3 .agents/guard.py hook --host git --event pre-commit
elif command -v python &>/dev/null; then
  python .agents/guard.py hook --host git --event pre-commit
else
  echo "⚠️ Python not detected. Skipping local pre-commit check."
  exit 0
fi
`;

  fs.writeFileSync(hookFile, hookScript, { encoding: 'utf-8', mode: 0o755 });
  try {
    fs.chmodSync(hookFile, 0o755);
  } catch (_) {}

  return true;
}

function installEditorAdapters(targetDir) {
  // 1. Cursor hooks
  const cursorDir = path.join(targetDir, '.cursor');
  if (!fs.existsSync(cursorDir)) {
    fs.mkdirSync(cursorDir, { recursive: true });
  }
  const cursorHookFile = path.join(cursorDir, 'hooks.json');
  const cursorConfig = {
    version: 1,
    hooks: {
      preToolUse: {
        command: "python3 .agents/guard.py hook --host cursor --event pre-tool"
      }
    }
  };
  fs.writeFileSync(cursorHookFile, JSON.stringify(cursorConfig, null, 2), 'utf-8');

  // 2. Cursorrules & Windsurfrules pointers
  const rulePointer = `# Heisenberg Governance Pointer
This project is strictly governed by [AGENTS.md](AGENTS.md).
Read AGENTS.md before making edits. All tasks, artifacts, and skills live in .agents/.
`;
  fs.writeFileSync(path.join(targetDir, '.cursorrules'), rulePointer, 'utf-8');
  fs.writeFileSync(path.join(targetDir, '.windsurfrules'), rulePointer, 'utf-8');
}

function unpack(targetDir) {
  console.log(BANNER);
  console.log('Unpacking Heisenberg OS into your project...\n');

  const bundleDir = path.join(__dirname, '..', 'bundle');

  // 1. Copy AGENTS.md
  const srcAgents = path.join(bundleDir, 'AGENTS.md');
  const destAgents = path.join(targetDir, 'AGENTS.md');
  fs.copyFileSync(srcAgents, destAgents);
  console.log(' ✔ Created AGENTS.md (Master Constitutional Contract)');

  // 2. Copy .agents/
  const srcAgentsDir = path.join(bundleDir, '.agents');
  const destAgentsDir = path.join(targetDir, '.agents');
  copyRecursiveSync(srcAgentsDir, destAgentsDir);
  console.log(' ✔ Created .agents/ (Full rules, skills library, schemas, and guard engine)');

  // 3. Install Git Hook
  const gitHookInstalled = installGitHook(targetDir);
  if (gitHookInstalled) {
    console.log(' ✔ Armed .git/hooks/pre-commit (Instant 0.04s local commit bouncer)');
  } else {
    console.log(' ℹ️ No .git directory detected; skipped git pre-commit hook.');
  }

  // 4. Install Editor Adapters
  installEditorAdapters(targetDir);
  console.log(' ✔ Configured IDE adapters (.cursor/hooks.json, .cursorrules, .windsurfrules)');

  console.log(`
============================================================
✨ SUCCESS! Your project is now protected by Heisenberg.

Zero project clutter:
• AGENTS.md       <-- The rulebook AI coding agents read
• .agents/        <-- The hidden lab (guard, skills, rules)

To verify workspace compliance at any time, run:
  npx heisenberg-vibecheck validate
============================================================
`);
}

function runValidate(targetDir) {
  const guardScript = path.join(targetDir, '.agents', 'guard.py');
  if (!fs.existsSync(guardScript)) {
    console.error('❌ Error: .agents/guard.py not found. Run "npx heisenberg-vibecheck" first.');
    process.exit(1);
  }

  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
  const result = spawnSync(pythonCmd, [guardScript, 'validate', '--workspace', targetDir], {
    stdio: 'inherit',
    cwd: targetDir
  });

  process.exit(result.status || 0);
}

function runStatus(targetDir) {
  console.log(BANNER);
  const tasksDir = path.join(targetDir, '.agents', 'tasks');
  const artifactsDir = path.join(targetDir, '.agents', 'artifacts');

  if (!fs.existsSync(tasksDir)) {
    console.log('No .agents/tasks directory found. Run "npx heisenberg-vibecheck" to initialize.');
    return;
  }

  const files = fs.readdirSync(tasksDir).filter(f => f.endsWith('.json'));
  if (files.length === 0) {
    console.log('ℹ️  No task manifests found. Heisenberg is in clean bootstrap mode.');
    return;
  }

  console.log(`Found ${files.length} task manifest(s):\n`);
  for (const file of files) {
    try {
      const data = JSON.parse(fs.readFileSync(path.join(tasksDir, file), 'utf-8'));
      const statusIcon = data.status === 'complete' ? '✅' : '⏳';
      console.log(`${statusIcon} ${data.task_id || file}: ${data.title || 'Untitled'} [Status: ${data.status || 'unknown'}]`);
      
      const taskArtifacts = path.join(artifactsDir, data.task_id || '');
      if (fs.existsSync(taskArtifacts)) {
        const artifacts = fs.readdirSync(taskArtifacts);
        console.log(`   Artifacts: ${artifacts.join(', ') || 'none'}`);
      }
      console.log('');
    } catch (_) {
      console.log(`⚠️  ${file}: Invalid JSON`);
    }
  }
}

// Main CLI router
const args = process.argv.slice(2);
const command = args[0] || 'init';
const targetDir = process.cwd();

switch (command) {
  case 'init':
  case 'install':
  case 'unpack':
    unpack(targetDir);
    break;
  case 'validate':
  case 'check':
    runValidate(targetDir);
    break;
  case 'status':
    runStatus(targetDir);
    break;
  case '--help':
  case '-h':
  case 'help':
    console.log(BANNER);
    console.log(`Usage:
  npx heisenberg-vibecheck [command]

Commands:
  init       Unpack Heisenberg OS into the current project (default)
  validate   Validate current workspace against Heisenberg governance
  status     Inspect active tasks and artifact completion
  help       Show this help message
`);
    break;
  default:
    console.log(`Unknown command: ${command}`);
    console.log('Run "npx heisenberg-vibecheck help" for available commands.');
    process.exit(1);
}
