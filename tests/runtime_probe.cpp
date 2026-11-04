#include <omp.h>
#include <iostream>
int main(){
 std::cout<<"MSVC="<<_MSC_VER<<" OpenMP_macro="<<_OPENMP<<" max_processors="<<omp_get_num_procs()<<'\n';omp_set_dynamic(0);
 for(int requested:{1,2,4,8,16}){int actual=0;
 #pragma omp parallel num_threads(requested)
 {
 #pragma omp single
 actual=omp_get_num_threads();
 }
 std::cout<<"requested="<<requested<<" actual="<<actual<<'\n';if(actual!=requested)return 1;
 }return 0;
}
