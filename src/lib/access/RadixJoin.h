// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#ifndef SRC_LIB_ACCESS_RADIXJOIN_H_
#define SRC_LIB_ACCESS_RADIXJOIN_H_

#include "access/system/PlanOperation.h"
#include "helper/types.h"

namespace hyrise {
namespace access {

class RadixJoin : public PlanOperation {
public:
  void executePlanOperation();
  static std::shared_ptr<PlanOperation> parse(const Json::Value &data);
  const std::string vname();
  void setBits1(const uint32_t b);
  void setBits2(const uint32_t b);
  uint32_t bits1() const;
  uint32_t bits2() const;

  virtual std::vector<taskscheduler::task_ptr_t> applyDynamicParallelization(size_t dynamicCount);

protected:
  // for determineDynamicCount
  // overridden from PlanOperation
  virtual size_t getTotalTableSize();
  virtual double min_mts_a() { return 0.208081598456783; }
  virtual double min_mts_b() { return -5.12106533314949; }
  virtual double a_a() { return 137.365747455395; }
  virtual double a_b() { return -3540.54997935958; }

private:
  uint32_t _bits1;
  uint32_t _bits2;
  static const size_t MaxParallelizationDegree = 24;

void distributePartitions(
          const int partitions,
          const int join_count,
          const int current_join,
          int &first,
          int &last) const;

void copyTaskAttributesFromThis(std::shared_ptr<PlanOperation> to);

std::vector<taskscheduler::task_ptr_t> build_probe_side(std::string prefix,
                                                          field_t &fields,
                                                          uint probe_par,
                                                          uint32_t bits1,
                                                          uint32_t bits2,
                                                          taskscheduler::task_ptr_t input);

std::vector<taskscheduler::task_ptr_t> build_hash_side(std::string prefix,
                                                          field_t &fields,
                                                          uint probe_par,
                                                          uint32_t bits1,
                                                          uint32_t bits2,
                                                          taskscheduler::task_ptr_t input);

};

}
}


#endif  // SRC_LIB_ACCESS_RADIXJOIN_H_
