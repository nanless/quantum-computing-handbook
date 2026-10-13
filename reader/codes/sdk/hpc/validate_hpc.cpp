// Original handbook validation; requires the complete pinned upstream checkout.
#include "qiskit/addon/sqd/postselection.hpp"
#include "qiskit/addon/sqd/subsampling.hpp"
#include "qiskit/addon/sqd/configuration_recovery.hpp"
#include <array>
#include <bitset>
#include <cmath>
#include <iostream>
#include <numeric>
#include <random>
#include <set>
#include <stdexcept>
#include <vector>
void require(bool ok) { if (!ok) throw std::runtime_error("independent invariant failed"); }
int main() {
  using namespace Qiskit::addon::sqd;
  std::vector<std::bitset<4>> bits;
  std::vector<double> weights;
  for (unsigned i=0;i<16;i++) { bits.emplace_back(i); weights.push_back(i+1); }
  auto selected=postselect_bitstrings(bits,weights,MatchesRightLeftHamming(1u,1u));
  require(selected.first.size()==4);
  std::set<unsigned long> expected{5,6,9,10}, observed;
  for (const auto &s:selected.first) observed.insert(s.to_ulong());
  require(expected==observed);
  require(std::abs(std::accumulate(selected.second.begin(),selected.second.end(),0.)-1)<1e-12);
  // Independent normalization: surviving weights are 6,7,10,11 with total 34.
  for (size_t i=0;i<selected.first.size();i++)
    require(std::abs(selected.second[i]-(selected.first[i].to_ulong()+1)/34.)<1e-12);
  std::mt19937 r1(72),r2(72);
  auto batches=subsample_multiple_batches(selected.first,selected.second,3,8,r1);
  auto repeated=subsample_multiple_batches(selected.first,selected.second,3,8,r2);
  require(batches==repeated);
  for (const auto &b:batches) {std::set<unsigned long> unique;for(auto s:b) unique.insert(s.to_ulong());require(unique.size()==3);}
  std::array<std::vector<double>,2> occ{{{.3,.7},{.6,.4}}};
  std::mt19937 r3(72),r4(72);
  auto recovered=recover_configurations(bits,weights,occ,{1,1},r3);
  auto again=recover_configurations(bits,weights,occ,{1,1},r4);
  require(recovered==again);
  for(auto s:recovered.first) {require((s.to_ulong()&3)==1||(s.to_ulong()&3)==2);require((s.to_ulong()>>2)==1||(s.to_ulong()>>2)==2);}
  require(std::abs(std::accumulate(recovered.second.begin(),recovered.second.end(),0.)-1)<1e-12);
  std::cout << "{\"status\":\"passed\",\"seed\":72,\"selected\":4,\"batches\":8,\"batch_size\":3,\"recovered\":" << recovered.first.size() << ",\"openmp\":false,\"mpi\":false}\n";
}
