import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const read=rel=>fs.readFile(path.join(root,rel),'utf8');
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
const groups={foundations:['00','01','02','03','04','05','q1','q2'],algorithms:['06','07','08','13','16','17','18','q4'],systems:['09','10','11','12','14','15','19','q3']};
const main=await fs.readdir(path.join(root,'handbook')),qm=await fs.readdir(path.join(root,'handbook/quantum-mechanics'));
const errors=[],chapters=[],labels=new Set(),labs=await read('handbook/labs/README.md');
for(const [group,ids]of Object.entries(groups))for(const id of ids){
 const file=id.startsWith('q')?'handbook/quantum-mechanics/'+qm.find(f=>f.startsWith('0'+id[1]+'-')):'handbook/'+main.find(f=>f.startsWith(id+'-'));
 const label=({foundations:'F',algorithms:'A',systems:'S'}[group])+'72-'+id.toUpperCase();
 const text=await read(file);
 for(const match of text.matchAll(/[FAS]72-(?:Q[1-4]|\d{2})(?:[a-cA-C])?/g))labels.add(match[0]);
 if(!text.includes(label)||!labs.includes(label))errors.push(`${file}: missing chapter/labs ${label}`);
 const script=`codes/${group}/${group==='foundations'?'round72_stdlib.py':'round72_checks.py'}`;
 chapters.push({id,label,file,sourceSha256:digest(text),script,scriptSha256:digest(await read(script))});
}
const workflows=JSON.parse(await read('codes/sdk/workflows/results-all.json'));
if(workflows.records.length!==9||workflows.records.some(r=>r.status!=='passed'))errors.push('Workflow SDK cases incomplete');
const foundations=JSON.parse(await read('codes/foundations/sdk/all-results.json'));
if(Object.keys(foundations.cases).length!==3||Object.values(foundations.cases).some(r=>r.status!=='passed'))errors.push('Foundation SDK cases incomplete');
const algorithms=JSON.parse(await read('codes/algorithms/sdk/round72-results.json'));
if(Object.keys(algorithms.cases).length!==8)errors.push('Algorithm SDK cases incomplete');
for(const [name,value]of Object.entries(algorithms.cases))if(value.status && value.status!=='passed')errors.push(`Algorithm ${name} failed`);
for(const file of ['stim-matching-results.json','grape-results.json','sequence-results.json','saved-results-verification.json']){
 const value=JSON.parse(await read('codes/systems/sdk/'+file));
 if(value.status!=='passed')errors.push(`System ${file} failed`);
}
const hpc=JSON.parse(await read('codes/sdk/hpc/results.json'));
if(hpc.status!=='passed')errors.push('HPC driver failed');
const testlog=await read('codes/sdk/hpc/upstream-tests.log');
if(!/49\s*\|\s*49 passed/.test(testlog)||!/36652\s*\|\s*36652 passed/.test(testlog))errors.push('HPC upstream tests absent');
const oqs=JSON.parse(await read('codes/systems/sdk/liboqs-build-run.json'));
if(oqs.algorithms.length!==3||oqs.algorithms.some(a=>a.valid_roundtrips!==10||a.tampered_different_secrets!==10))errors.push('ML-KEM evidence absent');
const vendor=JSON.parse(await read('codes/vendor/manifest.json'));
const projectNames=vendor.projects.map(p=>p.name);
const installed=[...workflows.records.flatMap(r=>r.checks.packages),'qiskit-aer','qiskit-experiments','qutip',...Object.keys(algorithms.cases),'stim','pymatching','qutip-qtrl','sequence','liboqs','qiskit-addon-sqd-hpc'];
if(new Set(installed).size!==26||projectNames.some(p=>!installed.includes(p)))errors.push('26 complete projects coverage mismatch');
const sdkText=await read('handbook/labs/sdk-validation.md');
for(const label of ['IAE','OBP','CUT','MPF','GST','HPC'])if(!sdkText.includes('R72-'+label))errors.push('Missing workflow exercise '+label);
const evidenceFiles=['codes/foundations/sdk/all-results.json','codes/algorithms/sdk/round72-results.json','codes/sdk/workflows/results-all.json','codes/systems/sdk/stim-matching-results.json','codes/systems/sdk/grape-results.json','codes/systems/sdk/sequence-results.json','codes/systems/sdk/liboqs-build-run.json','codes/sdk/hpc/results.json','codes/sdk/hpc/upstream-tests.log'];
const evidence=[];for(const file of evidenceFiles)evidence.push({file,sha256:digest(await fs.readFile(path.join(root,file)))});
const report={generatedAt:new Date().toISOString(),scope:'24 chapter groups, six integration exercises, 26 complete installed/built projects with explicit CPU-task limits',chapters,chapterExerciseLabels:[...labels].sort(),workflowExerciseGroups:6,completeProjects:[...new Set(installed)].sort(),evidence,errors};
await fs.writeFile(path.join(root,'work/research/round72-inventory.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({chapters:chapters.length,completeProjects:report.completeProjects.length,errors},null,2));
if(errors.length)process.exitCode=1;
