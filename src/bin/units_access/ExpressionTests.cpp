// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#include "testing/test.h"
#include "access/SimpleTableScan.h"
#include "access/expressions/pred_LikeExpression.h"
#include "access/expressions/pred_InExpression.h"
#include "io/shortcuts.h"

namespace hyrise {
namespace access {

class ExpressionTests : public AccessTest {
protected:
  virtual void SetUp() {
    AccessTest::SetUp();    
    students = Loader::shortcuts::load("test/students.tbl");
    scan = new SimpleTableScan;
    scan->addInput(students);
  }
  virtual void TearDown() {
    delete scan;
  }
  const storage::c_atable_ptr_t result() {
    return scan->getResultTable();
  }
  size_t resultSize() {
    return result()->size();
  }
  storage::c_atable_ptr_t students;
  SimpleTableScan * scan;
};

TEST_F(ExpressionTests, like_wildcard_percent_test) {
  scan->setPredicate(new LikeExpression(0, field_name_t("name"), hyrise_string_t("\% Sch\%")));
  scan->execute();

  ASSERT_EQ(4u, resultSize());
  ASSERT_EQ(703591, result()->getValue<hyrise_int_t>(field_name_t("student_number"), 0));
  ASSERT_EQ(703594, result()->getValue<hyrise_int_t>(field_name_t("student_number"), 1));
  ASSERT_EQ(703597, result()->getValue<hyrise_int_t>(field_name_t("student_number"), 2));
  ASSERT_EQ(703598, result()->getValue<hyrise_int_t>(field_name_t("student_number"), 3));
}

TEST_F(ExpressionTests, like_wilrdcard_underscore_test)
{
  scan->setPredicate(new LikeExpression(0, field_name_t("city"), hyrise_string_t("Be_l_n")));
  scan->execute();

  ASSERT_EQ(34u, resultSize());
} 

TEST_F(ExpressionTests, in_string_test)
{
  scan->setPredicate(new InExpression<hyrise_string_t>(0, field_name_t("city"), hyrise_string_t("Frohnau;Berlin")));
  scan->execute();

  ASSERT_EQ(5u+34u, resultSize());
}

TEST_F(ExpressionTests, in_float_test)
{
  scan->setPredicate(new InExpression<hyrise_float_t>(0, field_name_t("grade"), hyrise_string_t("1.3;5")));
  scan->execute();

  ASSERT_EQ(7u+1u, resultSize());
}

TEST_F(ExpressionTests, in_int_test)
{
  scan->setPredicate(new InExpression<hyrise_int_t>(0, field_name_t("student_number"), hyrise_string_t("703591;703613;703625")));
  scan->execute();

  ASSERT_EQ(3u, resultSize());
  ASSERT_EQ(hyrise_string_t("Martina Schmitt"), result()->getValue<hyrise_string_t>(field_name_t("name"), 0));
  ASSERT_EQ(hyrise_string_t("Uta Budig"), result()->getValue<hyrise_string_t>(field_name_t("name"), 1));
  ASSERT_EQ(hyrise_string_t("Lukas Ruppersberger"), result()->getValue<hyrise_string_t>(field_name_t("name"), 2));
}
 
}
}
