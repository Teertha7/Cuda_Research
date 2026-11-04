#include "edge.hpp"
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <limits>
static std::string token(std::istream& in){std::string t;while(in>>t){if(t[0]=='#'){in.ignore(std::numeric_limits<std::streamsize>::max(),'\n');continue;}return t;}throw std::runtime_error("Truncated PNM header");}
int main(int argc,char**argv){try{
 if(argc!=6)throw std::runtime_error("Usage: edge_image input.pgm|ppm output.pgm sobel|canny seq|omp|cuda|tiled|hybrid threads");
 std::ifstream in(argv[1],std::ios::binary);if(!in)throw std::runtime_error("Cannot open input");
 auto magic=token(in);int w=std::stoi(token(in)),h=std::stoi(token(in)),max=std::stoi(token(in));
 if((magic!="P5"&&magic!="P6")||w<1||h<1||w>16384||h>16384||max!=255)throw std::runtime_error("Requires 8-bit P5/P6, dimensions 1..16384");
 char sep;in.get(sep);if(sep=='\r'&&in.peek()=='\n')in.get();
 Image a(size_t(w)*h);if(magic=="P5")in.read(reinterpret_cast<char*>(a.data()),a.size());
 else {std::vector<unsigned char> rgb(a.size()*3);in.read(reinterpret_cast<char*>(rgb.data()),rgb.size());for(size_t i=0;i<a.size();++i)a[i]=uint8_t((77*rgb[3*i]+150*rgb[3*i+1]+29*rgb[3*i+2]+128)>>8);}
 if(!in)throw std::runtime_error("Truncated PNM pixels");
 std::string alg=argv[3],impl=argv[4];int threads=std::stoi(argv[5]);if(threads<1||threads>64)throw std::runtime_error("threads must be 1..64");Edges out(a.size());
 if(alg!="sobel"&&alg!="canny")throw std::runtime_error("Unknown algorithm");
 if(impl=="seq"||impl=="omp"){if(alg=="canny")out=canny(a,w,h,impl=="seq"?0:threads);else sobel(a,out,w,h,0,h,impl=="seq"?0:threads);}
 else if(impl=="cuda"||impl=="tiled"||impl=="hybrid"){
  if(alg!="sobel")throw std::runtime_error("CUDA Canny not implemented");if(impl=="hybrid"&&threads!=8)throw std::runtime_error("Hybrid requires 8 CPU threads");
  Gpu gpu(w,h);gpu.run(a,out,w,h,impl=="hybrid"?.5:0,impl=="tiled",16,16);
 }else throw std::runtime_error("Unknown implementation");
 std::ofstream f(argv[2],std::ios::binary);if(!f)throw std::runtime_error("Cannot open output");f<<"P5\n"<<w<<' '<<h<<'\n'<<(alg=="sobel"?2040:255)<<'\n';
 for(auto v:out){if(alg=="sobel")f.put(char(v>>8));f.put(char(v&255));}if(!f)throw std::runtime_error("Output write failed");return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
