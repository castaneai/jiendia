import pybinary.io
import jiendia.constant

class DataType:
    INT_UNSIGNED = 0
    STRING = 1
    BOOLEAN = 2
    INT_SIGNED = 3
    FLOAT = 4
  
@classmethod
  def to_string(cls, type):
    if type == DataType.INT_UNSIGNED:
      return 'INT_UNSIGNED'
    elif type == DataType.STRING:
      return 'STRING'
    elif type == DataType.BOOLEAN:
      return 'BOOLEAN'
    elif type == DataType.INT_SIGNED:
      return 'INT_SIGNED'
    elif type == DataType.FLOAT:
      return 'FLOAT'
  
class DataColumn:
  
  def __init__(self, name):
    self.name = name
    self.type = DataType.INT_SIGNED
    
  def __str__(self):
    return 'jiendia.DataColumn(name: {0}, type: {1})'.format(self.name, DataType.to_string(self.type))

class DataTable:
  
  def __init__(self, name, stream):
    self.name = name
    self.columns = []
    self.rows = []
    
    DATATYPE_POSITION = 8204
    ROW_POSITION = 8716
    COLUMN_NAME_LENGTH = 64
    
    reader = pybinary.io.BinaryReader(stream, jiendia.constant.ENCODING)
    stream.seek(4)
    column_count = reader.read_int32()
    row_count = reader.read_int32()
    
    # テーブルのカラム情報を読み込む
    # 最初にカラム名が並んでいて、その下にカラムのデータ型が並んでいる
    for _ in range(column_count):
      column = DataColumn(reader.read_string(COLUMN_NAME_LENGTH))
      self.columns.append(column)
    
    stream.seek(DATATYPE_POSITION)
    for column in self.columns:
      column.type = reader.read_int32()
      
    # すべてのテーブルには最初にIDというSIGNED_INTのカラムが暗黙的に挿入される
    # 行データにはちゃんと存在するのにカラム情報には存在しないのでここで無理矢理挿入することにしている
    self.columns.insert(0, DataColumn("ID"))
    
    # 行データを読み込む
    stream.seek(ROW_POSITION)
    for _ in range(row_count):
      row = []
      for column in self.columns:
        if column.type in [DataType.INT_SIGNED, DataType.INT_UNSIGNED, DataType.BOOLEAN]:
          row.append(reader.read_int32())
        elif column.type == DataType.FLOAT:
          row.append(reader.read_float())
        elif column.type == DataType.STRING:
          string_length = reader.read_short()
          if 0 < string_length:
            row.append(reader.read_string(string_length))
          else:
            row.append("")
        else:
          raise ValueError("invalid datatype found: {0}".format(column.type))
      self.rows.append(tuple(row))
      
if __name__ == '__main__':
  import jiendia.package
  import jiendia.util
  pack = jiendia.package.Package(jiendia.util.get_latale_directory_path() + '\ROWID.SPF')
  resource = pack.resources[0]
  table = DataTable(resource.name, resource.stream)
  print([column.name for column in table.columns])
  print(table.rows[0])
