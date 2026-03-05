#!/usr/bin/env node
// memory-stack/pre-task-checker.js
// MANDATORY enforcement: check corrections BEFORE similar tasks
// Blocks task start if corrections exist but weren't reviewed
// Usage: node pre-task-checker.js "task description"
//        node pre-task-checker.js --force "task description" (bypass enforcement for non-critical tasks)

const fs = require('fs');
const path = require('path');
const { callHaiku, log, today } = require('./lib');
const cfg = require('./config');

const PROCESS = 'pre-task-checker';
const CORRECTIONS_FILE = path.join(cfg.MEMORY_DIR, 'corrections.md');
const ACKNOWLEDGMENTS_FILE = path.join(cfg.MEMORY_DIR, 'correction-acknowledgments.md');

async function getRelevantCorrections(taskDescription) {
  if (!fs.existsSync(CORRECTIONS_FILE)) return { relevant: [], allCount: 0 };

  const corrections = fs.readFileSync(CORRECTIONS_FILE, 'utf8');
  const allLines = corrections.split('\n').filter(l => l.trim()).length;

  if (corrections.length < 50) {
    return { relevant: [], allCount: allLines };
  }

  try {
    const response = await callHaiku(
      `You are a pre-task checker for an AI assistant (Alo).
Before Alo starts a task, you must identify which past corrections apply.

Task Alo is about to do: "${taskDescription}"

Past corrections and rules (most recent first):
${corrections.slice(0, 8000)}

Return ONLY the corrections/rules that apply to this specific task.
Format each as a bullet: - [rule or correction]
If NONE apply, return: NONE`,
      ''
    );

    const relevant = response.includes('NONE') 
      ? [] 
      : response.split('\n').filter(line => line.trim().startsWith('-')).map(line => line.substring(1).trim());

    return { relevant, allCount: allLines };
  } catch(e) {
    log(PROCESS, `Relevance check failed: ${e.message}`);
    return { relevant: [], allCount: allLines };
  }
}

async function checkIfAcknowledged(taskDescription) {
  if (!fs.existsSync(ACKNOWLEDGMENTS_FILE)) return false;

  const acks = fs.readFileSync(ACKNOWLEDGMENTS_FILE, 'utf8');
  // Check if task type was acknowledged today
  const taskHash = taskDescription.split(' ').slice(0, 3).join(' ').toLowerCase();
  return acks.toLowerCase().includes(taskHash);
}

async function recordAcknowledgment(taskDescription) {
  const taskHash = taskDescription.split(' ').slice(0, 3).join(' ').toLowerCase();
  if (!fs.existsSync(ACKNOWLEDGMENTS_FILE)) {
    fs.writeFileSync(ACKNOWLEDGMENTS_FILE, '# Correction Acknowledgments\n*Auto-updated when Alo acknowledges past corrections before starting a task*\n\n');
  }
  fs.appendFileSync(ACKNOWLEDGMENTS_FILE, `- [${today()}] Acknowledged corrections before: "${taskDescription}"\n`);
}

async function enforceCheck(taskDescription, isForced = false) {
  const { relevant, allCount } = await getRelevantCorrections(taskDescription);

  if (!relevant.length) {
    console.log('\n✅ PRE-TASK CHECK: No past corrections apply to this task.\n');
    return { passed: true, corrections: [], reason: 'no-relevant' };
  }

  // Corrections DO apply to this task
  const alreadyAcknowledged = await checkIfAcknowledged(taskDescription);

  if (alreadyAcknowledged && !isForced) {
    // Already reviewed today, allow task
    console.log('\n✅ PRE-TASK CHECK: Corrections already reviewed today. Proceed.\n');
    return { passed: true, corrections: relevant, reason: 'already-acknowledged' };
  }

  // NEW corrections found or forced bypass requested
  console.log('\n🚨 PRE-TASK CHECK: CORRECTIONS APPLY TO THIS TASK\n');
  console.log(`Task: "${taskDescription}"\n`);
  console.log('📋 RELEVANT PAST CORRECTIONS:\n');

  for (const correction of relevant) {
    console.log(`  ⚠️  ${correction}`);
  }

  if (isForced) {
    console.log('\n⏭️  FORCED BYPASS: --force used. Proceeding without enforcement.\n');
    return { passed: true, corrections: relevant, reason: 'forced-bypass', enforcement: 'bypassed' };
  }

  // MANDATORY enforcement mode
  console.log('\n' + '='.repeat(60));
  console.log('🔴 TASK BLOCKED: Corrections must be reviewed before proceeding.');
  console.log('='.repeat(60) + '\n');

  console.log(`To proceed, Alo MUST:
1. Read the corrections above
2. Acknowledge: "--ack" flag when restarting
3. Apply these rules in your work

If you bypass via --force, you accept responsibility for repeating these mistakes.

RESTART WITH:
  node pre-task-checker.js --ack "${taskDescription}"\n`);

  return { passed: false, corrections: relevant, reason: 'enforcement-required', blocked: true };
}

// CLI Entry Point
const args = process.argv.slice(2);
const isForced = args[0] === '--force';
const isAck = args[0] === '--ack';
const offset = isForced || isAck ? 1 : 0;
const taskDesc = args.slice(offset).join(' ');

if (!taskDesc) {
  console.log('Usage: node pre-task-checker.js "task description"');
  console.log('       node pre-task-checker.js --ack "task description" (acknowledge corrections)');
  console.log('       node pre-task-checker.js --force "task description" (bypass enforcement)');
  console.log('\nExample: node pre-task-checker.js "build a dashboard UI"');
  process.exit(1);
}

if (isAck) {
  recordAcknowledgment(taskDesc).then(() => {
    console.log('\n✅ Corrections acknowledged. You may proceed with the task.\n');
  }).catch(e => console.error('Failed to record acknowledgment:', e.message));
} else {
  enforceCheck(taskDesc, isForced).then(result => {
    if (!result.passed && result.blocked) {
      process.exit(1); // Block task via non-zero exit
    }
  }).catch(e => {
    console.error('Pre-task check failed:', e.message);
    process.exit(1);
  });
}
