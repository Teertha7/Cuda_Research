from pathlib import Path
import re, copy, html, json
import pdfplumber
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Flowable, KeepTogether, FrameBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
ROOT=Path('/Users/teerthachatterjee/Downloads/PCAP_project')
SRC='/Users/teerthachatterjee/Downloads/PCAP_Final_Report.pdf'
pdf=pdfplumber.open(SRC)
fontdir=Path('/System/Library/Fonts/Supplemental')
for name,file in [('T','Times New Roman.ttf'),('TB','Times New Roman Bold.ttf'),('TI','Times New Roman Italic.ttf'),('TBI','Times New Roman Bold Italic.ttf')]:pdfmetrics.registerFont(TTFont(name,str(fontdir/file)))
pdfmetrics.registerFont(TTFont('Math', '/Users/teerthachatterjee/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype/DejaVuSerif.ttf'))
pdfmetrics.registerFontFamily('T',normal='T',bold='TB',italic='TI',boldItalic='TBI')
styles={
'body':ParagraphStyle('body',fontName='T',fontSize=10,leading=11.7,alignment=TA_JUSTIFY,firstLineIndent=10,spaceAfter=4.5,allowWidows=0,allowOrphans=0),
'head':ParagraphStyle('head',fontName='T',fontSize=10,leading=12,alignment=TA_CENTER,spaceBefore=10,spaceAfter=7,keepWithNext=True),
'sub':ParagraphStyle('sub',fontName='TI',fontSize=10,leading=12,spaceBefore=6,spaceAfter=5,keepWithNext=True),
'abstract':ParagraphStyle('abstract',fontName='TB',fontSize=9,leading=10.5,alignment=TA_JUSTIFY,spaceAfter=6),
'caption':ParagraphStyle('caption',fontName='T',fontSize=8,leading=9.5,spaceAfter=8),
'ref':ParagraphStyle('ref',fontName='T',fontSize=8,leading=9.3,leftIndent=18,firstLineIndent=-18,spaceAfter=3,splitLongWords=True),
}
blocks=[]; story=[]; placements=[]
# Extract only the user's revised PDF; line endings and discretionary hyphenation are layout.
def lines(pg,col,y0,y1):
 x0,x1= ((0,300) if col==0 else (300,612)) if pg==3 else ((0,310) if col==0 else (310,612))
 return [l for l in pdf.pages[pg-1].crop((x0,0,x1,792)).extract_text_lines() if y0 <= l['top'] < y1]
def raw(pg,col,y0,y1):return '\n'.join(l['text'] for l in lines(pg,col,y0,y1))
def clean(t):
 # Restore words split only by a typesetting line break; keep authored hyphenated compounds.
 parts=['nec-\nessarily','charac-\nterize','medi-\nans','ap-\nproximates','in-\ntervals','combi-\nnations','mea-\nsurement','predic-\ntions','arith-\nmetic','empha-\nsizing','col-\nlaborative','ideal-\nized','lit-\nerature','ac-\ntivity','gener-\nalization','intermedi-\nate','imple-\nmented','config-\nurations','execu-\ntion','con-\ntrolled','la-\ntency','Mea-\nsurements']
 for p in parts:t=t.replace(p,p.replace('-\n',''))
 t=re.sub(r'-\n(?=\w)','-',t)
 return re.sub(r'\s+',' ',t).strip()
def add(pg,col,y0,y1,kind='body',extra=None):
 t=raw(pg,col,y0,y1)
 if extra:t+='\n'+raw(*extra)
 t=clean(t);blocks.append({'kind':kind,'text':t})
 escaped=html.escape(t)
 for symbol in ['∈','⌊','⌋']:escaped=escaped.replace(symbol,'<font name="Math">'+symbol+'</font>')
 story.append(Paragraph(escaped,styles[kind]))
 return t
class Vector(Flowable):
 def __init__(self,path,page,box,width=252):
  Flowable.__init__(self);self.path=path;self.page=page;self.box=box;self.width=width;self.height=(box[3]-box[1])*width/(box[2]-box[0]);self.hAlign='CENTER'
 def draw(self):
  x,y=self.canv.absolutePosition(0,0);placements.append((self.canv.getPageNumber()-1,x,y,self.width,self.height,self.path,self.page,self.box))
def vec(pg,box,width=252):return Vector(SRC,pg-1,box,width)
def figure(pg,box,capregion):
 caption=clean(raw(*capregion));blocks.append({'kind':'caption','text':caption})
 story.append(KeepTogether([vec(pg,box),Spacer(1,5),Paragraph(html.escape(caption),styles['caption'])]))
