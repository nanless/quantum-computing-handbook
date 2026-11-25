import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const read = f => fs.readFile(path.join(root, f), 'utf8');
const answers = await read('handbook/appendices/exercises.md');
const answerSections = answers.split(/^## /m).slice(1);
const files = [];
for (const dir of ['handbook', 'handbook/quantum-mechanics']) {
  for (const f of (await fs.readdir(path.join(root,dir))).sort()) if (/^\d\d-.*\.md$/.test(f)) files.push(dir+'/'+f);
}
const counts = [];
let foundationArchivesAligned = 0;
for (const file of files) {
  const t = await read(file);
  const section = t.split(/^## /m).find(s=>/^.*自检/.test(s)).split('\n').slice(1).join('\n');
  const nums = [...section.matchAll(/^(\d+)\. /gm)].map(m=>Number(m[1]));
  assert.ok(nums.every((n,i)=>n===i+1),file+' question order');
  const chapter = Number(path.basename(file).slice(0,2));
  const title = file.includes('/quantum-mechanics/') ? '量子力学 Q'+chapter : '第 '+chapter+' 章';
  const answer = answerSections.find(s=>s.split('\n')[0]===title);
  assert.ok(answer,title+' missing answers');
  const answerNums = [...answer.matchAll(/^(\d+)\. /gm)].map(m=>Number(m[1]));
  assert.deepEqual(answerNums,nums,title+' answer order');
  if (file.includes('/quantum-mechanics/')) {
    // Keep historical round31 archives untouched and verify their question numbering
    // without freezing exercises.md byte-for-byte against the round31 draft text.
    const draft = await read(`work/research/round31-qm${chapter}-answers.md`);
    const draftNums = [...draft.matchAll(/^(\d+)\. /gm)].map(m=>Number(m[1]));
    assert.deepEqual(draftNums,nums,title+' historical archive question order differs');
    foundationArchivesAligned++;
  }
  counts.push({file,questions:nums.length,answers:nums.length});
}
const q1 = await read('handbook/quantum-mechanics/01-experiments-states.md');
const q1Answer = answerSections.find(s=>s.startsWith('量子力学 Q1\n'));
const q2Answer = answerSections.find(s=>s.startsWith('量子力学 Q2\n'));
const q3Answer = answerSections.find(s=>s.startsWith('量子力学 Q3\n'));
const q4Answer = answerSections.find(s=>s.startsWith('量子力学 Q4\n'));
assert.ok(!q1.includes('\\chi')&&!q1Answer.includes('\\chi'));
assert.ok(q1.includes('\\theta_{\\rm g}')&&q1Answer.includes('\\theta_{\\rm g}'));
assert.ok(q1.includes('完全可区分')&&q1.includes('0.6')&&q1Answer.includes('0.8'));
assert.ok(q1.includes('#4-局部操作不能单独揭示整个纠缠态'));
const foundationMathChecks = [
  ['Q1 key results', /3\/4|\\frac\{?3\}?\{?4\}?/.test(q1Answer) && q1Answer.includes('1000') && q1Answer.includes('0.2')],
  ['Q2 key results', /Cauchy[–-]Schwarz/.test(q2Answer) && q2Answer.includes('Robertson') && /3\/2|\\frac\{?3\}?\{?2\}?/.test(q2Answer) && /20(?:\\ |\\,|\s)*\\mathrm\{ns\}/.test(q2Answer)],
  ['Q3 key results', q3Answer.includes('0.288') && q3Answer.includes('0.0211') && q3Answer.includes('250') && q3Answer.includes('0.64') && /100(?:\\ |\\,|\s)*\\mathrm\{ns\}/.test(q3Answer) && q3Answer.includes('0.3') && q3Answer.includes('|10\\rangle') && q3Answer.includes('|01\\rangle')],
  ['Q4 key results', q4Answer.includes('0.8183') && q4Answer.includes('0.9244') && q4Answer.includes('0.0756') && /\\sqrt\{?3\}?/.test(q4Answer) && /\\hbar\/2|\\frac\{\\hbar\}\{2\}/.test(q4Answer) && q4Answer.includes('0.419974')],
];
for (const [label, ok] of foundationMathChecks) assert.ok(ok, label + ' missing expected math/symbol check');
const add = (a,b)=>[a[0]+b[0],a[1]+b[1]];
const mul = (a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];
const conj = a=>[a[0],-a[1]];
const abs2 = a=>a[0]**2+a[1]**2;
const psi = [[1/Math.sqrt(3),1/Math.sqrt(3)],[1/Math.sqrt(3),0]];
const measurements = [[[1,0],[0,0]],[[1/Math.sqrt(2),0],[0,1/Math.sqrt(2)]],[[Math.sqrt(.2),0],[Math.sqrt(.8),0]]];
const probability = (m,v)=>abs2(m.reduce((s,a,i)=>add(s,mul(conj(a),v[i])),[0,0]));
let phaseChecks = 0;
for(const theta of [-3,-1,0,.2,1,2,Math.PI])for(const m of measurements){
  const shifted = psi.map(a=>mul([Math.cos(theta),Math.sin(theta)],a));
  assert.ok(Math.abs(probability(m,psi)-probability(m,shifted))<1e-12);
  phaseChecks++;
}
const report = {generatedAt:new Date().toISOString(),reviewer:'primary agent',chapters:counts.length,
  questions:counts.reduce((s,c)=>s+c.questions,0),answers:counts.reduce((s,c)=>s+c.answers,0),
  foundationArchivesAligned,foundationMathChecks:foundationMathChecks.length,
  globalPhaseProbabilityChecks:phaseChecks,counts,status:'passed'};
await fs.writeFile(path.join(root,'work/research/qm-question-inventory.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({...report,counts:undefined},null,2));
