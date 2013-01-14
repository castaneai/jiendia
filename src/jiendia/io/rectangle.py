import io
import collections
import pybinary.io

RectangleGroup = collections.namedtuple('RectangleGroup',
	'name, rectangles')

Rectangle = collections.namedtuple('Rectangle',
	'pattern, x, y, rotate_x, rotate_y, left, top, right, bottom, filename')

class RectangleTable(object):
	
	def __init__(self, stream, encoding):
		self.rectangle_groups = []
		
		reader = pybinary.io.BinaryReader(stream, encoding)
		stream.seek(4, io.SEEK_CUR)
		group_count = reader.read_int32()
		
		for _ in range(group_count):
			contains_rectangle_count = reader.read_int32()
			group_name = reader.read_string(16)
			stream.seek(116, io.SEEK_CUR)
			rectangles = []
			for __ in range(contains_rectangle_count):
				pattern = reader.read_int32()
				x = reader.read_int32()
				y = reader.read_int32()
				rotate_x = reader.read_float()
				rotate_y = reader.read_float()
				left = reader.read_int32()
				top = reader.read_int32()
				right = reader.read_int32()
				bottom = reader.read_int32()
				filename = reader.read_string(24)
				stream.seek(104, io.SEEK_CUR)
				rectangle = Rectangle._make(
					(pattern, x, y, rotate_x, rotate_y, left, top, right, bottom, filename)
				)
				rectangles.append(rectangle)
			rectangle_group = RectangleGroup._make((group_name, rectangles))
			self.rectangle_groups.append(rectangle_group)
			
if __name__ == '__main__':
	import jiendia.util
	import jiendia.package
	pack = jiendia.package.Package(jiendia.util.get_latale_directory_path() + '/ZENNE.SPF')
	resource = pack.find_resources('WEAPON_SPECIAL.TBL')[0]
	table = RectangleTable(resource.name, resource.stream)
	for group in table.rectangle_groups:
		print(group)
