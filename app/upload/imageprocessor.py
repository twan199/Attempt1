from PIL import Image 
import glob
import os
import shutil

def processor2(path):
	#for file in glob.glob(""):
	file = path + "original"
	quality_factor = 50
	#	print(file)
	im = Image.open(file)
	rgb_im = im.convert('RGB')
	rgb_im.save(path + "image.png",quality=quality_factor)
	rgb_im.save(path + "image.jpg",quality=quality_factor)
	rgb_im.save(path + "image.gif",quality=quality_factor)

	filesize = []
	filenames = []
	for image in glob.glob(path + "image.*"):
		filenames.append(image)
		filesize.append(os.path.getsize(image))
		if len(filenames) > 1:
			if filesize[0] > filesize[1]:
				os.remove(filenames[0])
				del(filesize[0])
				del(filenames[0])
			else:
				os.remove(filenames[1])
				del(filesize[1])
				del(filenames[1])
	os.rename(filenames[0], path + "optimized")
	if os.path.getsize(path + "optimized") > os.path.getsize(path + "original"):
		os.remove(path + "optimized")
		shutil.copy2(path + "original", path + "optimized")
		
	rgb_im.save(path + "thumbnail.png",quality=0.1)
	#im1 = Image.open(path + "optimized")
	#im1.show()
#processor("/mnt/c/Users/Bouts/Documents/Biogrund/Attempt1/instance/images/5c87ce8be061127f64c39d90c636c5acfb9265b54cc64a00e0b72a4379deda87/")