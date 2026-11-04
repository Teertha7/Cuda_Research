#include "edge.hpp"
#include <iostream>
#include <iomanip>
#include <chrono>
#include <stdexcept>
#include <algorithm>
#include <memory>
#include <omp.h>
using Clock=std::chrono::steady_clock;
static void require(bool ok,const char* what){if(!ok)throw std::runtime_error(what);}
static Edges oracle(const Image& a,int w,int h){
 Edges r(a.size());const int kx[9]={-1,0,1,-2,0,2,-1,0,1},ky[9]={-1,-2,-1,0,0,0,1,2,1};
 for(int y=1;y<h-1;++y)for(int x=1;x<w-1;++x){int gx=0,gy=0,k=0;for(int dy=-1;dy<=1;++dy)for(int dx=-1;dx<=1;++dx,++k){int v=a[size_t(y+dy)*w+x+dx];gx+=kx[k]*v;gy+=ky[k]*v;}r[size_t(y)*w+x]=std::abs(gx)+std::abs(gy);}return r;
}
static void tests(){
 device_info();int cases=0;
 for(auto wh:std::vector<std::pair<int,int>>{{1,1},{2,7},{3,3},{17,19},{31,33},{63,65},{129,127},{512,512}}){
  int w=wh.first,h=wh.second;Gpu gpu(w,h);
  for(int p=0;p<3;++p){Image a=generate(w,h,p);auto ref=oracle(a,w,h);Edges out(a.size());
   for(int th:{0,1,2,4,8,16}){sobel(a,out,w,h,0,h,th);require(out==ref,"CPU Sobel mismatch");++cases;}
   for(bool tiled:{false,true})for(auto block:std::vector<std::pair<int,int>>{{16,16},{32,8},{32,16}})for(double f:{0.,.25,.5,.75,1.}){
    gpu.run(a,out,w,h,f,tiled,block.first,block.second);require(out==ref,"GPU/hybrid Sobel mismatch");++cases;
   }
   auto cr=canny(a,w,h,0);for(int th:{1,2,4,8,16}){require(canny(a,w,h,th)==cr,"Canny OpenMP mismatch");++cases;}
  }
 }
 Image flat(81,127);Edges z(81);sobel(flat,z,9,9,0,9,0);require(std::all_of(z.begin(),z.end(),[](auto v){return v==0;}),"flat Sobel");
 auto c=canny(flat,9,9,0);require(std::all_of(c.begin(),c.end(),[](auto v){return v==0;}),"flat Canny");
 Image ramp(81);for(int y=0;y<9;y++)for(int x=0;x<9;x++)ramp[y*9+x]=uint8_t(x*10);sobel(ramp,z,9,9,0,9,0);require(z[40]==80,"analytical ramp Sobel");
 std::cout<<"PASS "<<cases<<" equivalence checks plus 3 analytical checks\n";
}
int main(int argc,char**argv){try{
 omp_set_dynamic(0);
 if(argc==2&&std::string(argv[1])=="--test"){tests();return 0;}
 if(argc==2&&std::string(argv[1])=="--probe"){device_info();return 0;}
 if(argc!=11)throw std::runtime_error("Usage: edge algorithm implementation size pattern threads cpu_fraction block_x block_y repeats warmups; or --test/--probe");
 std::string alg=argv[1],impl=argv[2];int w=std::stoi(argv[3]),p=std::stoi(argv[4]),th=std::stoi(argv[5]);double f=std::stod(argv[6]);int bx=std::stoi(argv[7]),by=std::stoi(argv[8]),reps=std::stoi(argv[9]),warm=std::stoi(argv[10]);
 require(w>0&&w<=16384&&p>=0&&p<=2&&th>=0&&th<=64&&f>=0&&f<=1&&bx>0&&by>0&&bx*by<=1024&&reps>0&&warm>=0,"Invalid configuration");
 require(alg=="sobel"||alg=="canny","Unknown algorithm");require(impl=="seq"||impl=="omp"||impl=="cuda"||impl=="tiled"||impl=="hybrid","Unknown implementation");
 bool dev=impl=="cuda"||impl=="tiled"||impl=="hybrid";require(!(dev&&alg=="canny"),"CUDA Canny not implemented");
 if(impl=="seq")th=0;if(impl=="omp")require(th>0,"OpenMP requires positive threads");if(impl=="hybrid")require(th==8,"Hybrid currently uses eight CPU threads");
 Image a=generate(w,w,p);Edges ref(a.size()),out(a.size());if(alg=="sobel")sobel(a,ref,w,w,0,w,0);else ref=canny(a,w,w,0);
 std::unique_ptr<Gpu> gpu;if(dev)gpu=std::make_unique<Gpu>(w,w);
 std::cout<<"algorithm,implementation,image,width,height,threads,cpu_fraction,block_x,block_y,repetition,h2d_ms,kernel_ms,d2h_ms,cpu_ms,e2e_ms,overlap_lower_bound_ms,correct\n"<<std::setprecision(10);
 for(int r=-warm;r<reps;++r){Timing t;
  if(dev)t=gpu->run(a,out,w,w,impl=="hybrid"?f:0,impl=="tiled",bx,by);
  else {auto start=Clock::now();if(alg=="sobel")sobel(a,out,w,w,0,w,th);else out=canny(a,w,w,th);t.total=std::chrono::duration<double,std::milli>(Clock::now()-start).count();t.cpu=t.total;}
  require(out==ref,"Benchmark correctness failure");
  if(r>=0)std::cout<<alg<<','<<impl<<','<<p<<','<<w<<','<<w<<','<<th<<','<<(dev?(impl=="hybrid"?f:0):1)<<','<<bx<<','<<by<<','<<r<<','<<t.h2d<<','<<t.kernel<<','<<t.d2h<<','<<t.cpu<<','<<t.total<<','<<t.overlap<<",1\n";
 }return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
