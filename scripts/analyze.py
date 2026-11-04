"""All figure and table values originate in a selected immutable raw run."""
import sys,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'/'python'))
import argparse,json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('run',type=pathlib.Path);args=p.parse_args();raw=args.run/'observations.csv';d=pd.read_csv(raw)
assert len(d)>0 and (d.correct==1).all() and (d.e2e_ms>0).all()
assert np.isfinite(d.select_dtypes('number')).all().all()
out=ROOT/'results'/'processed'/args.run.name;out.mkdir(parents=True,exist_ok=True)
fig=ROOT/'paper'/'figures';tables=ROOT/'paper'/'tables';fig.mkdir(parents=True,exist_ok=True);tables.mkdir(exist_ok=True)
keys=['algorithm','implementation','image','width','height','threads','cpu_fraction','block_x','block_y']
s=d.groupby(keys).agg(n=('e2e_ms','size'),median_ms=('e2e_ms','median'),q25_ms=('e2e_ms',lambda x:x.quantile(.25)),q75_ms=('e2e_ms',lambda x:x.quantile(.75)),min_ms=('e2e_ms','min'),max_ms=('e2e_ms','max'),mean_ms=('e2e_ms','mean'),std_ms=('e2e_ms','std')).reset_index();s.to_csv(out/'summary.csv',index=False)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42,'figure.dpi':150})
def save(name):
 plt.tight_layout();plt.savefig(fig/(name+'.pdf'),bbox_inches='tight');plt.savefig(fig/(name+'.png'),dpi=220,bbox_inches='tight');plt.close()
def line(frame,label,column='e2e_ms'):
 g=frame.groupby('width')[column];m=g.median();q1=g.quantile(.25);q3=g.quantile(.75)
 plt.errorbar(m.index*m.index/1e6,m,yerr=[m-q1,q3-m],marker='o',capsize=2,label=label,linewidth=1)
sob=d[d.algorithm=='sobel'];can=d[d.algorithm=='canny']
selected={'Sequential':sob[sob.implementation=='seq'],'OpenMP 8':sob[(sob.implementation=='omp')&(sob.threads==8)],'CUDA global':sob[sob.implementation=='cuda'],'CUDA tiled 16x16':sob[(sob.implementation=='tiled')&(sob.block_x==16)&(sob.block_y==16)]}
plt.figure(figsize=(3.45,2.6))
for name,frame in selected.items():line(frame,name)
plt.yscale('log');plt.xlabel('Image size (megapixels)');plt.ylabel('Steady-workspace latency (ms)');plt.legend(fontsize=7);save('latency')
base=selected['Sequential'].groupby(['width','image']).e2e_ms.median()
speedrows=[];plt.figure(figsize=(3.45,2.5))
for name,frame in selected.items():
 if name=='Sequential':continue
 speed=(base/frame.groupby(['width','image']).e2e_ms.median()).reset_index(name='speedup');speed['configuration']=name;speedrows.append(speed)
 g=speed.groupby('width').speedup.median();plt.plot(g.index*g.index/1e6,g,marker='o',label=name)
plt.axhline(1,color='gray',linestyle=':');plt.xlabel('Image size (megapixels)');plt.ylabel('Speedup vs sequential');plt.legend(fontsize=7);save('speedup');pd.concat(speedrows).to_csv(out/'speedups.csv',index=False)
plt.figure(figsize=(3.45,2.5))
for alg,frame in [('Sobel',sob),('Canny',can)]:
 frame=frame[frame.width==4096];b=frame[frame.implementation=='seq'].groupby('image').e2e_ms.median();vals=[]
 for th in [1,2,4,8,16]:vals.append((b/frame[(frame.implementation=='omp')&(frame.threads==th)].groupby('image').e2e_ms.median()).median())
 plt.plot([1,2,4,8,16],vals,marker='o',label=alg)
