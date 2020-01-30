from jinja2 import Environment, FileSystemLoader
import os 
import glob
root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment( loader = FileSystemLoader(templates_dir) )
template = env.get_template('imageview.html')
 
 
filename = os.path.join(root,'upload/static','imageview_updated.html')
slitted_path = root.split("/")
image_path = os.path.join("/".join(slitted_path[:-1]),'instance/images/')
image_path2 = '../../../instance/images/'
locations = []
for folder in glob.glob(image_path + "*/"):
	print(folder.split("/")[-2])
	locations.append(image_path2 + folder.split("/")[-2] + "/thumbnail.png")
	print(locations)

with open(filename, 'w') as fh:
    fh.write(template.render(
        paths    = locations,
    ))
 #https://code-maven.com/minimal-example-generating-html-with-python-jinja