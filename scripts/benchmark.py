"""Run independent processes in seeded randomized configuration order; preserve every sample."""
import argparse,csv,datetime,hashlib,io,json,os,pathlib,platform,random,shutil,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--repeats',type=int,default=15);p.add_argument('--warmups',type=int,default=3);p.add_argument('--sizes',type=int,nargs='+',default=[512,1024,2048,4096]);p.add_argument('--algorithms',nargs='+',default=['sobel','canny']);args=p.parse_args()
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');out=ROOT/'results'/'raw'/stamp;out.mkdir(parents=True,exist_ok=False)
exe=ROOT/'build'/'edge.exe';configs=[]
for alg in args.algorithms:
 for n in args.sizes:
  for image in range(3):
   configs.append([alg,'seq',n,image,0,1,16,16])
   for th in [1,2,4,8,16]:configs.append([alg,'omp',n,image,th,1,16,16])
   if alg=='sobel':
    configs.append([alg,'cuda',n,image,0,0,16,16])
    for bx,by in [(16,16),(32,8),(32,16)]:configs.append([alg,'tiled',n,image,0,0,bx,by])
    for f in [0,.25,.5,.75,1]:configs.append([alg,'hybrid',n,image,8,f,16,16])
random.Random(3129).shuffle(configs)
env=os.environ.copy();env.update(OMP_DYNAMIC='FALSE',OMP_NUM_THREADS='8',OMP_WAIT_POLICY='PASSIVE')
def capture(cmd):
 r=subprocess.run(cmd,capture_output=True,text=True);return {'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
meta={'run_id':stamp,'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':platform.platform(),'python':sys.version,'cpu':platform.processor(),'logical_cpus':os.cpu_count(),'executable_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'gpu':capture(['nvidia-smi','--query-gpu=name,memory.total,compute_cap,driver_version','--format=csv']),'protocol':vars(args),'random_seed':3129,'omp_environment':{k:env[k] for k in ['OMP_DYNAMIC','OMP_NUM_THREADS','OMP_WAIT_POLICY']},'timing_scope':'steady workspace; includes host staging, transfers, kernel, CPU region, synchronization and merge; excludes process/context startup, workspace allocation, input generation and validation','source_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((ROOT/'src').glob('*'))}}
(out/'manifest.json').write_text(json.dumps(meta,indent=2));(out/'configurations.json').write_text(json.dumps(configs,indent=2))
# Archive the exact executable and source before any measurement, even for failed runs.
shutil.copy2(exe,out/'edge_measured.exe')
shutil.copytree(ROOT/'src',out/'source')
shutil.copy2(pathlib.Path(__file__),out/'benchmark_runner.py')
failures=[];writer=None
with (out/'observations.csv').open('x',newline='') as f:
 for idx,cfg in enumerate(configs):
  cmd=[str(exe),*map(str,cfg),str(args.repeats),str(args.warmups)]
  r=subprocess.run(cmd,capture_output=True,text=True,env=env)
  (out/f'case_{idx:03d}.stdout.csv').write_text(r.stdout);(out/f'case_{idx:03d}.stderr.txt').write_text(r.stderr)
  if r.returncode:
   failures.append({'index':idx,'command':cmd,'returncode':r.returncode,'stderr':r.stderr});print('FAILED',cfg,flush=True);continue
  rows=list(csv.DictReader(io.StringIO(r.stdout)))
  if len(rows)!=args.repeats:raise RuntimeError('Unexpected record count')
  for row in rows:
   row.update(run_id=stamp,case_id=idx,hardware_id=meta['executable_sha256'][:12]+'-i7-13700HX-RTX4060',warmups=args.warmups,timing_scope='steady_workspace',threshold_low=40,threshold_high=100)
   if writer is None:writer=csv.DictWriter(f,fieldnames=list(row));writer.writeheader()
   writer.writerow(row)
  f.flush();print(f'{idx+1}/{len(configs)} {cfg}',flush=True)
(out/'failures.json').write_text(json.dumps(failures,indent=2));print(out)
if failures:sys.exit(1)
