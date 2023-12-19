import textwrap

import cairo

def generate_test_image():
	width = 618
	height = 1000
	with cairo.ImageSurface(cairo.Format.ARGB32, width, height) as surface:
		ctx = cairo.Context(surface)

		ctx.set_source_rgba(0.0, 0.0, 0.0, 1.0)
		ctx.rectangle(0, 0, width, height)
		ctx.fill()

		generate_corners(width, height, ctx)
		generate_edges(width, height, 5, ctx)
		gh = generate_gradients(16, width - 16, height // 2, ctx)

		upper_area = (16, 16, width - 32, height // 2 - gh - 32)
		generate_text(upper_area, False, "PNG rgbau8", ctx)

		lower_area = (16, height // 2 + gh + 16, width - 32, height // 2 - gh - 32)
		generate_text(lower_area, True, "PNG rgbau8", ctx)

		surface.write_to_png('test_png_rgbau8.png')

def generate_text(area, flip, format, ctx):
	padding = 32

	ctx.save()

	label_surface, label_size = fit_text(area[2], area[3], "TEST")
	label_x = (area[2] - label_size[0]) // 2
	label_y = 0

	assert label_size[1] < area[3]

	remaining = (area[2], area[3] - label_size[1] - padding)
	format_surface, format_size = fit_text(remaining[0], remaining[1], format)
	format_x = (area[2] - format_size[0]) // 2
	format_y = label_size[1] + padding

	vert_off = (area[3] - (label_size[1] + padding + format_size[1])) // 2
	label_y += vert_off
	format_y += vert_off

	g = cairo.LinearGradient(area[0], area[1], area[0] + area[2], area[1])
	if flip:
		g.add_color_stop_rgba(0.0, 0.0, 0.0, 0.0, 1.0)
		g.add_color_stop_rgba(1.0, 1.0, 1.0, 1.0, 1.0)
	else:
		g.add_color_stop_rgba(0.0, 1.0, 1.0, 1.0, 1.0)
		g.add_color_stop_rgba(1.0, 0.0, 0.0, 0.0, 1.0)
	ctx.set_source(g)
	ctx.mask_surface(label_surface, area[0] + label_x, area[1] + label_y)

	g = cairo.LinearGradient(area[0], area[1], area[0] + area[2], area[1])
	if flip:
		g.add_color_stop_rgba(0.0, 0.25, 0.25, 0.25, 1.0)
		g.add_color_stop_rgba(1.0, 0.75, 0.75, 0.75, 1.0)
	else:
		g.add_color_stop_rgba(0.0, 0.667, 0.667, 0.667, 1.0)
		g.add_color_stop_rgba(1.0, 0.333, 0.333, 0.333, 1.0)
	ctx.set_source(g)
	ctx.mask_surface(format_surface, area[0] + format_x, area[1] + format_y)

	ctx.restore()

def fit_text(width, height, text):
	surface = cairo.ImageSurface(cairo.Format.ARGB32, width, height)
	ctx = cairo.Context(surface)

	ctx.select_font_face('sans-serif', cairo.FontSlant.NORMAL, cairo.FontWeight.NORMAL)
	font_size = 32.0
	while True:
		try_font_size = font_size + 0.1
		ctx.set_font_size(try_font_size)
		extents = ctx.text_extents(text)
		if extents.width > width or extents.height > height:
			break
		else:
			font_size = try_font_size

	ctx.set_font_size(font_size)
	extents = ctx.text_extents(text)
	ctx.move_to(-extents.x_bearing, -extents.y_bearing)
	ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
	ctx.show_text(text)

	return surface, (round(extents.width), round(extents.height))

def generate_corners(width, height, ctx):
	pattern = textwrap.dedent("""
		## ##
		#
		  # #
		#
		# # #
	""").splitlines()[1:]
	pw = max(map(len, pattern))
	ph = len(pattern)

	ctx.save()
	for y in range(ph):
		for x in range(pw):
			try:
				p = pattern[y][x]
			except IndexError:
				p = ' '

			if p == '#':
				ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
			else:
				ctx.set_source_rgba(0.0, 0.0, 0.0, 1.0)

			ctx.rectangle(x, y, 1, 1)
			ctx.rectangle(width - 1 - x, y, 1, 1)
			ctx.rectangle(x, height - 1 - y, 1, 1)
			ctx.rectangle(width - 1 - x, height - 1 - y, 1, 1)
			ctx.fill()
	ctx.restore()


def generate_edges(width, height, thickness, ctx):
	gradient('x', (thickness + 1, 0),                  (width - thickness, thickness),  (1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 0.0, 1.0), ctx)
	gradient('x', (thickness + 1, height - thickness), (width - thickness, height),     (1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 0.0, 1.0), ctx)
	gradient('y', (0, thickness + 1),                  (thickness, height - thickness), (1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 0.0, 1.0), ctx)
	gradient('y', (width - thickness, thickness + 1),  (width, height - thickness),     (1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 0.0, 1.0), ctx)

def generate_gradients(x1, x2, ymid, ctx):
	GRAD_HEIGHT = 24
	grads = [
		((1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 0.0)),
		((0.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 0.0)),
		((1.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0)),
		((0.0, 1.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0)),
		((0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 0.0, 1.0)),
		((1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 0.0, 1.0)),
	]

	for i, grad in enumerate(grads):
		y = ymid - GRAD_HEIGHT * (len(grads) - i)
		gradient('x', (x1, y), (x2, y + GRAD_HEIGHT), grad[0], grad[1], ctx)

	for i, grad in enumerate(reversed(grads)):
		y = ymid + GRAD_HEIGHT * i
		gradient('x', (x1, y), (x2, y + GRAD_HEIGHT), grad[1], grad[0], ctx)

	return GRAD_HEIGHT * len(grads)

def gradient(dir, p1, p2, c1, c2, ctx):
	ctx.save()

	if dir == 'x':
		g = cairo.LinearGradient(p1[0], p1[1], p2[0], p1[1])
	elif dir == 'y':
		g = cairo.LinearGradient(p1[0], p1[1], p1[0], p2[1])
	else:
		raise ValueError("Invalid dir")

	g.add_color_stop_rgba(0.0, c1[0], c1[1], c1[2], c1[3])
	g.add_color_stop_rgba(1.0, c2[0], c2[1], c2[2], c2[3])
	ctx.rectangle(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1])
	ctx.set_source(g)
	ctx.set_operator(cairo.Operator.SOURCE)
	ctx.fill()

	ctx.restore()

def main():
	generate_test_image()

if __name__ == '__main__':
	main()
