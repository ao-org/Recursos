import fs from 'fs';
import path from 'path';

const STANDARDS_URL = 'https://raw.githubusercontent.com/ao-org/Recursos/refs/heads/master/tools/ai_context/vb6-coding-standards.md';
const VB6_EXTENSIONS = ['.bas', '.cls', '.frm'];

async function main() {
  // Fetch VB6 coding standards
  const standardsRes = await fetch(STANDARDS_URL);
  const standards = await standardsRes.text();

  const issueTitle = process.env.ISSUE_TITLE;
  const issueBody = process.env.ISSUE_BODY;

  // Collect all VB6 source files
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
          content: `${standards}

Return a JSON array of files to modify:
[{"path": "relative/path.bas", "content": "...full file content..."}]

Return ONLY the JSON array, no markdown, no explanation.`
        },
        {
          role: 'user',
          content: `Issue: ${issueTitle}

${issueBody}

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
