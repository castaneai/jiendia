import os
import struct
import io
import pybinary.io
import jiendia.constant

RESOURCE_STRUCT_SIZE = 140

class Package:
  
  def __init__(self, path):
    self.path = path
    self.resources = []
    
    with open(path, 'rb') as stream:
      stream.seek(-RESOURCE_STRUCT_SIZE, os.SEEK_END)
      length = struct.unpack("<l", stream.read(4))[0]
      stream.seek(-(length + 4), os.SEEK_CUR)
      data = stream.read(length)
    
    stream = io.BytesIO(data)
    reader = pybinary.io.BinaryReader(stream, jiendia.constant.ENCODING)
    resource_count = int(len(data) / RESOURCE_STRUCT_SIZE)
    for _ in range(resource_count):
      path = reader.read_string(128)
      start_position = reader.read_int32()
      size = reader.read_int32()
      self.resources.append(Resource(self, path, start_position, size))
      stream.seek(4, os.SEEK_CUR)
      
  def find_resources(self, keyword):
    result = []
    for resource in self.resources:
      if -1 < resource.path.find(keyword):
        result.append(resource)
    return result
    
class Resource:
  
  def __init__(self, package, path, start_position, size):
    self.package = package
    self.path = path
    self.start_position = start_position
    self.size = size
    
  @property
  def name(self):
    return os.path.splitext(os.path.basename(self.path))[0]
    
  @property
  def stream(self):
    with open(self.package.path, "rb") as package_stream:
      package_stream.seek(self.start_position)
      stream = io.BytesIO(package_stream.read(self.size))
    return stream
  
  def __repr__(self):
    return 'jiendia.package.Resource(path: {0})'.format(self.path)
  
if __name__ == '__main__':
  import jiendia.util
  package = Package(jiendia.util.get_latale_directory_path() + '/ROWID.SPF')
  print(package.resources)
  
