

import os 
from random import randint, sample
from operator import add, sub, mul, truediv as div
from functools import reduce
from PIL import Image, ImageDraw, ImageFont
from pprint import pprint
from glob import glob 

class puzzle():

    ops = {'+': add, '-': sub, '*': mul, '/': div}


    def __init__(self) -> None:
        
        
        self.level = 1

        
        while True:
            x, y, z = self.values()
            self.vars = x,y,z
            self.array = [self.one_var(x), self.two_vars(x,y), self.three_vars(x,y,z), self.footer_vars(x,y,z)]
            if all([i[-1] for i in self.array]):break
        pprint(self.array)
        
        self.icons = dict(zip([x,y,z],sample(self.load_icons(), k=3)))
        self.image = self.visualize()
        

    def load_icons(self):

        icons = glob('.\icons\*.png')
        return [Image.open(i) for i in icons]
        
    def values(self):
        
        max_value = 20 if self.level==1 else 25

        while True:
            x,y,z = randint(1,max_value), randint(1,max_value),randint(1,max_value)
            if len(list(set([x,y,z])))==3:
                return x,y,z

    def one_var(self, x):
        s = [x,'+',x,'+',x]
        r = eval(''.join(map(str,s)))

        if self.level==1:
            if r/3>12:
                r = 0
        if r in self.vars:
            r = 0
        return s+['=', r]

    def two_vars(self, y,z):
        s = [y,'+',z,'+',z]
        r = eval(''.join(map(str,s)))

        if self.level==1:
            if r/2>12:
                r = 0
        if r in self.vars:
            r = 0

        return s+['=', r]
    
    def three_vars(self, x, y, z):
        s = [x,'+',y,'+',z]
        r = eval(''.join(map(str,s)))
        if r in self.vars:
            r = 0
        return s+['=', r]
    
    def footer_vars(self,x,y,z):
        opps = sample(list(self.ops.keys()),k=2)
        vars = sample([x,y,z],k=3)
        s = [vars[0],opps[0],vars[1],opps[1],vars[2]]
        r = eval(''.join(map(str,s)))

        if self.level==1:
            if r/3>12:
                r = 0
        if r in self.vars:
            r = 0
        
        if not int(r)==r or r<0:
            r=0

        #r= int(r)

        return s+['=', "?"]
    
    def visualize(self):
        item_width = 125
        x_margin, y_margin = (1000-7*item_width)//2, item_width
        
        im = Image.new(mode='RGBA', size=(1000,800), color='white')
        font = ImageFont.truetype(r'arial.ttf', 100)
        font2 = ImageFont.truetype(r'arial.ttf', 20) 
        draw = ImageDraw.Draw(im)
        for i, txt in enumerate(self.array):
            for j, item in enumerate(txt):
                
                if item in self.vars:

                    icon = self.icons[item]
                    im.paste(icon, (x_margin+item_width*j+item_width//2-icon.width//2, y_margin+i*150), mask=icon)
                    continue
                draw.text(xy=(x_margin+item_width*j+item_width//2-font.getlength(str(item))//2, y_margin+i*150), text=str(item).translate({ord('/'): '÷', ord('*'):'×'}), fill='black', font=font)
        
        txt= '— Ahmed shokry : fb.me/ahmed4end — '
        draw.text(xy=(500-font2.getlength(txt)//2, 750), text=txt, fill='lightgrey', font=font2)
        #im.show()
        return im
        


if __name__=='__main__':

    

    for i in range(200):
        puz = puzzle()
        puz.image.save(f'{i}.png')
