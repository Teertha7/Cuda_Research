"""Save publisher-deposited Crossref metadata, then emit BibTeX without guessed fields."""
import json,pathlib,urllib.request,urllib.parse,time
root=pathlib.Path(__file__).resolve().parents[1];out=root/'research'/'metadata';out.mkdir(exist_ok=True)
entries=[];failures=[]
for key,doi in json.loads((root/'research'/'doi_candidates.json').read_text()).items():
 try:
  cached=out/(key+'.json')
  if cached.exists():data=json.loads(cached.read_text(encoding='utf-8'))
  else:
   req=urllib.request.Request('https://api.crossref.org/works/'+urllib.parse.quote(doi,safe=''),headers={'User-Agent':'PCAP-academic-reproducibility-project/1.0'})
   with urllib.request.urlopen(req,timeout=45) as f:data=json.load(f)
  (out/(key+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
  m=data['message'];authors=' and '.join(a.get('family','')+', '+a.get('given','') for a in m.get('author',[]));year=m.get('published-print',m.get('published',m.get('issued')))['date-parts'][0][0]
  title=m['title'][0]+(': '+m['subtitle'][0] if m.get('subtitle') else '')
  fields={'title':title,'author':authors,'year':str(year),'doi':m['DOI'],'url':m['URL']}
  typ='article' if m['type']=='journal-article' else 'inproceedings'
  if m.get('container-title'):fields['journal' if typ=='article' else 'booktitle']=m['container-title'][0]
  for k in ['volume','issue','page']:
   if k in m:fields[{'issue':'number','page':'pages'}.get(k,k)]=str(m[k]).replace('–','--')
  def tex(s):return s.replace('&',r'\&').replace('_',r'\_').replace('–','--')
  entries.append('@'+typ+'{'+key+',\n'+',\n'.join('  '+k+' = {'+tex(v)+'}' for k,v in fields.items())+'\n}\n')
  print(key,year,m['title'][0],flush=True)
 except Exception as e:failures.append({'key':key,'doi':doi,'error':str(e)});print('FAILED',key,str(e),flush=True)
 time.sleep(.2)
(root/'research'/'crossref.bib').write_text('\n'.join(entries),encoding='utf-8');(out/'failures.json').write_text(json.dumps(failures,indent=2))
