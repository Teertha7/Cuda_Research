"""Independent small-image NumPy oracle, including full connected hysteresis."""
import pathlib,sys,subprocess,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'/'python'))
import numpy as np
from collections import deque
out=R/'data'/'test_images';out.mkdir(parents=True,exist_ok=True)
results=R/'results'/'validation'/'images';results.mkdir(parents=True,exist_ok=True)
def conv(a,k,padding):
 r=len(k)//2;p=np.pad(a,r,mode=padding);z=np.zeros(a.shape,dtype=float)
 for y in range(len(k)):
  for x in range(len(k)):z+=k[y,x]*p[y:y+a.shape[0],x:x+a.shape[1]]
 return z
kx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]]);ky=kx.T
def reference(a,alg):
 if alg=='sobel':
  v=np.abs(conv(a,kx,'constant'))+np.abs(conv(a,ky,'constant'));v[[0,-1],:]=0;v[:,[0,-1]]=0;return v.astype(np.uint16)
 k=np.array([1,4,6,4,1]);sm=conv(a,np.outer(k,k)/256,'edge');gx=conv(sm,kx,'constant');gy=conv(sm,ky,'constant');mag=np.hypot(gx,gy);mag[[0,-1],:]=0;mag[:,[0,-1]]=0
 angles=np.mod(np.degrees(np.arctan2(gy,gx)),180);nms=np.zeros_like(mag);h,w=a.shape
 for y in range(1,h-1):
  for x in range(1,w-1):
   d=angles[y,x];dy,dx=(0,1) if d<22.5 or d>=157.5 else ((1,1) if d<67.5 else ((1,0) if d<112.5 else (1,-1)))
   if mag[y,x]>=mag[y-dy,x-dx] and mag[y,x]>=mag[y+dy,x+dx]:nms[y,x]=mag[y,x]
 edge=nms>=100;queue=deque(map(tuple,np.argwhere(edge)))
 while queue:
  y,x=queue.popleft()
  for yy in range(max(0,y-1),min(h,y+2)):
   for xx in range(max(0,x-1),min(w,x+2)):
    if not edge[yy,xx] and nms[yy,xx]>=40:edge[yy,xx]=True;queue.append((yy,xx))
 return edge.astype(np.uint16)*255
def read_pgm(path):
 with path.open('rb') as f:
  assert f.readline().strip()==b'P5';w,h=map(int,f.readline().split());m=int(f.readline());return np.frombuffer(f.read(),dtype='>u2' if m>255 else np.uint8).reshape(h,w).astype(np.uint16)
y,x=np.indices((31,37));rng=np.random.default_rng(3129)
images={'flat':np.full((31,37),127,dtype=np.uint8),'vertical_step':np.where(x<18,0,255).astype(np.uint8),'diagonal_step':np.where(x>y,230,20).astype(np.uint8),'noise':rng.integers(0,256,(31,37),dtype=np.uint8),'weak_connected':np.where(x>18,np.where(y<10,220,35),0).astype(np.uint8)}
checks=0;manifest=[]
for name,a in images.items():
 path=out/(name+'.pgm');path.write_bytes(f'P5\n{a.shape[1]} {a.shape[0]}\n255\n'.encode()+a.tobytes());manifest.append({'file':str(path.relative_to(R)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'origin':'Original procedural fixture','license':'CC0-1.0'})
 for alg in ['sobel','canny']:
  expected=reference(a,alg)
  for impl in (['seq','omp','cuda','tiled','hybrid'] if alg=='sobel' else ['seq','omp']):
   dest=results/(name+'_'+alg+'_'+impl+'.pgm');subprocess.run([str(R/'build'/'edge_image.exe'),str(path),str(dest),alg,impl,'8'],check=True)
   actual=read_pgm(dest);assert np.array_equal(actual,expected),(name,alg,impl,int((actual!=expected).sum()));checks+=1
# RGB grayscale contract checked through a uniform color image (zero Sobel).
rgb=np.zeros((5,7,3),dtype=np.uint8);rgb[:]=[200,50,100];path=out/'color.ppm';path.write_bytes(b'P6\n7 5\n255\n'+rgb.tobytes());dest=results/'color_sobel.pgm';subprocess.run([str(R/'build'/'edge_image.exe'),str(path),str(dest),'sobel','seq','1'],check=True);assert not read_pgm(dest).any();checks+=1
(out/'manifest.json').write_text(json.dumps(manifest,indent=2));print(f'PASS {checks} independent NumPy-oracle and RGB fixture checks')