plt.xlabel('OpenMP threads');plt.ylabel('Speedup vs sequential (4096 square)');plt.xticks([1,2,4,8,16]);plt.legend();save('scalability')
plt.figure(figsize=(3.45,2.5));line(sob[sob.implementation=='cuda'],'Global 16x16','kernel_ms')
for bx,by in [(16,16),(32,8),(32,16)]:line(sob[(sob.implementation=='tiled')&(sob.block_x==bx)&(sob.block_y==by)],f'Tiled {bx}x{by}','kernel_ms')
plt.xlabel('Image size (megapixels)');plt.ylabel('CUDA kernel interval (ms)');plt.legend(fontsize=7);save('tiling')
plt.figure(figsize=(3.45,2.5));g=sob[sob.implementation=='cuda'].groupby('width')[['h2d_ms','kernel_ms','d2h_ms','e2e_ms']].median();x=np.arange(len(g));bottom=np.zeros(len(g))
for col,label in [('h2d_ms','H2D'),('kernel_ms','Kernel'),('d2h_ms','D2H')]:plt.bar(x,g[col],bottom=bottom,label=label);bottom+=g[col]
plt.plot(x,g.e2e_ms,'ko--',label='Wall latency');plt.xticks(x,g.index);plt.xlabel('Square image width (pixels)');plt.ylabel('Time (ms)');plt.legend(fontsize=7);save('breakdown')
hy=sob[sob.implementation=='hybrid'];plt.figure(figsize=(3.45,2.5))
for size,group in hy.groupby('width'):
 g=group.groupby('cpu_fraction').e2e_ms.median();plt.plot(g.index*100,g,marker='o',label=str(size))
plt.xlabel('Rows assigned to CPU (%)');plt.ylabel('Steady-workspace latency (ms)');plt.legend(title='Square width',fontsize=7);save('partition')
plt.figure(figsize=(3.45,2.5));cpu=selected['OpenMP 8'].groupby('width').e2e_ms.median();gpu=selected['CUDA global'].groupby('width').e2e_ms.median();plt.plot(cpu.index*cpu.index/1e6,cpu/gpu,'o-');plt.axhline(1,color='gray',linestyle=':');plt.xlabel('Image size (megapixels)');plt.ylabel('OpenMP 8 / CUDA wall latency');save('crossover')
# A four-coefficient descriptive model; largest resolution withheld completely.
h=hy.groupby(['width','image','cpu_fraction']).e2e_ms.median().reset_index();train=h.width<4096
def features(frame):
 n=frame.width.to_numpy()**2/1e6;f=frame.cpu_fraction.to_numpy();return np.column_stack([np.ones(len(frame)),n*f,n*(1-f),n*np.minimum(f,1-f)])
coef=np.linalg.lstsq(features(h[train]),h[train].e2e_ms,rcond=None)[0];test=h[~train].copy();test['prediction_ms']=np.maximum(0,features(test)@coef);test['absolute_percentage_error']=abs(test.prediction_ms-test.e2e_ms)/test.e2e_ms*100;test.to_csv(out/'model_holdout.csv',index=False)
plt.figure(figsize=(3.45,2.5));plt.scatter(test.e2e_ms,test.prediction_ms,c=test.cpu_fraction,cmap='viridis',s=24);lim=max(test.e2e_ms.max(),test.prediction_ms.max())*1.05;plt.plot([0,lim],[0,lim],'k--',lw=.8);plt.xlabel('Measured held-out latency (ms)');plt.ylabel('Predicted latency (ms)');plt.colorbar(label='CPU fraction');save('prediction')
# Initial endpoint-throughput estimate and retrospectively evaluated candidate selection.
policy=[]
for (width,image),g in h.groupby(['width','image']):
 c=float(g[g.cpu_fraction==1].e2e_ms.iloc[0]);v=float(g[g.cpu_fraction==0].e2e_ms.iloc[0]);estimate=v/(c+v);nearest=min([0,.25,.5,.75,1],key=lambda f:abs(f-estimate));chosen=float(g[g.cpu_fraction==nearest].e2e_ms.iloc[0]);best=g.loc[g.e2e_ms.idxmin()]
 policy.append(dict(width=width,image=image,throughput_cpu_fraction=estimate,nearest_tested_fraction=nearest,selected_ms=chosen,best_tested_fraction=best.cpu_fraction,best_tested_ms=best.e2e_ms,regret_percent=(chosen/best.e2e_ms-1)*100))
pd.DataFrame(policy).to_csv(out/'partition_policy.csv',index=False)
rows=[]
for name,frame in selected.items():
 for width,g in frame.groupby('width'):rows.append(dict(configuration=name,width=width,n=len(g),median_ms=g.e2e_ms.median(),q25_ms=g.e2e_ms.quantile(.25),q75_ms=g.e2e_ms.quantile(.75)))
