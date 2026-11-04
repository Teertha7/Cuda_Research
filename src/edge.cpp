#include "edge.hpp"
#include <cmath>
#include <algorithm>
#include <omp.h>
#include <stdexcept>
Image generate(int w,int h,int p) {
 Image a(size_t(w)*h); uint32_t s=0x12345678u;
 for(int y=0;y<h;++y) for(int x=0;x<w;++x) {
  s^=s<<13; s^=s>>17; s^=s<<5;
  a[size_t(y)*w+x]=p==0?uint8_t(s&255):p==1?uint8_t(((x/17+y/23)%2)*255):uint8_t((x*255LL/std::max(1,w-1)+y*127LL/std::max(1,h-1))%256);
 } return a;
}
void sobel(const Image& a,Edges& out,int w,int h,int begin,int end,int threads) {
 #pragma omp parallel for schedule(static) num_threads(threads>0?threads:1) if(threads>0)
 for(int y=begin;y<end;++y) for(int x=0;x<w;++x) {
  const size_t i=size_t(y)*w+x;
  if(x==0||y==0||x==w-1||y==h-1) {out[i]=0;continue;}
  int gx=-a[i-w-1]+a[i-w+1]-2*a[i-1]+2*a[i+1]-a[i+w-1]+a[i+w+1];
  int gy=-a[i-w-1]-2*a[i-w]-a[i-w+1]+a[i+w-1]+2*a[i+w]+a[i+w+1];
  out[i]=uint16_t(std::abs(gx)+std::abs(gy));
 }
}
Edges canny(const Image& a,int w,int h,int threads) {
 const size_t n=a.size(); std::vector<float> smooth(n),mag(n),angle(n),nms(n); Edges out(n);
 const int k[5]={1,4,6,4,1};
 #pragma omp parallel for schedule(static) num_threads(threads>0?threads:1) if(threads>0)
 for(int y=0;y<h;++y) for(int x=0;x<w;++x) {
  float v=0; for(int j=-2;j<=2;++j) for(int i=-2;i<=2;++i)
   v+=k[j+2]*k[i+2]*a[size_t(std::clamp(y+j,0,h-1))*w+std::clamp(x+i,0,w-1)];
  smooth[size_t(y)*w+x]=v/256.0f;
 }
 #pragma omp parallel for schedule(static) num_threads(threads>0?threads:1) if(threads>0)
 for(int y=1;y<h-1;++y) for(int x=1;x<w-1;++x) {
  size_t i=size_t(y)*w+x;
  float gx=-smooth[i-w-1]+smooth[i-w+1]-2*smooth[i-1]+2*smooth[i+1]-smooth[i+w-1]+smooth[i+w+1];
  float gy=-smooth[i-w-1]-2*smooth[i-w]-smooth[i-w+1]+smooth[i+w-1]+2*smooth[i+w]+smooth[i+w+1];
  mag[i]=std::sqrt(gx*gx+gy*gy); float d=std::atan2(gy,gx)*180.0f/3.14159265358979323846f;
  angle[i]=d<0?d+180:d;
 }
 #pragma omp parallel for schedule(static) num_threads(threads>0?threads:1) if(threads>0)
 for(int y=1;y<h-1;++y) for(int x=1;x<w-1;++x) {
  size_t i=size_t(y)*w+x; float d=angle[i],u,v;
  if(d<22.5f||d>=157.5f){u=mag[i-1];v=mag[i+1];}
  else if(d<67.5f){u=mag[i-w-1];v=mag[i+w+1];}
  else if(d<112.5f){u=mag[i-w];v=mag[i+w];}
  else {u=mag[i-w+1];v=mag[i+w-1];}
  if(mag[i]>=u&&mag[i]>=v)nms[i]=mag[i];
 }
 // One global serial queue preserves connectivity across all row boundaries.
 std::vector<size_t> queue; queue.reserve(n/8);
 for(size_t i=0;i<n;++i) if(nms[i]>=100){out[i]=255;queue.push_back(i);}
 for(size_t q=0;q<queue.size();++q) {
  size_t i=queue[q]; int y=int(i/w),x=int(i%w);
  for(int dy=-1;dy<=1;++dy)for(int dx=-1;dx<=1;++dx){
   int yy=y+dy,xx=x+dx;if(yy<0||yy>=h||xx<0||xx>=w)continue;
   size_t j=size_t(yy)*w+xx;
   if(!out[j]&&nms[j]>=40){out[j]=255;queue.push_back(j);}
  }
 } return out;
}

