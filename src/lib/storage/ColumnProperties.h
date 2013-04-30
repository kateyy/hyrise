#pragma once
#include <cstdlib>
#include <vector>


class ColumnProperties;
typedef ColumnProperties* PColumnProperties;

enum ColumnType {
  ColDefaultType = 0,
  // TODO: BitCompressed, FixedLength ...
  ColDefaultDictVector
};

// struct ColumnProperty - compressed, sorted, ...


// store properties of multiple columns
// Use default values, if types are not set.
class ColumnProperties {
public:
  ColumnProperties();
  virtual ~ColumnProperties();

  ColumnType defaultType;
  void setType(size_t column, ColumnType type);
  ColumnType getType(size_t column);

private:
  std::vector<ColumnType> _types;
};

