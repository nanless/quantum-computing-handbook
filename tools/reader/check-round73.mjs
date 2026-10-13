import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const read=rel=>fs.readFile(path.join(root,rel),'utf8'),digest=b=>crypto.createHash('sha256').update(b).digest('hex');
const groups={foundations:['00','01','02','03','04','05','q1','q2'],algorithms:['06','07','08','13','16','17','18','q4'],systems:['09','10','11','12','14','15','19','q3']};
const main=await fs.readdir(path.join(root,'handbook')),qm=await fs.readdir(path.join(root,'handbook/quantum-mechanics'));
const errors=[],chapters=[],labels=new Set(),labs=await read('handbook/labs/README.md');
for(const [group,ids]of Object.entries(groups))for(const id of ids){
 const file=id.startsWith('q')?'handbook/quantum-mechanics/'+qm.find(f=>f.startsWith('0'+id[1]+'-')):'handbook/'+main.find(f=>f.startsWith(id+'-'));
 const label=({foundations:'F',algorithms:'A',systems:'S'}[group])+'73-'+id.toUpperCase(),text=await read(file);
 for(const match of text.matchAll(/[FAS]73-(?:Q[1-4]|\d{2})(?:[ab])?/g))labels.add(match[0]);
 if(!text.includes(label)||!labs.includes(label))errors.push(`${file}: missing chapter/labs ${label}`);
 const script=`codes/${group}/round73_checks.py`;
 chapters.push({id,label,file,sourceSha256:digest(text),script,scriptSha256:digest(await read(script))});
}
const files=['codes/foundations/sdk73/all-results.json','codes/algorithms/sdk73/results-all.json','codes/systems/sdk73/qec-grid-results.json','codes/systems/sdk73/grape-three-results.json','codes/systems/sdk73/sequence-entanglement-results.json','codes/sdk/round73/dynamic-mpf-results.json','codes/sdk/round73/gst-long-results.json','codes/sdk/round73/pna-results.json','codes/sdk/round73/slc-results.json','codes/sdk/round73/hpc/results.json','codes/sdk/round73/saved-checks.json'];
const evidence=[];
for(const file of files){const bytes=await fs.readFile(path.join(root,file)),value=JSON.parse(bytes);if(value.status && value.status!=='passed')errors.push(file+' failed');if(value.cases&&!Array.isArray(value.cases))for(const [key,entry]of Object.entries(value.cases))if(entry.status&&entry.status!=='passed')errors.push(file+': '+key+' failed');evidence.push({file,sha256:digest(bytes)});}
const foundation=JSON.parse(await read(files[0])),algorithm=JSON.parse(await read(files[1]));
if(Object.keys(foundation.cases).length!==4 || Object.keys(algorithm.cases).length!==4)errors.push('four foundation/algorithm workflows absent');
const qec=JSON.parse(await read(files[2]));if(qec.cases.length!==18||qec.controls.length!==2)errors.push('QEC 18 points/two controls absent');
const vendor=JSON.parse(await read('codes/vendor/manifest.json'));
const old=JSON.parse(execFileSync('git',['show','d7f43107568fcaa0daa1e15972e14f715d0385d9:codes/vendor/manifest.json'],{cwd:root,encoding:'utf8'}));
if(vendor.projects.length!==31 || vendor.projects.reduce((n,p)=>n+p.files.length,0)!==122)errors.push('31 projects/122 files mismatch');
for(const p of old.projects){const current=vendor.projects.find(q=>q.name===p.name);if(JSON.stringify(current)!==JSON.stringify(p))errors.push('historical manifest changed '+p.name);for(const f of p.files)if(digest(await fs.readFile(path.join(root,'codes/vendor',p.name,f.path)))!==f.sha256)errors.push('historical bytes changed '+p.name+'/'+f.path);}
const text=await read('handbook/labs/sdk-validation.md');for(const label of ['MPF','SLC','PNA','GST','HPC'])if(!text.includes('R73-'+label))errors.push('integration exercise missing '+label);
const defaults=JSON.parse(await read('work/research/code-validation.json'));if(defaults.checks.length!==34||defaults.checks.some(c=>c.returncode!==0))errors.push('34 actual stdlib checks absent');
const report={generatedAt:new Date().toISOString(),baseline:'d7f43107568fcaa0daa1e15972e14f715d0385d9',scope:'24 chapters; new SDK tasks and independent saved checks, not all upstream functionality',chapters,chapterExerciseLabels:[...labels].sort(),integrationExerciseGroups:5,vendorProjects:31,vendorFiles:122,preservedHistoricalProjects:26,preservedHistoricalFiles:97,evidence,errors};
await fs.writeFile(path.join(root,'work/research/round73-inventory.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({chapters:chapters.length,chapterExerciseLabels:labels.size,errors},null,2));if(errors.length)process.exitCode=1;
