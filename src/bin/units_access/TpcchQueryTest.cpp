// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#include "testing/test.h"
#include "io/StorageManager.h"

#include "helper.h"

namespace hyrise {
namespace access {

class TpcchQueryTest : public AccessTest {
protected:
  virtual void SetUp() {
    sm = StorageManager::getInstance();
    executeAndWait(loadFromFile("test/tpcc/load_tpcc_tables.json"));
  }
  virtual void TearDown() {
    sm->removeAll();
  }
  void loadReference(std::string fileName) {
    sm->loadTableFile("refTable", fileName);
  }
  std::shared_ptr<AbstractTable> reference() {
    return sm->getTable("refTable");
  }
  StorageManager * sm;
};

TEST_F(TpcchQueryTest, analyt_query1) {
  loadReference("tpcch/query1_result.tbl");

  const auto& out = executeAndWait(loadFromFile("test/tpcch/query1.json"));

  ASSERT_TRUE(out != nullptr);

  ASSERT_TABLE_EQUAL(out, reference());
}

TEST_F(TpcchQueryTest, DISABLED_analyt_query3) {
  // loadReference("tpcch/query3_result.tbl");

  std::cout << "ping" << std::endl;
  std::string query = loadFromFile("test/tpcch/query3.json");
  std::cout << "ping2" << std::endl;
  // ... null value at some point...
  // problem occurs only when executing here, (query3 works with curl)
  const auto& out = executeAndWait(query);
  std::cout << "ping3" << std::endl;
  ASSERT_TRUE(out != nullptr);

  // ASSERT_TABLE_EQUAL(out, sm->getTable("expectedTable"));
}

TEST_F(TpcchQueryTest, analyt_query6) {
  loadReference("tpcch/query6_result.tbl");

  const auto& out = executeAndWait(loadFromFile("test/tpcch/query6.json"));

  ASSERT_TRUE(out != nullptr);

  ASSERT_TABLE_EQUAL(out, reference());
}

TEST_F(TpcchQueryTest, analyt_query18) {
  loadReference("tpcch/query18_result.tbl");

  const auto& out = executeAndWait(loadFromFile("test/tpcch/query18.json"));

  ASSERT_TRUE(out != nullptr);

  ASSERT_TABLE_EQUAL(out, reference());
}

}
}