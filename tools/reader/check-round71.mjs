import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const groups = {
  foundations: ['00','01','02','03','04','05','q1','q2'],
  algorithms: ['06','07','08','13','16','17','18','q4'],
  systems: ['09','10','11','12','14','15','19','q3']
};
const prefix = {foundations:'F', algorithms:'A', systems:'S'};
const chapters = (await fs.readdir(path.join(root,'handbook'))).filter(f=>/^\d\d-.+\.md$/.test(f));
const qm = (await fs.readdir(path.join(root,'handbook/quantum-mechanics'))).filter(f=>/^\d\d-.+\.md$/.test(f));
const labs = await fs.readFile(path.join(root,'handbook/labs/README.md'),'utf8');
const errors = [], entries = [];
for (const [group, ids] of Object.entries(groups)) {
  const script = `codes/${group}/round71_checks.py`;
  const code = await fs.readFile(path.join(root,script));
  for (const id of ids) {
    const isQM = id.startsWith('q');
    const file = isQM ? 'handbook/quantum-mechanics/' + qm.find(f=>f.startsWith('0'+id[1]+'-'))
      : 'handbook/' + chapters.find(f=>f.startsWith(id+'-'));
    const label = `${prefix[group]}71-${id.toUpperCase()}`;
    const bytes = await fs.readFile(path.join(root,file));
    if (!bytes.toString().includes(label)) errors.push(`${file}: missing ${label}`);
    if (!labs.includes(label)) errors.push(`labs index missing ${label}`);
    if (!bytes.toString().includes('round71_checks.py')) errors.push(`${file}: missing code entry`);
    entries.push({id,label,file,sourceSha256:hash(bytes),script,scriptSha256:hash(code)});
  }
}
const sourcePractice = await fs.readFile(path.join(root,'handbook/appendices/software-practice.md'),'utf8');
for (const label of ['MPF','OBP','NOISE','SQD','RNG','TOMO']) {
  if (!sourcePractice.includes('S71-'+label)) errors.push('software practice missing S71-'+label);
}
const manifest = JSON.parse(await fs.readFile(path.join(root,'codes/vendor/manifest.json'),'utf8'));
const projects=manifest.projects.length, files=manifest.projects.reduce((n,p)=>n+p.files.length,0);
if (projects !== 26 || files !== 97) errors.push(`unexpected vendor scope ${projects}/${files}`);
for (const file of ['handbook/README.md','handbook/appendices/software-practice.md','codes/vendor/README.md']) {
  const text=await fs.readFile(path.join(root,file),'utf8');
  if (!/26\s*个?项目/.test(text) || !/97\s*份?(?:文件|源码)/.test(text)) errors.push(`${file}: current source counts not synchronized`);
}
const report={generatedAt:new Date().toISOString(),scope:'24 chapter labels and code links; six workflow exercises; source scope synchronization',
  chapters:entries, workflowExerciseGroups:6,projects,files,errors};
await fs.writeFile(path.join(root,'work/research/round71-inventory.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({chapters:entries.length,workflowExerciseGroups:6,projects,files,errors},null,2));
if(errors.length)process.exitCode=1;
