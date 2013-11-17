// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#include "testing/test.h"

#include "helper.h"

namespace hyrise {
namespace access {

template <int I>
struct QueryId {
  static int id() { return I; }
};

template <typename Query>
class TpcchQueryTest : public AccessTest {
protected:
  virtual void SetUp() {
    AccessTest::SetUp();
    
    // load input tables
    executeAndWait(loadFromFile("test/tpcc/load_tpcc_tables.json"));

    // load expected output table
    StorageManager *sm = StorageManager::getInstance();
    sm->loadTableFile("refTable", "tpcch/query"+std::to_string(Query::id())+"_result.tbl");

    // load query from file
    query = loadFromFile("test/tpcch/query"+std::to_string(Query::id())+".json");
  }

  std::shared_ptr<AbstractTable> reference() {
    StorageManager *sm = StorageManager::getInstance();
    return sm->getTable("refTable");
  }
  std::string query;
};

// Define here which queries we want to execute
typedef ::testing::Types<
  QueryId<1>,
  QueryId<3>,
  QueryId<6>,
  QueryId<18>
> Queries;

TYPED_TEST_CASE(TpcchQueryTest, Queries);

TYPED_TEST(TpcchQueryTest, query_execute_test) {
  const auto& out = executeAndWait(this->query);

  ASSERT_TRUE(out != nullptr);

  ASSERT_TABLE_EQUAL(out, this->reference());
}

}
}