table=pd.DataFrame(rows);table.to_csv(out/'paper_latency.csv',index=False)
lines=[r'\begin{tabular}{lrrrr}',r'\hline',r'Configuration & 512 & 1024 & 2048 & 4096 \\',r'\hline']
for name in selected:
 g=table[table.configuration==name].sort_values('width');lines.append(name+' & '+' & '.join(f'{v:.3f}' for v in g.median_ms)+r' \\')
lines.extend([r'\hline',r'\end{tabular}']);(tables/'latency.tex').write_text('\n'.join(lines))
facts={'raw_run':args.run.name,'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'observations':len(d),'configurations':len(s),'all_correct':bool((d.correct==1).all()),'model_coefficients':coef.tolist(),'model_holdout_n':len(test),'model_holdout_mape_percent':float(test.absolute_percentage_error.mean()),'overlap_positive_samples':int((hy.overlap_lower_bound_ms>.01).sum()),'overlap_max_lower_bound_ms':float(hy.overlap_lower_bound_ms.max()),'latency_4096_ms':{name:float(frame[frame.width==4096].e2e_ms.median()) for name,frame in selected.items()},'canny_4096_ms':{str(th):float(can[(can.width==4096)&(can.implementation==('seq' if th==0 else 'omp'))&(can.threads==th)].e2e_ms.median()) for th in [0,1,2,4,8,16]}}
(out/'facts.json').write_text(json.dumps(facts,indent=2));(tables/'facts.json').write_text(json.dumps(facts,indent=2));print(json.dumps(facts,indent=2))
macros={'ObservationCount':str(len(d)),'ConfigurationCount':str(len(s)),'SeqLarge':f"{facts['latency_4096_ms']['Sequential']:.3f}",'OmpLarge':f"{facts['latency_4096_ms']['OpenMP 8']:.3f}",'CudaLarge':f"{facts['latency_4096_ms']['CUDA global']:.3f}",'TileLarge':f"{facts['latency_4096_ms']['CUDA tiled 16x16']:.3f}",'ModelError':f"{facts['model_holdout_mape_percent']:.2f}",'CannySeq':f"{facts['canny_4096_ms']['0']:.3f}",'CannySixteen':f"{facts['canny_4096_ms']['16']:.3f}"}
(tables/'numbers.tex').write_text('\n'.join('\\newcommand{\\'+k+'}{'+v+'}' for k,v in macros.items()))
cuda_large=selected['CUDA global'].query('width == 4096');tile_large=selected['CUDA tiled 16x16'].query('width == 4096');hy_large=hy.query('width == 4096').groupby('cpu_fraction').e2e_ms.median()
extra={'HtoDLarge':f'{cuda_large.h2d_ms.median():.3f}','KernelLarge':f'{cuda_large.kernel_ms.median():.3f}','DtoHLarge':f'{cuda_large.d2h_ms.median():.3f}','TileKernelLarge':f'{tile_large.kernel_ms.median():.3f}','HybridHalf':f'{hy_large.loc[.5]:.3f}','HybridGpu':f'{hy_large.loc[0.]:.3f}','HybridCpu':f'{hy_large.loc[1.]:.3f}','RegretMax':f"{pd.DataFrame(policy).regret_percent.max():.2f}",'OverlapCount':str(facts['overlap_positive_samples']),'OverlapMax':f"{facts['overlap_max_lower_bound_ms']:.4f}"}
with (tables/'numbers.tex').open('a') as f:f.write('\n'+'\n'.join('\\newcommand{\\'+k+'}{'+v+'}' for k,v in extra.items()))
(out/'claim_values.json').write_text(json.dumps({**macros,**extra},indent=2))
large=table[table.width==4096];lines=[r'\begin{tabular}{lrrr}',r'\hline',r'Configuration & Median & Q1--Q3 & $n$ \\',r'\hline']
for row in large.itertuples():lines.append(f'{row.configuration} & {row.median_ms:.3f} & {row.q25_ms:.3f}--{row.q75_ms:.3f} & {row.n}'+r' \\')
lines.extend([r'\hline',r'\end{tabular}']);(tables/'variability.tex').write_text('\n'.join(lines))
