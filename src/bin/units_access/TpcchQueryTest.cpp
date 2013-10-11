// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
// #include "TpccTableLoadHelper.h"

#include "testing/test.h"
#include "helper.h"
#include "helper/Settings.h"
#include <json.h>
#include <access.h>
#include <io.h>
#include <storage.h>

#include <io/shortcuts.h>
#include "taskscheduler/SharedScheduler.h"

#include <iostream>

namespace hyrise {
namespace access {

class TpcchQueryTest : public AccessTest {};


TEST_F(TpcchQueryTest, analyt_query1) {
  // StorageManager::getInstance()->loadTableFile("lin_xxs", "lin_xxs.tbl");
  StorageManager::getInstance()->loadTableFile("query1_result", "tpcch/query1_result.tbl");

  std::string q = loadFromFile("test/tpcch/query1.json");

  const auto& out = executeAndWait(q);

  ASSERT_FALSE(!out);

  ASSERT_TABLE_EQUAL(out, StorageManager::getInstance()->getTable("query1_result"));

  // for (int i=0; i < 10; ++i)
  //   std::cout << "Tpcch " << out->metadataAt(i)->getName() << std::endl;

  StorageManager::getInstance()->removeAll();
}

}
}