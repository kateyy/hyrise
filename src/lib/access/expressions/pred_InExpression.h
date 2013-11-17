// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#ifndef SRC_LIB_ACCESS_PRED_INEXPRESSION_H_
#define SRC_LIB_ACCESS_PRED_INEXPRESSION_H_

#include "pred_common.h"
#include <vector>
#include <algorithm>
#include "helper/stringhelpers.h"

template <typename T>
class InExpression : public SimpleFieldExpression {
public:
  InExpression(size_t i, field_t f, hyrise_string_t value):
      SimpleFieldExpression(i, f),
      values(parseValues(value))
  {}

  InExpression(size_t i, field_name_t f, hyrise_string_t value):
      SimpleFieldExpression(i, f),
      values(parseValues(value))
  {}

  InExpression(hyrise::storage::c_atable_ptr_t _table, field_t _field, hyrise_string_t value):
      SimpleFieldExpression(_table, _field),
      values(parseValues(value))
  {}

  virtual ~InExpression() { }

  inline virtual bool operator()(size_t row) {
    T currentValue = table->getValue<T>(field, row);
    // check if we can find currentValue in our list of values
    return std::find(values.cbegin(), values.cend(), currentValue) != values.cend();
  }

protected:
  const std::vector<T> values;
  const std::vector<T> parseValues(const hyrise_string_t inValuesString) const {
    std::vector<hyrise_string_t> strings;
    splitString(strings, inValuesString, ";");
    std::vector<T> result;
    for (const hyrise_string_t & s: strings) {
      result.push_back(fromString<T>(s));
    }
    return result;
  }
};

#endif  // SRC_LIB_ACCESS_PRED_INEXPRESSION_H_
