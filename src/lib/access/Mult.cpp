// Copyright (c) 2012 Hasso-Plattner-Institut fuer Softwaresystemtechnik GmbH. All rights reserved.
#include "access/Mult.h"

#include "access/system/BasicParser.h"
#include "access/system/QueryParser.h"

#include "storage/AbstractTable.h"
#include "storage/MutableVerticalTable.h"
#include "storage/TableBuilder.h"

#include <cmath>

namespace hyrise {
namespace access {

namespace {
  auto _ = QueryParser::registerPlanOperation<Mult>("Mult");
}

Mult::~Mult() {
}

void Mult::executePlanOperation() {
  
  auto in = std::const_pointer_cast<storage::AbstractTable>(input.getTable(0));

  storage::TableBuilder::param_list list;

  if(getVType() == 0){
    list.append().set_type("INTEGER").set_name(getColName());
  }else{
    list.append().set_type("FLOAT").set_name(getColName());
  }

  auto resultTable = storage::TableBuilder::build(list);

  resultTable->resize(in->size());

  for(size_t row = 0; row < in->size(); row++) {
    float mulValue = getFactor();
    for(size_t col = 0; col < _field_definition.size(); col++) {
      if(in->typeOfColumn(_field_definition[col]) == IntegerType)
        mulValue *= in->getValue<hyrise_int_t>(_field_definition[col], row);
      else
        mulValue *= in->getValue<hyrise_float_t>(_field_definition[col], row);
    }
    if(getVType() == 0){
      resultTable->setValue<hyrise_int_t>(0, row, (hyrise_int_t)mulValue);
    }else{
      resultTable->setValue<hyrise_float_t>(0, row, mulValue);
    }
  }

  addResult(std::make_shared<storage::MutableVerticalTable>(
    std::vector<storage::atable_ptr_t> {in, resultTable}));
}

std::shared_ptr<PlanOperation> Mult::parse(const Json::Value &data) {
  std::shared_ptr<Mult> instance = BasicParser<Mult>::parse(data);

  if(!data.isMember("fields") || data["fields"].size()<1){
    throw std::runtime_error("At least one field should be defined in \"fields\"");
  }

  instance->setFactor(data.isMember("factor") ? data["factor"].asFloat() : 1.f);

  if(data.isMember("as")){
    instance->setColName(data["as"].asString());
  }else{
    throw std::runtime_error("'as' has to be defined");
  }

  if(data.isMember("vtype")){
    instance->setVType(data["vtype"].asInt());
    if(instance->getVType()!=1 && instance->getVType()!=0){
      throw std::runtime_error("vtype has to be 0 or 1 for int or float");
    }
  }else{
    throw std::runtime_error("'vtype' has to be defined (0 or 1 for int or float)");
  }

  return instance;
}

const std::string Mult::vname() {
  return "Mult";
}

void Mult::setVType(const int &vtype){
  _vtype = vtype;
}

void Mult::setFactor(const float &factor){
  _factor = factor;
}

void Mult::setColName(const std::string &colName){
  _colName = colName;
}

int Mult::getVType() const {
  return _vtype;
}

float Mult::getFactor() const {
  return _factor;
}

std::string Mult::getColName() const {
  return _colName;
}

}
}
