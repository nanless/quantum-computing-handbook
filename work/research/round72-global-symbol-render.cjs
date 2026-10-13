// Read-only full-source KaTeX check using the reader's exact extraction expression.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const katex=require(path.join(root,'tools/reader/node_modules/katex'));
function walk(d){return fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(d,e.name)):[path.join(d,e.name)]);}
const files=walk(path.join(root,'handbook')).filter(f=>f.endsWith('.md')).sort();
const results={access_date:'2026-10-13',evidence:'Actual KaTeX rendering of source math fragments, no reader build writes',pages:[],errors:[]};
const pattern=/(^[ \t]*```[^\n]*\n[\s\S]*?^[ \t]*```[^\n]*$)|(`+)[^\n]*?\2|\$\$([\s\S]*?)\$\$|\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)|(?<!\\)\$(?!\$)((?:\\.|[^$\n])+?)(?<!\\)\$/gm;
for(const f of files){const text=fs.readFileSync(f,'utf8');let n=0;const hash=crypto.createHash('sha256').update(text).digest('hex');
text.replace(pattern,(full,fence,ticks,d1,d2,i1,i2)=>{if(fence||ticks)return full;let latex=d1??d2??i1??i2;n++;try{katex.renderToString(latex,{displayMode:d1!==undefined||d2!==undefined,throwOnError:true,strict:'ignore',trust:false,output:'htmlAndMathml'});}catch(e){results.errors.push({file:path.relative(root,f),latex,error:e.message});}return full;});results.pages.push({path:path.relative(root,f),formulas:n,source_sha256:hash});}
results.total_formulas=results.pages.reduce((a,p)=>a+p.formulas,0);fs.writeFileSync(path.join(__dirname,'round72-global-symbol-render.json'),JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify({pages:results.pages.length,formulas:results.total_formulas,errors:results.errors},null,2));if(results.errors.length)process.exitCode=1;
