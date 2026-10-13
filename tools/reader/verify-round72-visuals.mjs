import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
import {closeBrowser} from './browser-cleanup.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../..');
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const browser=await chromium.launch({headless:true,...(process.env.HANDBOOK_CHROMIUM?{executablePath:process.env.HANDBOOK_CHROMIUM}:{})});
const out=path.join(root,'work/rendered');await fs.mkdir(out,{recursive:true});
const inventory=JSON.parse(await fs.readFile(path.join(root,'work/research/round72-inventory.json'),'utf8'));
const report={generatedAt:new Date().toISOString(),chapterContexts:[],figures:[],errors:[],manualInspection:'separate human/model image review; generation alone is not manual acceptance'};
const figures=[
 ['round72-foundations-trajectories.svg','quantum-mechanics/02-observables-dynamics.html'],
 ['round72-algorithms.svg','16-advanced-algorithms-verification.html'],
 ['round72-systems-qec.svg','10-error-correction.html'],
 ['round72-systems-control.svg','14-compilation-control.html']
];
try{
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:1000},deviceScaleFactor:1});
  for(const entry of inventory.chapters){
   const rel=entry.file.replace(/^handbook\//,'').replace(/\.md$/,'.html');
   await page.goto(pathToFileURL(path.join(root,'reader',rel)).href);
   await page.evaluate(async()=>{await document.fonts.ready;document.documentElement.style.scrollBehavior='auto';if(innerWidth<760)document.querySelector('.chapters details').open=false;for(const img of document.images){img.loading='eager';await img.decode().catch(()=>{});}});
   const target=page.locator('article h3,article strong').filter({hasText:entry.label}).first();
   if(!(await target.count())){report.errors.push({file:rel,message:'exercise target absent'});continue;}
   await target.evaluate(e=>window.scrollTo({top:e.getBoundingClientRect().top+window.scrollY-140,behavior:'instant'}));
   await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
   const screenshot=`round72-${entry.id}-${width}.png`;
   await page.screenshot({path:path.join(out,screenshot)});
   report.chapterContexts.push({file:rel,width,label:entry.label,screenshot:'work/rendered/'+screenshot});
  }
  for(const [asset,rel] of figures){
   await page.goto(pathToFileURL(path.join(root,'reader',rel)).href);
   await page.evaluate(async()=>{await document.fonts.ready;document.documentElement.style.scrollBehavior='auto';if(innerWidth<760)document.querySelector('.chapters details').open=false;for(const img of document.images){img.loading='eager';await img.decode().catch(()=>{});}});
   const image=page.locator(`img[src$="${asset}"]`);
   await image.scrollIntoViewIfNeeded();await page.evaluate(()=>window.scrollBy(0,-120));
   const screenshot=`round72-context-${asset.replace('.svg','')}-${width}.png`;
   await page.screenshot({path:path.join(out,screenshot)});
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2);
   if(overflow)report.errors.push({file:rel,width,message:'context page overflow'});
   report.figures.push({asset,context:rel,width,screenshot:'work/rendered/'+screenshot});
  }
  await page.close();
 }
 const page=await browser.newPage({viewport:{width:1200,height:800},deviceScaleFactor:1});
 for(const [asset]of figures){
  await page.goto(pathToFileURL(path.join(root,'reader/assets',asset)).href);await page.evaluate(()=>document.fonts.ready);
  const screenshot=`round72-full-${asset.replace('.svg','')}.png`;
  await page.locator('svg').screenshot({path:path.join(out,screenshot)});
  report.figures.push({asset,original:true,screenshot:'work/rendered/'+screenshot});
 }
 await page.close();
}catch(error){report.errors.push({message:String(error)});throw error;}
finally{
 await fs.writeFile(path.join(root,'work/research/round72-visual-checks.json'),JSON.stringify(report,null,2)+'\n');
 if(report.errors.length)process.exitCode=1;
 console.log(JSON.stringify({chapterContexts:report.chapterContexts.length,figureScreenshots:report.figures.length,errors:report.errors}));
 await closeBrowser(browser);
}
