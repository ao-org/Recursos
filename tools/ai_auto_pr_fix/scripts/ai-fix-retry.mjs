import fs from 'fs';
import path from 'path';

const STANDARDS_URL = 'https://raw.githubusercontent.com/ao-org/Recursos/refs/heads/master/tools/ai_context/vb6-coding-standards.md';
const VB6_EXTENSIONS = ['.bas', '.cls', '.frm'];

async function main() {
  const jenkinsUrl = process.env.TARGET_URL || '';
  const jenkinsUser = process.env.JENKINS_USER || '';
  const jenkinsToken = process.env.JENKINS_TOKEN || '';

  // Fetch build log from Jenkins
  let buildLog = '';
  if (jenkinsUrl) {
    const logUrl = jenkinsUrl.replace(/\/$/, '') + '/consoleText';
    const auth = Buffer.from(`${jenkinsUser}:${jenkinsToken}`).toString('base64');
    const logRes = await fetch(logUrl, {
      headers: { 'Authorization': `Basic ${auth}` }
    });
    if (logRes.ok) {
      const fullLog = await logRes.text();
      // Take last 200 lines
      buildLog = fullLog.split('\n').slice(-200).join('\n');
    }
  }

  // Fetch VB6 coding standards
  const standardsRes = await fetch(STANDARDS_URL);
  const standards = await standardsRes.text();

  // Collect current VB6 source files
  const relevantFiles = {};
  collectFiles('.', relevantFiles);

  // Call DeepSeek API (OpenAI-compatible)
  const response = await fetch('https://api.deepseek.com/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.DEEPSEEK_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'deepseek-chat',
      max_tokens: 8192,
      messages: [
        {
          role: 'system',
          content: `You are a VB6 developer fixing build errors in Argentum Online.

Follow these coding standards strictly:

${standards}

The previous code change caused a build failure. Fix the errors shown in the build log.

Return a JSON array of files to modify:
[{"path": "relative/path.bas", "content": "...full file content..."}]

Return ONLY the JSON array, no markdown, no explanation.`
        },
        {
          role: 'user',
          content: `Build failed with these errors:

${buildLog}

Current files:
${JSON.stringify(relevantFiles, null, 2)}`
        }
      ],
    }),
  });

  const result = await response.json();
  const files = JSON.parse(result.choices[0].message.content);

  // Write modified files
  for (const file of files) {
    const dir = path.dirname(file.path);
    if (dir && dir !== '.') {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(file.path, file.content);
  }
}

function collectFiles(dir, result) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === '.git') continue;
      collectFiles(fullPath, result);
    } else if (VB6_EXTENSIONS.some(ext => entry.name.endsWith(ext))) {
      result[fullPath] = fs.readFileSync(fullPath, 'utf-8');
    }
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