def table(pg,box):story.extend([vec(pg,box),Spacer(1,8)])
# Title and names are drawn in a full-width area on the first page.
title=clean(pdf.pages[0].crop((0,45,612,105)).extract_text())
authors=pdf.pages[0].crop((0,110,612,163)).extract_text().splitlines()
add(1,0,190,393,'abstract');add(1,0,393,418,'abstract')
add(1,0,425,441,'head')
add(1,0,443,550);add(1,0,550,662);add(1,0,662,775,extra=(1,1,185,217))
add(1,1,224,242,'head')
for a,b in [(244,387),(387,495),(495,640)]:add(1,1,a,b)
add(1,1,640,710,extra=(2,0,48,114))
add(2,0,121,137,'head');add(2,0,140,242);add(2,0,242,386)
story.extend([vec(2,(110,392,302,422),220),Spacer(1,6)])
add(2,0,422,495);add(2,0,520,537,'head');add(2,0,539,557,'sub')
add(2,0,561,610);add(2,0,618,660);add(2,0,714,781,extra=(2,1,44,110))
add(3,0,45,64,'sub');add(3,0,69,172);add(3,0,179,298);add(3,0,303,405);add(3,0,413,442)
story.extend([vec(3,(80,443,300,459),240),Spacer(1,6)])
add(3,0,459,528);add(3,0,547,562,'head');add(3,0,564,582,'sub');add(3,0,588,705)
add(3,0,734,778,extra=(3,1,45,112))
add(4,0,49,68,'sub')
for a,b in [(72,200),(207,322),(329,420),(427,554)]:add(4,0,a,b)
add(4,0,580,595,'sub');add(4,0,596,612)
story.extend([vec(4,(53,613,302,633),252),Spacer(1,6)])
# Subscripts/superscripts use the same mathematical text, with restored baseline positioning.
t=clean(raw(4,0,635,735)).replace('where N = N/106.','where NM = N/106.').replace('M 1024','1024')
# extract_text_lines separates the subscript M into its own line.
t=t.replace('512, M 1024','512, 1024')
blocks.append({'kind':'body','text':t})
esc=html.escape(t).replace('where NM = N/106.','where N<sub>M</sub> = N/10<super>6</super>.')
story.append(Paragraph(esc,styles['body']))
add(4,0,739,754,'head');add(4,0,755,775,'sub')
add(4,1,45,88,extra=(5,0,396,434))
table(5,(55,45,300,141))
# Figure 1 has displaced chart components in the edited PDF. The intact original plot is in the accompanying project.
plot=PdfReader(str(ROOT/'paper/figures/latency.pdf')).pages[0]
caption=clean(raw(5,0,355,381));blocks.append({'kind':'caption','text':caption})
story.append(KeepTogether([Vector(str(ROOT/'paper/figures/latency.pdf'),0,(0,0,float(plot.mediabox.width),float(plot.mediabox.height))),Spacer(1,5),Paragraph(html.escape(caption),styles['caption'])]))
add(5,0,434,532)
figure(6,(53,53,298,238),(6,0,260,284))
add(5,0,539,554,'sub');add(5,0,555,686)
add(5,0,686,750,extra=(6,0,563,603))
figure(6,(53,310,298,493),(6,0,515,549))
add(6,0,607,622,'sub');add(6,0,623,731)
add(6,0,731,762,extra=(6,1,557,607))
figure(6,(316,53,559,232),(6,1,252,278))
add(6,1,608,681);add(6,1,683,760)
figure(6,(317,309,559,489),(6,1,510,535))
table(7,(58,50,299,138))
add(7,0,154,169,'head');add(7,0,169,338);add(7,0,338,413)
add(7,0,415,430,'head');add(7,0,431,515);add(7,0,515,634);add(7,0,634,722)
add(7,1,45,60,'head');add(7,1,61,169);add(7,1,169,243)
add(7,1,245,259,'head');add(7,1,261,336);add(7,1,338,352,'head')
for pg,col,a,b in [(7,1,354,720),(8,0,48,351),(8,1,45,314)]:
 t=raw(pg,col,a,b)
 for ref in re.split(r'\n(?=\[\d+\])',t):
  ref=re.sub(r'(https?://.*)',lambda m: re.sub(r'\s+','',m.group(0)),clean(ref).replace('https: //','https://')); blocks.append({'kind':'ref','text':ref});
  if ref.startswith('[14]'):story.append(FrameBreak())
  story.append(KeepTogether([Paragraph(html.escape(ref),styles['ref'])]))
W,H=612,792; margin=45; gap=18; cw=252
frames=lambda top:[Frame(margin,42,cw,top-42,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),Frame(margin+cw+gap,42,cw,top-42,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)]
def first(canvas,doc):
 p=Paragraph(html.escape(title),ParagraphStyle('title',fontName='T',fontSize=21,leading=24,alignment=TA_CENTER))
 _,h=p.wrap(522,80);p.drawOn(canvas,45,747-h)
 y=747-h-17
 for author in authors:
  canvas.setFont('T',11);canvas.drawCentredString(306,y,author);y-=14
out=ROOT/'tmp/pdfs/reflow.pdf'
doc=BaseDocTemplate(str(out),pagesize=(W,H),title=title,author='; '.join(authors))
doc.addPageTemplates([PageTemplate(id='First',frames=frames(620),onPage=first,autoNextPageTemplate='Later'),PageTemplate(id='Later',frames=frames(747))])
doc.build(story)
reader=PdfReader(str(out)); cache={};writer=PdfWriter()
for p in reader.pages:writer.add_page(p)
for dest,x,y,w,h,path,idx,box in placements:
 if path not in cache:cache[path]=PdfReader(path)
 src=copy.copy(cache[path].pages[idx]); ph=float(src.mediabox.height)
 x0,top,x1,bottom=box
 src.cropbox.lower_left=(x0,ph-bottom);src.cropbox.upper_right=(x1,ph-top)
 scale=w/(x1-x0)
 transform=Transformation().translate(-x0,-(ph-bottom)).scale(scale).translate(x,y)
 writer.pages[dest].merge_transformed_page(src,transform)
final=ROOT/'output/pdf/PCAP_Final_Report_Formatted.pdf'
writer.write(str(final))
(ROOT/'tmp/pdfs/content.json').write_text(json.dumps({'title':title,'authors':authors,'blocks':blocks},ensure_ascii=False,indent=2))
print(final, 'pages:',len(writer.pages));print('held out:',t[:100])
