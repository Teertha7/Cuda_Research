// Isolated compute-window overlap validation; not an end-to-end benchmark.
#include "../src/cuda.cu"
#include <omp.h>
int main(){try{
 omp_set_dynamic(0);const int w=4096,h=4096,first=1024,offset=first-1;
 Image a=generate(w,h,0);Edges out(a.size()),ref(a.size());sobel(a,ref,w,h,0,h,0);
 unsigned char* in=nullptr;unsigned short* result=nullptr;cudaStream_t stream;cudaEvent_t e0,e1;
 CK(cudaMalloc(&in,size_t(h-offset)*w));CK(cudaMalloc(&result,size_t(h-first)*w*2));
 CK(cudaMemcpy(in,a.data()+size_t(offset)*w,size_t(h-offset)*w,cudaMemcpyHostToDevice));CK(cudaStreamCreateWithFlags(&stream,cudaStreamNonBlocking));CK(cudaEventCreate(&e0));CK(cudaEventCreate(&e1));
 std::cout<<"repetition,cpu_ms,kernel_ms,window_ms,overlap_lower_bound_ms,correct\n";
 for(int r=-3;r<20;++r){
  auto start=Clock::now();CK(cudaEventRecord(e0,stream));base<<<dim3((w+15)/16,(h-first+15)/16),dim3(16,16),0,stream>>>(in,result,w,h,first,offset);CK(cudaGetLastError());CK(cudaEventRecord(e1,stream));
  auto c0=Clock::now();sobel(a,out,w,h,0,first,8);auto c1=Clock::now();CK(cudaStreamSynchronize(stream));auto end=Clock::now();float kernel;CK(cudaEventElapsedTime(&kernel,e0,e1));
  CK(cudaMemcpy(out.data()+size_t(first)*w,result,size_t(h-first)*w*2,cudaMemcpyDeviceToHost));if(out!=ref)throw std::runtime_error("Overlap probe output mismatch");
  if(r>=0)std::cout<<r<<','<<ms(c0,c1)<<','<<kernel<<','<<ms(start,end)<<','<<std::max(0.0,ms(c0,c1)+kernel-ms(start,end))<<",1\n";
 }
 cudaEventDestroy(e0);cudaEventDestroy(e1);cudaStreamDestroy(stream);cudaFree(in);cudaFree(result);return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
