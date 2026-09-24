import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const near = (a,b,tol=1e-10) => assert.ok(Math.abs(a-b)<tol, `${a} != ${b}`);
const add = (a,b) => [a[0]+b[0],a[1]+b[1]];
const mul = (a,b) => [a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];
const conj = a => [a[0],-a[1]];
const abs2 = a => a[0]**2+a[1]**2;
const reciprocal = a => [a[0]/abs2(a),-a[1]/abs2(a)];
const mv = (m,v) => m.map(row=>row.reduce((s,x,j)=>add(s,mul(x,v[j])),[0,0]));
const inner = (a,b) => a.reduce((s,x,j)=>add(s,mul(conj(x),b[j])),[0,0]);
const H = [[[1/Math.SQRT2,0],[1/Math.SQRT2,0]],[[1/Math.SQRT2,0],[-1/Math.SQRT2,0]]];
const interference=[];
for(const phi of [0,Math.PI/2,Math.PI,Math.PI/3]) {
  const split=mv(H,[[1,0],[0,0]]);
  split[1]=mul(split[1],[Math.cos(phi),Math.sin(phi)]);
  const p=mv(H,split).map(abs2);
  near(p[0],(1+Math.cos(phi))/2); near(p[0]+p[1],1);
  interference.push({phi,probabilities:p});
}
const X=[[[0,0],[1,0]],[[1,0],[0,0]]];
// Trace out a normalized two-state path record, then recombine both paths.
const partialRecords=[];
for (const gamma of [0,.6,1]) for (const phase of [0,Math.PI/3]) {
  const d0=[[1,0],[0,0]],d1=[[gamma,0],[Math.sqrt(1-gamma*gamma),0]];
  const phaseFactor=[Math.cos(phase),Math.sin(phase)];
  const output0=d0.map((a,j)=>mul([.5,0],add(a,mul(phaseFactor,d1[j]))));
  const output1=d0.map((a,j)=>mul([.5,0],add(a,mul([-1,0],mul(phaseFactor,d1[j])))));
  const p0=output0.reduce((s,a)=>s+abs2(a),0),p1=output1.reduce((s,a)=>s+abs2(a),0);
  near(p0,(1+gamma*Math.cos(phase))/2);near(p0+p1,1);
  partialRecords.push({gamma,phase,p0,p1});
}
const Z=[[[1,0],[0,0]],[[0,0],[-1,0]]];
const expectation=(a,v)=>inner(v,mv(a,v));
const yp=[[1/Math.SQRT2,0],[0,1/Math.SQRT2]];
near(expectation(X,yp)[0],0); near(expectation(Z,yp)[0],0);
const comm=mv(X,mv(Z,yp)).map((a,i)=>add(a,mul([-1,0],mv(Z,mv(X,yp))[i])));
near(Math.sqrt(abs2(inner(yp,comm)))/2,1);
const realState=[[Math.cos(Math.PI/8),0],[Math.sin(Math.PI/8),0]];
near((1-expectation(X,realState)[0]**2),.5);
near((1-expectation(Z,realState)[0]**2),.5);

function integrate(f,a,b,n=20000) {
  const h=(b-a)/n;
  let sum=f(a)+f(b);
  for(let i=1;i<n;i++)sum+=(i%2?4:2)*f(a+i*h);
  return sum*h/3;
}
const phi=(n,x)=>Math.SQRT2*Math.sin(n*Math.PI*x);
near(integrate(x=>phi(1,x)**2,0,1),1);
near(integrate(x=>phi(2,x)**2,0,1),1);
near(integrate(x=>phi(1,x)*phi(2,x),0,1),0);
const middle=integrate(x=>phi(1,x)**2,.25,.75);
near(middle,.5+1/Math.PI);
const leftPlus=integrate(x=>(phi(1,x)+phi(2,x))**2/2,0,.5);
const leftMinus=integrate(x=>(phi(1,x)-phi(2,x))**2/2,0,.5);
near(leftPlus,.5+4/(3*Math.PI)); near(leftMinus,.5-4/(3*Math.PI));
// Dimensionless oscillator: m = omega = hbar = 1; integrate Gaussian independently.
const gaussian=x=>Math.PI**(-.25)*Math.exp(-x*x/2);
const norm=integrate(x=>gaussian(x)**2,-10,10);
const x2=integrate(x=>x*x*gaussian(x)**2,-10,10);
const p2=integrate(x=>(x*gaussian(x))**2,-10,10);
near(norm,1); near(x2,.5); near(p2,.5);

const barriers=[];
for(const E of [.2,.5,.8]) for(const L of [.5,2,6]) {
  // Units: hbar^2/(2m)=1, V0=1. Match both wavefunction and derivative.
  const k=Math.sqrt(E),kap=Math.sqrt(1-E),C=Math.cosh(kap*L),S=Math.sinh(kap*L);
  const F=reciprocal([C,.5*(kap/k-k/kap)*S]);
  const r=add(mul(F,[C,-k/kap*S]),[-1,0]);
  const derivativeLeft=mul([0,k],add([1,0],mul([-1,0],r)));
  const derivativeBarrier=mul(F,[-kap*S,k*C]);
  near(derivativeLeft[0],derivativeBarrier[0]); near(derivativeLeft[1],derivativeBarrier[1]);
  const T=abs2(F),R=abs2(r),closed=1/(1+S*S/(4*E*(1-E)));
  near(T,closed); near(T+R,1);
  barriers.push({E,L,T,R});
}
const h=6.62607015e-34,kB=1.380649e-23,f=5e9;
const thermal=[.020,300].map(T=>{const ratio=Math.exp(-h*f/(kB*T));return {kelvin:T,excitedToGround:ratio,excitedProbability:ratio/(1+ratio)}});
near(thermal[0].excitedProbability,0.00000615581,1e-11);
near(thermal[1].excitedProbability,.49980003,1e-8);
const omega=2*Math.PI*10e6;
near(Math.sin(omega*25e-9/2)**2,.5);near(Math.sin(omega*50e-9/2)**2,1);
const detuned=[{driveMHz:4,detuningMHz:3,peak:0.64,ns:100},{driveMHz:10,detuningMHz:6,peak:100/136,ns:42.8746462856}].map(v=>{
  const rabiMHz=Math.hypot(v.driveMHz,v.detuningMHz);
  const peak=v.driveMHz**2/rabiMHz**2,ns=500/rabiMHz;
  near(peak,v.peak);near(ns,v.ns,1e-8);return {...v,rabiMHz};
});
const report={generatedAt:new Date().toISOString(),node:process.version,interference,partialRecords,
  uncertainty:{yStateProduct:1,realStateProduct:.5,realStateRobertsonBound:0},
  well:{norms:[1,1],overlap:0,middle,leftPlus,leftMinus},
  oscillator:{norm,x2,p2,uncertaintyProduct:Math.sqrt(x2*p2)},barriers,
  barrierExamples:{kappaL1:1/Math.cosh(1)**2,bareExponential:Math.exp(-2),kappaL3:1/Math.cosh(3)**2,thickApproximation:4*Math.exp(-6)},
  thermal,rabi:{megahertz:10,halfPopulationNanoseconds:25,inversionNanoseconds:50,detuned},assertions:'passed'};
await fs.writeFile(path.join(root,'work/research/qm-example-checks.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
