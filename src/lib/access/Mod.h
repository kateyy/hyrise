// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#ifndef SRC_LIB_ACCESS_MOD_H_
#define SRC_LIB_ACCESS_MOD_H_

#include "access/system/ParallelizablePlanOperation.h"

namespace hyrise {
namespace access {

class Mod : public ParallelizablePlanOperation {
public:
  virtual ~Mod();

  void executePlanOperation();
  static std::shared_ptr<PlanOperation> parse(const Json::Value &data);
  const std::string vname();

  void setDivisor(const float &divisor);
  void setVType(const int &vtype);
  void setColName(const std::string &colName);
  
  float getDivisor() const;
  int getVType() const;
  std::string getColName() const;

private:
  float _divisor;
  int _vtype;
  std::string _colName;
};

}
}
#endif  // SRC_LIB_ACCESS_MOD_H_
