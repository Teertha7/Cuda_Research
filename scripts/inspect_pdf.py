import pathlib,sys,json
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'/'python'))
import pymupdf
doc=pymupdf.open(R/'paper'/'main.pdf');dest=R/'paper'/'qa';dest.mkdir(exist_ok=True);report=[]
for i,page in enumerate(doc):
 page.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3)).save(dest/f'page-{i+1}.png')
 text=page.get_text();(dest/f'page-{i+1}.txt').write_text(text,encoding='utf-8');blocks=page.get_text('blocks');outside=[b[:4] for b in blocks if b[0]<0 or b[1]<0 or b[2]>page.rect.width+1 or b[3]>page.rect.height+1]
 report.append({'page':i+1,'width_pt':page.rect.width,'height_pt':page.rect.height,'characters':len(text),'blocks_outside_page':outside,'fonts':[list(f) for f in page.get_fonts()]})
(dest/'layout.json').write_text(json.dumps(report,indent=2));print(json.dumps([{k:v for k,v in p.items() if k!='fonts'} for p in report],indent=2))
