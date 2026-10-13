// Authored integration: full SQD-HPC plus official Random123 Philox4x64.
#include "qiskit/addon/sqd/configuration_recovery.hpp"
#include <Random123/philox.h>
#include <array>
#include <bitset>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <random>
#include <vector>
#include <stdexcept>
#ifdef _OPENMP
#include <omp.h>
#endif
class PhiloxStream {
 public:
 using result_type=std::uint64_t;
 using counter_type=std::array<result_type,4>;
 static constexpr int word_size=64;
 static constexpr result_type min(){return 0;}
 static constexpr result_type max(){return ~result_type(0);}
 explicit PhiloxStream(result_type value=73){seed(value);}
 void seed(result_type value){key={{value,0}};counter={{0,0,0,0}};cursor=4;}
 void set_counter(const counter_type &value){counter=value;cursor=4;}
 result_type operator()(){
  if(cursor==4){r123::Philox4x64::ctr_type c={{counter[0],counter[1],counter[2],counter[3]}};r123::Philox4x64::key_type k={{key[0],key[1]}};
   auto out=r123::Philox4x64()(c,k);for(unsigned i=0;i<4;i++)block[i]=out[i];cursor=0;
   // SDK sets word0 to stable work ID; consume draws through word3 instead.
   if(++counter[3]==0)if(++counter[2]==0)++counter[1];
  }
  return block[cursor++];
 }
 private:counter_type counter{},block{};std::array<result_type,2> key{};unsigned cursor=4;
};
void require(bool ok){if(!ok)throw std::runtime_error("Invariant failed");}
template<class R>void run(const char *name){
 std::vector<std::bitset<8>> bits;std::vector<double> weights;
 for(unsigned j=0;j<4000;j++){bits.emplace_back((37*j+5)&255);weights.push_back(1+(j%7));}
 std::array<std::vector<double>,2> occ{{{.3,.4,.5,.6},{.7,.6,.5,.4}}};R rng(73017);
 auto result=Qiskit::addon::sqd::recover_configurations(bits,weights,occ,{2,2},rng);
 double total=0;
 for(size_t i=0;i<result.first.size();i++){auto v=result.first[i].to_ulong();require(std::bitset<4>(v&15).count()==2);require(std::bitset<4>(v>>4).count()==2);total+=result.second[i];std::cout<<name<<" "<<result.first[i]<<" "<<std::setprecision(17)<<result.second[i]<<"\n";}
 require(std::abs(total-1)<1e-12);
}
int main(){
 PhiloxStream zero(0);std::array<std::uint64_t,4> expected{{0x16554d9eca36314cULL,0xdb20fe9d672d0fdcULL,0xd7e772cee186176bULL,0x7e68b68aec7ba23bULL}};
 for(auto value:expected)require(zero()==value);
 static_assert(Qiskit::addon::sqd::internal::is_counter_based_rng_v<PhiloxStream>);
 run<PhiloxStream>("philox4x64");run<std::mt19937>("mt19937");
}
