"""Automated evidence checks; does not replace human review or visual inspection."""
import pathlib,sys,csv,json,hashlib,re,subprocess,datetime
R=pathlib.Path(__file__).resolve().parents[1];run=R/'results/raw/20261026T153339790016Z';checks=[]
def check(name,ok,detail=''):
 checks.append({'name':name,'pass':bool(ok),'detail':detail})
 if not ok:print('FAIL',name,detail)
manifest=json.loads((run/'manifest.json').read_text());rows=list(csv.DictReader((run/'observations.csv').open()))
check('raw observations',len(rows)==3780,str(len(rows)))
check('all measured outputs match reference',all(r['correct']=='1' for r in rows))
check('no recorded benchmark failures',json.loads((run/'failures.json').read_text())==[])
check('archived executable hash',hashlib.sha256((run/'edge_measured.exe').read_bytes()).hexdigest()==manifest['executable_sha256'])
groups={}
for row in rows:groups.setdefault(row['case_id'],[]).append(row)
check('252 configurations with 15 observations each',len(groups)==252 and all(len(v)==15 for v in groups.values()))
for path,expected in manifest['source_sha256'].items():check('measured source unchanged: '+path,hashlib.sha256((R/path).read_bytes()).hexdigest()==expected)
for path,expected in manifest['source_sha256'].items():check('archived measured source: '+path,hashlib.sha256((run/'source'/pathlib.Path(path).name).read_bytes()).hexdigest()==expected)
for case,records in groups.items():
 original=list(csv.DictReader((run/f'case_{int(case):03d}.stdout.csv').open()))
 check('raw case integrity: '+case,len(original)==len(records) and all(all(saved[k]==v for k,v in original_row.items()) for original_row,saved in zip(original,records)))
facts=json.loads((R/'paper/tables/facts.json').read_text());check('analysis raw hash matches',facts['raw_sha256']==hashlib.sha256((run/'observations.csv').read_bytes()).hexdigest())
check('C++ test execution', 'PASS 984' in (R/'results/validation/correctness_final.txt').read_text())
check('independent oracle execution','PASS 36' in (R/'results/validation/independent_oracle.txt').read_text())
check('fresh rebuilt C++ tests','PASS 984' in (R/'results/validation/correctness_resume.txt').read_text())
check('fresh independent oracle','PASS 36' in (R/'results/validation/independent_oracle_resume.txt').read_text())
check('real CUDA device execution','RTX 4060' in (R/'results/validation/device_probe.txt').read_text())
bib=(R/'paper/references.bib').read_text(encoding='utf-8');tex=(R/'paper/main.tex').read_text(encoding='utf-8');bibkeys=set(re.findall(r'@\w+\s*\{\s*([^,]+)',bib));cited=set()
for group in re.findall(r'\\cite\{([^}]+)\}',tex):cited.update(group.split(','))
check('all citations resolve',cited<=bibkeys,str(sorted(cited-bibkeys)))
check('research and paper bibliographies identical',bib==(R/'research/references.bib').read_text(encoding='utf-8'))
candidates=json.loads((R/'research/doi_candidates.json').read_text())
for key,doi in candidates.items():
 data=json.loads((R/'research/metadata'/(key+'.json')).read_text(encoding='utf-8'));check('DOI metadata: '+key,data['message']['DOI'].lower()==doi.lower())
log=(R/'paper/main.log').read_text(errors='replace');check('IEEEtran conference class',r'\documentclass[conference]{IEEEtran}' in tex and 'Document Class: IEEEtran' in log)
check('no undefined citations or references',not re.search(r'(?:Citation|Reference).*undefined|There were undefined references',log,re.I))
check('no unresolved font warnings','LaTeX Font Warning:' not in log and 'defaults substituted' not in log)
check('no overfull boxes','Overfull' not in log)
check('no TeX errors',not re.search(r'^!',log,re.M))
for name in ['latency','speedup','scalability','tiling','breakdown','partition','crossover','prediction']:check('figure '+name,(R/'paper/figures'/(name+'.pdf')).stat().st_size>1000)
layout=json.loads((R/'paper/qa/layout.json').read_text());check('letter paper and no off-page text',all(p['width_pt']==612 and p['height_pt']==792 and not p['blocks_outside_page'] for p in layout))
check('PDF exists',(R/'paper/main.pdf').stat().st_size>10000)
sys.path.insert(0,str(R/'tools/python'))
import pandas as pd,numpy as np
d=pd.DataFrame(rows);numeric=['width','image','threads','block_x','block_y','cpu_fraction','e2e_ms','kernel_ms'];d[numeric]=d[numeric].apply(pd.to_numeric)
check('finite positive wall observations',np.isfinite(d[numeric]).all().all() and (d.e2e_ms>0).all())
s=d[d.algorithm=='sobel'];b=s[s.implementation=='seq'].groupby(['width','image']).e2e_ms.median();sp=pd.read_csv(R/'results/processed'/run.name/'speedups.csv')
selectors={'OpenMP 8':s[(s.implementation=='omp')&(s.threads==8)],'CUDA global':s[s.implementation=='cuda'],'CUDA tiled 16x16':s[(s.implementation=='tiled')&(s.block_x==16)&(s.block_y==16)]}
for name,frame in selectors.items():
 expected=b/frame.groupby(['width','image']).e2e_ms.median();saved=sp[sp.configuration==name].set_index(['width','image']).speedup;check('speedup formula: '+name,np.allclose(expected.sort_index(),saved.sort_index()))
base_kernel=s[s.implementation=='cuda'].groupby('width').kernel_ms.median();t=s[s.implementation=='tiled'].groupby(['width','block_x','block_y']).kernel_ms.median();check('tiling claim matches all measured pooled medians',all(v>base_kernel.loc[k[0]] for k,v in t.items()))
claims=json.loads((R/'results/processed'/run.name/'claim_values.json').read_text());numbers=(R/'paper/tables/numbers.tex').read_text()
check('claim macros generated from processed values',all('\\newcommand{\\'+key+'}{'+value+'}' in numbers for key,value in claims.items()))
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':sum(c['pass'] for c in checks),'total':len(checks),'checks':checks,'limitations':['One measurement session; no claim of statistical significance','No natural-image performance corpus','No profiler timeline or Compute Sanitizer run','No CUDA or heterogeneous Canny','Author information and submission-level human review pending','Some literature records are abstract-only; detailed hardware extraction incomplete']}
(R/'results/validation/audit.json').write_text(json.dumps(report,indent=2));print(f"Audit: {report['passed']}/{report['total']} checks passed")
if report['passed']!=report['total']:sys.exit(1)
