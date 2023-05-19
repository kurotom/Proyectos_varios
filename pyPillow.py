from PIL import Image
import os

class CompressIMG(object):
    listExtentions = ['apng', 'gif', 'jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp', 'png', 'svg', 'webp', 'bmp']

    def __init__(self, exts=listExtentions, file=''):
        if type(file) == str:
            self.path = os.path.abspath(file)
            self.img = Image.open(self.path)

        elif type(file) == list or type(file) == tuple:
            self.path = [os.path.abspath(i) for i in file]
            self.img = [Image.open(x) for x in self.path]


    def convert(self):
        def name_final(original_name, extention):
            return original_name.replace(f'.{extention}', f'_compressed.{extention}')

        if type(self.path) == list:
            for ext in self.listExtentions:
                for item in self.img:
                    if item.filename.endswith(ext):
                        item.save(name_final(item.filename, ext), optimize=True, quality=10)

        elif type(self.path) == str:
            ext = [i for i in self.listExtentions if self.img.filename.endswith(i)][0]
            self.img.save(name_final(self.img.filename, ext), optimize=True, quality=10)

    def fileExtention(self):
        return f'Extention: {self.img.format}'




