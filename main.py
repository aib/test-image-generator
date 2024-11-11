import numpy
import cv2

import gen

def generate_images():
	width = 618
	height = 1000

	def gen_img(format, ftype, ext=None):
		label = f'{ftype} {format}'
		print(f'{label}...')
		if ext is None: ext = ftype.lower()
		arr = gen.generate_test_image(width, height, label)
		cv2.imwrite(f'output/test_{ftype.lower()}_{format.lower()}.{ext}', gen.formats[format](arr))
		arr = gen.generate_test_image(width, height, None)
		cv2.imwrite(f'output/test_nl_{format.lower()}.{ext}', gen.formats[format](arr))

	def gen_raw(format, conv, dtype=None):
		print(f"RAW {format}...")
		numpy.ascontiguousarray(
			conv(gen.generate_test_image(width, height, f'RAW {format}')),
			dtype=dtype,
		).tofile(f'output/test_raw_{width}x{height}_{format}.raw')
		numpy.ascontiguousarray(
			conv(gen.generate_test_image(width, height, None)),
			dtype=dtype,
		).tofile(f'output/test_nl_{width}x{height}_{format}.raw')

	gen_img('RGBA16', 'PNG')
	gen_img('RGB16',  'PNG')
#	gen_img('GA16',   'PNG')
	gen_img('G16',    'PNG')
	gen_img('RGBA8',  'PNG')
	gen_img('RGB8',   'PNG')
#	gen_img('GA8',    'PNG')
	gen_img('G8',     'PNG')

	gen_img('RGBA8',  'BMP')
	gen_img('RGB8',   'BMP')
	gen_img('G8',     'BMP')

	gen_img('RGBA16', 'TIFF', ext='tif')
	gen_img('RGB16',  'TIFF', ext='tif')
#	gen_img('GA16',   'TIFF', ext='tif')
	gen_img('G16',    'TIFF', ext='tif')
	gen_img('RGBA8',  'TIFF', ext='tif')
	gen_img('RGB8',   'TIFF', ext='tif')
#	gen_img('GA8',    'TIFF', ext='tif')
	gen_img('G8',     'TIFF', ext='tif')

	gen_img('RGB8',   'JPEG', ext='jpg')
	gen_img('G8',     'JPEG', ext='jpg')

	gen_raw('rgbau16le', gen.formats['RGBA16'], '<u2')
	gen_raw('rgbu16le', gen.formats['RGB16'], '<u2')
	gen_raw('gu16le', gen.formats['G16'], '<u2')

	gen_raw('rgbau8', gen.formats['RGBA8'])
	gen_raw('rgbu8', gen.formats['RGB8'])
	gen_raw('gu8', gen.formats['G8'])

if __name__ == '__main__':
	generate_images()
