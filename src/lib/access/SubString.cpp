// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#include "access/SubString.h"

#include "access/system/BasicParser.h"
#include "access/system/QueryParser.h"

#include "storage/AbstractTable.h"
#include "storage/TableBuilder.h"

namespace hyrise {
namespace access {

namespace {
  auto _ = QueryParser::registerPlanOperation<SubString>("SubString");
}

SubString::~SubString() {
}

void SubString::executePlanOperation() {

  const auto &in = input.getTable(0);

  storage::TableBuilder::param_list list;
  for(size_t col=0; col<in->columnCount(); col++){
    switch(in->typeOfColumn(col)){
      case IntegerType:
        list.append().set_type("INTEGER").set_name(in->nameOfColumn(col));
      break;
      case FloatType:
        list.append().set_type("FLOAT").set_name(in->nameOfColumn(col));
      break;
      case StringType:
        list.append().set_type("STRING").set_name(in->nameOfColumn(col));
      break;
    }
  }

  list.append().set_type("STRING").set_name(getColName());
  auto resultTable = storage::TableBuilder::build(list);

  resultTable->resize(in->size());

  if(in->typeOfColumn(_field_definition[0]) == StringType){
    for(size_t row = 0; row < in->size(); row++) {
      for(size_t col = 0; col < in->columnCount(); col++) {
        switch(in->typeOfColumn(col)){
          case IntegerType:
            resultTable->setValue<hyrise_int_t>(col, row, in->getValue<hyrise_int_t>(col, row) );
          break;
          case FloatType:
            resultTable->setValue<hyrise_float_t>(col, row, in->getValue<hyrise_float_t>(col, row) );
          break;
          case StringType:
            resultTable->setValue<hyrise_string_t>(col, row, in->getValue<hyrise_string_t>(col, row) );
          break;
        }
      }

      resultTable->setValue<hyrise_string_t>(in->columnCount(), row, 
        (in->getValue<std::string>(_field_definition[0], row)).substr(getFrom(), getCount()) );
    }
  }

  addResult(resultTable);
  //addResult(std::make_shared<storage::MutableVerticalTable>(
    //std::vector<storage::atable_ptr_t> {in, resultTable}));
}

std::shared_ptr<PlanOperation> SubString::parse(const Json::Value &data) {
  std::shared_ptr<SubString> instance = BasicParser<SubString>::parse(data);

  int from = 0;
  int count = 0;
  if (data.isMember("from")) {
    from = data["from"].asInt();
  }else{
    throw std::runtime_error("Please define a start with member 'from'!");
  }
  if (data.isMember("count")) {
    count = data["count"].asInt();
  }else{
    throw std::runtime_error("Please define a length with member 'count'!");
  }
  instance->setRange(from, count);

  if (data.isMember("as")) {
    instance->setColName(data["as"].asString());
  }else{
    throw std::runtime_error("Please define a column name with member 'as'!");
  }

  return instance;
}

const std::string SubString::vname() {
  return "SubString";
}


void SubString::setRange(const int &from, const int &count){
  _from = from;
  _count = count;
}

void SubString::setColName(const std::string &colName){
  _colName = colName;
}
  
int SubString::getFrom() const {
  return _from;
}
  
int SubString::getCount() const {
  return _count;
}

std::string SubString::getColName() const {
  return _colName;
}

}
}
