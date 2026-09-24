// Independent finite-dimensional and probability checks for chapter 12.
// These checks do not constitute a QKD security proof or a device model.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const near = (a,b,tolerance=1e-10) => assert.ok(Math.abs(a-b)<tolerance, `${a} != ${b}`);
const s = Math.SQRT1_2;
const bells = [[s,0,0,s],[s,0,0,-s],[0,s,s,0],[0,s,-s,0]];
const corrections = [[[1,0],[0,1]],[[1,0],[0,-1]],[[0,1],[1,0]],[[0,-1],[1,0]]];
const initial = Array(16).fill(0);
for (const i of [0,3,12,15]) initial[i]=.5;
const average = Array.from({length:4},()=>Array(4).fill(0));
const branches = bells.map((bell,k)=>{
  const projected = Array(4).fill(0);
  for(let a=0;a<2;a++)for(let c=0;c<2;c++)for(let b1=0;b1<2;b1++)for(let b2=0;b2<2;b2++) projected[2*a+c]+=bell[2*b1+b2]*initial[8*a+4*b1+2*b2+c];
  const probability = projected.reduce((sum,x)=>sum+x*x,0);
  near(probability,.25);
  const normalized = projected.map(x=>x/Math.sqrt(probability));
  normalized.forEach((x,i)=>near(x,bell[i]));
  for(let i=0;i<4;i++)for(let j=0;j<4;j++)average[i][j]+=probability*normalized[i]*normalized[j];
  const corrected = Array(4).fill(0);
  for(let a=0;a<2;a++)for(let c=0;c<2;c++)for(let input=0;input<2;input++)corrected[2*a+c]+=corrections[k][c][input]*normalized[2*a+input];
  const overlap = corrected.reduce((sum,x,i)=>sum+x*bells[0][i],0);
  near(overlap*overlap,1);
  return {bell:['Phi+','Phi-','Psi+','Psi-'][k],probability,correctedOverlap:overlap};
});
for(let i=0;i<4;i++)for(let j=0;j<4;j++)near(average[i][j],i===j?.25:0);
const p=.1,q=1-p,a=Math.exp(-1/20);
const closed=p/(2-p)*(1+q*a)/(1-q*a);
let doubleSum=0,weight=0;
for(let x=1;x<500;x++)for(let y=1;y<500;y++){const w=p*p*q**(x+y-2);weight+=w;doubleSum+=w*Math.exp(-Math.abs(x-y)/20);}
near(weight,1);near(doubleSum,closed);
const h = x=>-x*Math.log2(x)-(1-x)*Math.log2(1-x);
const report={generatedAt:new Date().toISOString(),node:process.version,branches,unconditionalState:average,memory:{p,slotMilliseconds:1,effectiveCoherenceMilliseconds:20,meanWaitMilliseconds:2/p-2/(1-q*q),doubleSum,closed,atMean:Math.exp(-(2/p-2/(1-q*q))/20)},bb84:{siftedErrorRate:.5*.5,retainedAndWrongFraction:.5*.5*.5,noErrorsIn20Checks:.75**20,asymptoticRateAtOnePercent:1-2*h(.01),asymptoticRateAtFivePercent:1-2*h(.05)},assertions:'passed'};
const target=fileURLToPath(new URL('../../work/research/network-example-checks.json',import.meta.url));
await fs.writeFile(target,JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
