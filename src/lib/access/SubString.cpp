// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#include "access/SubString.h"

#include "access/system/BasicParser.h"
#include "access/system/QueryParser.h"

#include "storage/AbstractTable.h"
#include "storage/MutableVerticalTable.h"
#include "storage/TableBuilder.h"

#include <iostream>

namespace hyrise {
namespace access {

namespace {
  auto _ = QueryParser::registerPlanOperation<SubString>("SubString");
}

SubString::~SubString() {
}

void SubString::executePlanOperation() {
  
  auto in = std::const_pointer_cast<storage::AbstractTable>(input.getTable(0));

  for (unsigned i = 0; i < _field_definition.size(); ++i) {
    if(in->typeOfColumn(_field_definition[i]) != StringType){
      throw std::runtime_error(in->nameOfColumn(_field_definition[i])+" is not of string type");
    }
  }

  storage::TableBuilder::param_list list;

  for (unsigned i = 0; i < _field_definition.size(); ++i){
    list.append().set_type("STRING").set_name(getColName(i));
  }
  auto resultTable = storage::TableBuilder::build(list);

  resultTable->resize(in->size());

  for(size_t row = 0; row < in->size(); row++) {
    for(size_t col = 0; col < _field_definition.size(); col++) {
      resultTable->setValue<hyrise_string_t>(col, row, 
        (in->getValue<std::string>(_field_definition[col], row)).substr(getStart(col), getCount(col)) );
    }
  }

  addResult(std::make_shared<storage::MutableVerticalTable>(
    std::vector<storage::atable_ptr_t> {in, resultTable}));
}

std::shared_ptr<PlanOperation> SubString::parse(const Json::Value &data) {
  std::shared_ptr<SubString> instance = BasicParser<SubString>::parse(data);

  size_t colCount = 0;

  if(data.isMember("fields")){
    colCount = data["fields"].size();
  }else{
    throw std::runtime_error("No fields defined");
  }
  if(!data.isMember("strstart") || colCount != data["strstart"].size()){
    throw std::runtime_error("number of definitions in 'strstart' unequal to number of selected columns");
  }
  if(!data.isMember("strcount") || colCount != data["strcount"].size()){
    throw std::runtime_error("number of definitions in 'strcount' unequal to number of selected columns");
  }
  if(!data.isMember("as") || colCount != data["as"].size()){
    throw std::runtime_error("number of definitions in 'as' unequal to number of selected columns");
  }

  for (int i = 0; i < int(colCount); ++i) {
    instance->addStart(data["strstart"][i].asInt());
    instance->addCount(data["strcount"][i].asInt());
    instance->addColName(data["as"][i].asString());
  }

  return instance;
}

const std::string SubString::vname() {
  return "SubString";
}


void SubString::addStart(const int &start){
  _start.push_back(start);
}

void SubString::addCount(const int &count){
  _count.push_back(count);
}

void SubString::addColName(const std::string &colName){
  _colName.push_back(colName);
}
  
int SubString::getStart(int col) const {
  return _start.at(col);
}
  
int SubString::getCount(int col) const {
  return _count.at(col);
}

std::string SubString::getColName(int col) const {
  return _colName.at(col);
}

}
}
