// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#ifndef SRC_LIB_ACCESS_PRED_LIKEEXPRESSION_H_
#define SRC_LIB_ACCESS_PRED_LIKEEXPRESSION_H_

#include <boost/regex.hpp>

#include "pred_common.h"
#include <helper/types.h>
#include <boost/regex.hpp>

class LikeExpression : public SimpleFieldExpression {
  boost::regex regExpr;

public:

  inline void initRegExpr(hyrise_string_t & reg_str)
  {
    std::string regStr(reg_str);
    regStr = boost::regex_replace(regStr,boost::regex(std::string("\%")), std::string(".*"));
    regStr = boost::regex_replace(regStr,boost::regex(std::string("_")), std::string("."));
    regExpr = boost::regex(regStr);
  }

  LikeExpression(size_t i, field_t f, hyrise_string_t _value):
      SimpleFieldExpression(i, f)
  {
    initRegExpr(_value);
  }

  LikeExpression(size_t i, field_name_t f, hyrise_string_t _value):
      SimpleFieldExpression(i, f)
  {
    initRegExpr(_value);
  }

  LikeExpression(const hyrise::storage::c_atable_ptr_t& _table, field_t _field, hyrise_string_t _value) :
      SimpleFieldExpression(_table, _field)
  {
    initRegExpr(_value);
  }

  virtual ~LikeExpression() { }

  inline virtual bool operator()(size_t row) {
    std::string currentValue = std::string(table->getValue<hyrise_string_t>(field, row));

    return boost::regex_match(currentValue, regExpr);
  }
};

#endif // SRC_LIB_ACCESS_PRED_LIKEEXPRESSION_H_
