// Real-parser validation. Setup: npm i mermaid@11 jsdom  |  Run: node validate_mermaid.mjs file.md [...]
// Checks every ```mermaid block with the official Mermaid parser (syntax only, no render).
import { JSDOM } from 'jsdom';
import fs from 'fs';
const dom = new JSDOM('<!DOCTYPE html><body></body>');
globalThis.window = dom.window; globalThis.document = dom.window.document;
const mermaid = (await import('mermaid')).default;
mermaid.initialize({ startOnLoad:false });
let bad = 0;
for (const f of process.argv.slice(2)) {
  const t = fs.readFileSync(f,'utf8');
  const bl = [...t.matchAll(/```mermaid\n([\s\S]*?)```/g)].map(m=>m[1]);
  for (const [i,b] of bl.entries()) {
    try { await mermaid.parse(b); console.log('OK  ', f, i+1); }
    catch(e){ bad++; console.log('FAIL', f, i+1, String(e.message).slice(0,200)); }
  }
}
process.exit(bad?1:0);
