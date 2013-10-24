// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#include "access/SimpleTableScan.h"
#include "access/expressions/predicates.h"
#include "access/UnionAll.h"
#include "io/shortcuts.h"
#include "testing/test.h"

namespace hyrise {
namespace access {

class SimpleTableScanTests : public AccessTest {};

TEST_F(SimpleTableScanTests, basic_simple_table_scan_test) {
  storage::c_atable_ptr_t t = Loader::shortcuts::load("test/lin_xxs.tbl");
  auto expr = new EqualsExpression<storage::hyrise_int_t>(t, 0, 100);

  SimpleTableScan sts;
  sts.addInput(t);
  sts.setPredicate(expr);
  sts.execute();

  const auto &result = sts.getResultTable();

  ASSERT_EQ(1u, result->size());
  ASSERT_EQ(100, result->getValue<storage::hyrise_int_t>(0, 0));
}

// Same as above, but manually parallelized
TEST_F(SimpleTableScanTests, parallelized_simple_table_scan) {
  storage::c_atable_ptr_t t = Loader::shortcuts::load("test/lin_xxs.tbl");

  SimpleTableScan sts1;
  sts1.addInput(t);
  sts1.setPredicate(new EqualsExpression<storage::hyrise_int_t>(0, 0, 100));
  sts1.setPart(0);
  sts1.setCount(2);
  sts1.execute();

  SimpleTableScan sts2;
  sts2.addInput(t);
  sts2.setPredicate(new EqualsExpression<storage::hyrise_int_t>(0, 0, 100));
  sts2.setPart(1);
  sts2.setCount(2);
  sts2.execute();

  auto result1 = sts1.getResultTable();
  auto result2 = sts2.getResultTable();

  UnionAll ua;
  ua.addInput(result1);
  ua.addInput(result2);
  ua.execute();

  auto result = ua.getResultTable();

  ASSERT_EQ(1u, result->size());
  ASSERT_EQ(100, result->getValue<storage::hyrise_int_t>(0, 0));
}

TEST_F(SimpleTableScanTests, basic_like_test) {
  storage::c_atable_ptr_t t = Loader::shortcuts::load("test/students.tbl");
  storage::c_atable_ptr_t expected = Loader::shortcuts::load("test/students_like.tbl");

  ASSERT_TRUE(expected != nullptr);
  ASSERT_TRUE(t != nullptr);

  SimpleTableScan like1;
  like1.addInput(t);
  like1.setPredicate(new LikeExpression(
                      0, field_name_t("name"), hyrise_string_t("\% Sch\%")));
  like1.execute();

  auto result1 = like1.getResultTable();

  ASSERT_TRUE(result1 != nullptr);
  ASSERT_TABLE_EQUAL(expected, result1);

  SimpleTableScan like2;
  like2.addInput(t);
  like2.setPredicate(new LikeExpression(
                      0, field_name_t("city"), hyrise_string_t("Be_l_n")));
  like2.execute();

  auto result2 = like2.getResultTable();

  ASSERT_EQ(34u, result2->size());
}

}
}
