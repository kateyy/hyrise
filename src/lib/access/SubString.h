// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#ifndef SRC_LIB_ACCESS_SUBSTRING_H_
#define SRC_LIB_ACCESS_SUBSTRING_H_

#include "access/system/ParallelizablePlanOperation.h"

namespace hyrise {
namespace access {

class SubString : public ParallelizablePlanOperation {
public:
  virtual ~SubString();

  void executePlanOperation();
  static std::shared_ptr<PlanOperation> parse(const Json::Value &data);
  const std::string vname();

  void setRange(const int &from, const int &count);
  void setColName(const std::string &colName);
  int getFrom() const;
  int getCount() const;
  std::string getColName() const;

private:
  int _from;
  int _count;
  std::string _colName;
};

}
}
#endif  // SRC_LIB_ACCESS_SUBSTRING_H_
