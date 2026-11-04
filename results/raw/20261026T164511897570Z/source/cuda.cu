#include "edge.hpp"
#include <cuda_runtime.h>
#include <stdexcept>
#include <iostream>
#include <chrono>
#include <cstring>
#include <algorithm>
#define CK(call) do {cudaError_t cuda_status_=(call);if(cuda_status_!=cudaSuccess)throw std::runtime_error(std::string(#call)+": "+cudaGetErrorString(cuda_status_));}while(0)
using Clock=std::chrono::steady_clock;
static double ms(Clock::time_point a,Clock::time_point b){return std::chrono::duration<double,std::milli>(b-a).count();}
__global__ void base(const unsigned char* a,unsigned short* o,int w,int h,int first,int offset) {
 int x=blockIdx.x*blockDim.x+threadIdx.x,y=first+blockIdx.y*blockDim.y+threadIdx.y;
 if(x>=w||y>=h)return; int q=(y-first)*w+x;
 if(x==0||x==w-1||y==0||y==h-1){o[q]=0;return;}
 int i=(y-offset)*w+x;
 int gx=-a[i-w-1]+a[i-w+1]-2*a[i-1]+2*a[i+1]-a[i+w-1]+a[i+w+1];
 int gy=-a[i-w-1]-2*a[i-w]-a[i-w+1]+a[i+w-1]+2*a[i+w]+a[i+w+1];
 o[q]=abs(gx)+abs(gy);
}
__global__ void tile(const unsigned char* a,unsigned short* o,int w,int h,int first,int offset) {
 extern __shared__ unsigned char s[];int sw=blockDim.x+2,sh=blockDim.y+2;
 int tid=threadIdx.y*blockDim.x+threadIdx.x;
 for(int i=tid;i<sw*sh;i+=blockDim.x*blockDim.y){
  int x=blockIdx.x*blockDim.x+i%sw-1,y=first+blockIdx.y*blockDim.y+i/sw-1;
  s[i]=(x>=0&&x<w&&y>=offset&&y<h)?a[(y-offset)*w+x]:0;
 }
 __syncthreads();
 int x=blockIdx.x*blockDim.x+threadIdx.x,y=first+blockIdx.y*blockDim.y+threadIdx.y;
 if(x>=w||y>=h)return;int q=(y-first)*w+x;
 if(x==0||x==w-1||y==0||y==h-1){o[q]=0;return;}
 int i=(threadIdx.y+1)*sw+threadIdx.x+1;
 int gx=-s[i-sw-1]+s[i-sw+1]-2*s[i-1]+2*s[i+1]-s[i+sw-1]+s[i+sw+1];
 int gy=-s[i-sw-1]-2*s[i-sw]-s[i-sw+1]+s[i+sw-1]+2*s[i+sw]+s[i+sw+1];
 o[q]=abs(gx)+abs(gy);
}
struct State {int w,h;unsigned char *in,*pin;unsigned short *out,*pout;cudaStream_t stream;cudaEvent_t ev[4];};
Gpu::Gpu(int w,int h):state(nullptr){
 State* s=new State{};s->w=w;s->h=h;state=s;
 CK(cudaMalloc(&s->in,size_t(w)*h));CK(cudaMalloc(&s->out,size_t(w)*h*2));
 CK(cudaMallocHost(&s->pin,size_t(w)*h));CK(cudaMallocHost(&s->pout,size_t(w)*h*2));
 CK(cudaStreamCreateWithFlags(&s->stream,cudaStreamNonBlocking));
 for(auto &e:s->ev)CK(cudaEventCreate(&e));
}
Gpu::~Gpu(){auto s=static_cast<State*>(state);if(!s)return;cudaStreamSynchronize(s->stream);for(auto e:s->ev)cudaEventDestroy(e);cudaStreamDestroy(s->stream);cudaFree(s->in);cudaFree(s->out);cudaFreeHost(s->pin);cudaFreeHost(s->pout);delete s;}
Timing Gpu::run(const Image& a,Edges& out,int w,int h,double fraction,bool tiled,int bx,int by){
 auto s=static_cast<State*>(state);Timing t;int first=int(h*fraction),offset=std::max(0,first-1);
 auto start=Clock::now();
 if(first<h){
  size_t bytes=size_t(h-offset)*w;std::memcpy(s->pin,a.data()+size_t(offset)*w,bytes);
  CK(cudaEventRecord(s->ev[0],s->stream));CK(cudaMemcpyAsync(s->in,s->pin,bytes,cudaMemcpyHostToDevice,s->stream));
  CK(cudaEventRecord(s->ev[1],s->stream));dim3 block(bx,by),grid((w+bx-1)/bx,(h-first+by-1)/by);
  if(tiled)tile<<<grid,block,(bx+2)*(by+2),s->stream>>>(s->in,s->out,w,h,first,offset);
  else base<<<grid,block,0,s->stream>>>(s->in,s->out,w,h,first,offset);
  CK(cudaGetLastError());CK(cudaEventRecord(s->ev[2],s->stream));
  CK(cudaMemcpyAsync(s->pout,s->out,size_t(h-first)*w*2,cudaMemcpyDeviceToHost,s->stream));CK(cudaEventRecord(s->ev[3],s->stream));
 }
 auto c0=Clock::now();if(first>0)sobel(a,out,w,h,0,first,8);auto c1=Clock::now();t.cpu=ms(c0,c1);
 if(first<h){CK(cudaStreamSynchronize(s->stream));std::memcpy(out.data()+size_t(first)*w,s->pout,size_t(h-first)*w*2);}
 t.total=ms(start,Clock::now());
 if(first<h){float v;CK(cudaEventElapsedTime(&v,s->ev[0],s->ev[1]));t.h2d=v;CK(cudaEventElapsedTime(&v,s->ev[1],s->ev[2]));t.kernel=v;CK(cudaEventElapsedTime(&v,s->ev[2],s->ev[3]));t.d2h=v;}
 t.overlap=std::max(0.0,t.cpu+t.kernel-t.total);return t;
}
void device_info(){int n;CK(cudaGetDeviceCount(&n));if(n<1)throw std::runtime_error("No CUDA GPU");cudaDeviceProp p;CK(cudaGetDeviceProperties(&p,0));CK(cudaFree(nullptr));std::cout<<"GPU="<<p.name<<" CC="<<p.major<<'.'<<p.minor<<" bytes="<<p.totalGlobalMem<<"\n";}

