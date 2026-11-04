#pragma once
#include <vector>
#include <cstdint>
#include <string>
using Image = std::vector<uint8_t>;
using Edges = std::vector<uint16_t>;
Image generate(int w,int h,int pattern);
void sobel(const Image&,Edges&,int,int,int,int,int);
Edges canny(const Image&,int,int,int);
struct Timing { double h2d=0,kernel=0,d2h=0,cpu=0,total=0,overlap=0; };
class Gpu {
public:
 Gpu(int,int); ~Gpu();
 Timing run(const Image&,Edges&,int,int,double,bool,int,int);
private: void* state;
};
void device_info();
