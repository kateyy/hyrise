// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#include "testing/test.h"
#include "access/SimpleTableScan.h"
#include "access/expressions/pred_LikeExpression.h"
#include "io/shortcuts.h"

namespace hyrise {
namespace access {

class LikeScanTests : public AccessTest {
protected:
    virtual void SetUp() {
        AccessTest::SetUp();        
        students = Loader::shortcuts::load("test/students.tbl");
        reference = Loader::shortcuts::load("test/students_like.tbl");
    }
    storage::c_atable_ptr_t students;
    storage::c_atable_ptr_t reference;
};

TEST_F(LikeScanTests, wildcard_percent_test) {
  SimpleTableScan like1;
  like1.addInput(students);
  like1.setPredicate(new LikeExpression(
                      0, field_name_t("name"), hyrise_string_t("\% Sch\%")));
  like1.execute();

  auto result1 = like1.getResultTable();

  ASSERT_TRUE(result1 != nullptr);
  ASSERT_TABLE_EQUAL(reference, result1);
}

TEST_F(LikeScanTests, wilrdcard_underscore_test)
{
  SimpleTableScan like2;
  like2.addInput(students);
  like2.setPredicate(new LikeExpression(
                      0, field_name_t("city"), hyrise_string_t("Be_l_n")));
  like2.execute();

  auto result2 = like2.getResultTable();

  ASSERT_EQ(34u, result2->size());
}

}
}