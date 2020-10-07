from gimpfu import *
import os

class SS_Creator(object):
	# Requires a foler name 'in' and a folder name 'out' to function.
	# Not coded to auto create these directories.
	def __init__(self, *kwargs):
		self.xlen_base = 9
		self.ylen_act = 1
		
		self.flist = False
		self.base_d = [0,0]
		self.final_d = [0,0]
		self.cwd = os.getcwd()
		self.dirpath = self.cwd + '/in/'
		self.oname = ''
		
		self.set_grid()
		self.set_matrix()
		
	def set_grid(self):
		self.flist = os.listdir(self.dirpath)
		xlen = 0
		for i in self.flist:
			xlen += 1
			if xlen > self.xlen_base:
				self.ylen_act += 1
				xlen = 1
		
	def set_matrix(self):
		
		fi = self.dirpath + self.flist[0]
		f_end = len(self.flist[0]) - 4
		self.oname = self.flist[0][0:f_end] + '_ssheet.png'
		
		img = pdb.gimp_file_load(fi, fi)
		self.base_d[0] = img.width
		self.base_d[1] = img.height
		
		self.final_d[0] = self.base_d[0] * self.xlen_base
		self.final_d[1] = self.base_d[1] * self.ylen_act
		
		#pdb.gimp_img_delete(img)
		
		self.create_ss()
		
		
	def create_ss(self):
		main_img = pdb.gimp_image_new(self.final_d[0], self.final_d[1], RGB)
		
		x_dim = self.base_d[0]
		y_dim = self.base_d[1]
		
		cur_x = 0
		cur_y = 0
		
		for i in self.flist:
			fpath = self.dirpath + i
			layer = pdb.gimp_file_load_layer(main_img, fpath)
	
			pdb.gimp_image_insert_layer(main_img, layer, None, 0)
			pdb.gimp_layer_add_alpha(main_img.layers[0])
			main_img.layers[0].set_offsets(cur_x, cur_y)
			print('Added layer')
			cur_x += x_dim
			if cur_x > self.final_d[0]:
				cur_x = 0
				cur_y += self.base_d[1]
		oname = self.cwd + '/out/' + self.oname
		main_img.merge_visible_layers(NORMAL_MODE)
		pdb.file_png_save(main_img, main_img.layers[0], oname, oname, 0, 9, 1, 0, 0, 1, 1)
		
a = SS_Creator()
