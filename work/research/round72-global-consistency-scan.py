"""Source-wide symbol/structure inventory; does not claim semantic proof or full reread."""
import collections,json,pathlib,re
root=pathlib.Path(__file__).resolve().parents[2]
chapters=sorted((root/'handbook').glob('[0-9][0-9]-*.md'))+sorted((root/'handbook/quantum-mechanics').glob('[0-9][0-9]-*.md'))
appendices=sorted((root/'handbook/appendices').glob('*.md'))
extras=[root/'handbook/labs/sdk-validation.md',root/'handbook/README.md',root/'handbook/quantum-mechanics/README.md']
files=sorted((root/'handbook').rglob('*.md'))
keys={'Gamma':r'\\Gamma\b','gamma':r'\\gamma\b','Favg':r'F_.*(?:avg|av)|Favg','hbar':r'\\hbar\b|hbar','CV_order':r'xxpp|交错|排序|多模','H_roles':r'Hadamard|Hamiltonian|哈密顿量|Shannon','bit_order':r'小端|大端|端序|基序|基顺序|高位|低位|qubit_order'}
rows=[]; issues=[]; suspects=[]
for p in files:
    text=p.read_text(); lines=text.splitlines(); active=[]; fence=False; headings=[]
    for i,line in enumerate(lines):
        if re.match(r'^\s*(```|~~~)',line): fence=not fence; continue
        if fence: continue
        active.append((i+1,line))
        match=re.match(r'^(#{1,6})\s+(.+)',line)
        if match:
            level=len(match[1]);headings.append({'line':i+1,'level':level,'title':match[2]})
            if i and lines[i-1].strip(): issues.append({'path':str(p.relative_to(root)),'line':i+1,'type':'heading_missing_blank_before'})
            if i+1<len(lines) and lines[i+1].strip(): issues.append({'path':str(p.relative_to(root)),'line':i+1,'type':'heading_missing_blank_after'})
        if line.strip()=='$$':
            # Display math body is free to immediately follow a delimiter.
            pass
    if fence: issues.append({'path':str(p.relative_to(root)),'type':'unclosed_code_fence'})
    delimiters=[i for i,line in active if line.strip()=='$$']
    if len(delimiters)%2: issues.append({'path':str(p.relative_to(root)),'type':'odd_display_math_delimiters'})
    for prev,next_ in zip(headings,headings[1:]):
        if next_['level']>prev['level']+1: suspects.append({'path':str(p.relative_to(root)),'line':next_['line'],'type':'heading_level_jump','prev':prev,'next':next_})
    duplicate=[s for s,n in collections.Counter(h['title'] for h in headings).items() if n>1]
    body='\n'.join(s for _,s in active)
    mentions={k:[{'line':n,'text':line[:350]} for n,line in active if re.search(expr,line)] for k,expr in keys.items()}
    bad=[]; local=[]
    # Match ordinary source Markdown targets. URI links are excluded; real anchor semantics belongs to reader verifier.
    for m in re.finditer(r'!?\[[^\]\n]*\]\(([^\s\n()]+)(?:\s+"[^"\n]*")?\)',text):
        target=m[1].strip('<>'); path=target.split('#',1)[0].split('?',1)[0]
        if not path or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',path): continue
        dest=p.parent/path
        local.append(target)
        if not dest.exists(): bad.append({'target':target,'line':text[:m.start()].count('\n')+1})
    if bad: issues.extend({'path':str(p.relative_to(root)),'type':'missing_local_target',**b} for b in bad)
    rows.append({'path':str(p.relative_to(root)),'lines':len(lines),'headings':headings,'duplicate_heading_titles':duplicate,'display_math_pairs':len(delimiters)//2,'code_fence_closed':not fence,'local_target_count':len(local),'symbol_mentions':mentions})
result={'access_date':'2026-10-13','scope':'All handbook source Markdown, including 24 chapters, 7 appendices, labs, navigation and STYLE','chapter_count':len(chapters),'appendix_count':len(appendices),'document_count':len(files),'rows':rows,'structural_issues':issues,'manual_review_candidates':suspects,'boundary':'Pattern inventory and target existence only; not mathematical proof, exact heading-anchor verification, all paragraph readability, all external-link freshness or human full-book reread.'}
out=root/'work/research/round72-global-consistency-scan.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'chapters':len(chapters),'appendices':len(appendices),'documents':len(files),'structural_issues':issues,'manual_candidates':suspects},ensure_ascii=False,indent=2))
