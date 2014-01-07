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

  void addStart(const int &start);
  void addCount(const int &count);
  void addColName(const std::string &colName);
  int getStart(int col) const;
  int getCount(int col) const;
  std::string getColName(int col) const;

private:
  std::vector<int> _start;
  std::vector<int> _count;
  std::vector<std::string> _colName;
};

}
}
#endif  // SRC_LIB_ACCESS_SUBSTRING_H_
