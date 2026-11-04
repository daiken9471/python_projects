# @author David Aiken 9/15/26
from dataclasses import dataclass
from typing import *
from pixel import *
import math
from time import sleep


@dataclass(init=False)
# init = False so it'll quit yelling at me for listing
# image as a "non-default attribue"
class PPM_Image:
    '''
    Creates a canvas of pixels and allows you to change
    the pixels to make an image.

    Attributes:
    width: the width (columns) of the canvas
    height: the height (rows) of the canvas
    image: a 2-d tuple representing a canvas

    Methods:
    save_canvas(file):
        write the image to a .ppm file
    get_pixel(row, col):
        returns the pixel at [row][col]
    draw_rect(row, col, height, width, hex):
        will change the pixels within the height/width range
        starting at [row][col]
    create_color_map(num, threshold):
        builds a color map and saves it to color_map.ppm in the same folder.
    '''
    
    width: int = 2
    height: int = 2
    image: tuple
        
    def __init__(self, type, *args):
        '''
        builds a 2-d tuple of tuples based on the height: rows
        and width: cols entered as parameters. 
        ''' 
        match (type, *args):
            case ('ONE_COLOR', cols, rows, hex_code):
                self.width = cols
                self.height = rows                
                self.image = tuple_matrix(hex_code, self.width, self.height)
            case ('FROM_FILE', filename):
                self.from_file(filename)
            case _:
                try:
                    raise TypeError("We haven't moved beyond ONE_COLOR yet")
                except TypeError as e:
                    print(f"let's keep moving though")

    def save_canvas(self, file: str = "") -> None:
        if not file:
            file = input(f'what would  you like to name this file?: ')            
        with open(f"{file}", "w") as outfile:
            outfile.write(f'P3\n{self.width} {self.height}\n255\n')
            for row in self.image:
                for pixel in row:
                    outfile.write(f'{pixel} ')
                outfile.write('\n')

    def get_pixel(self, row: int, col: int) -> Pixel:
        try:
            return self.image[row][col]
        except:
            return f'uh oh! one of those parameters is outside the range'

    def draw_rect(self, row: int, col: int, height: int, width: int, hex: str) -> None:        
        if row < 0:
            height += row
            row = 0
        if col < 0:
            width += col
            col = 0
        while row + height > self.height:
            height -= 1
        while col + width > self.width:
            width -= 1
        dec = hex_to_dec(hex_validator(hex))    
        for i in range(row, row+height):
            for j in range(col, col+width):
                self.image[i][j].set_rgb(*dec)

    def from_file(self, filename: str) -> None:        
        with open(filename, 'r') as infile:
            line1 = infile.readline()            
            if line1.strip() != 'P3':
                raise ValueError('This file doesn\'t start with "P3"')
            # handle line 2 width/height
            self.width, self.height = [int(i) for i in infile.readline().strip().split()]
            # line 3 for the folks at home
            infile.readline() 
            # I usually forget to initialize stuff but not this time
            self.image = tuple_matrix('000000', self.width, self.height)
            # read the file starting at line 4
            for row in range(self.height):
                line = [int(value) for value in infile.readline().strip().split()]
                for col in range(self.width):
                    self.image[row][col].set_rgb(line[0],line[1],line[2])                    
                    line.pop(0)
                    line.pop(0)
                    line.pop(0)          

    def create_color_map(self, num: int = 10, threshold: int = 20) -> None:
        BLOCK_SIZE = 20
        BLOCKS_PER_ROW = 5
        color_map = {}        
        # count colors and build a dictionary of them
        for row in self.image:
            for pixel in row:
                close_enough = False
                for color in color_map:
                    if pixel.is_close(color, threshold):
                        color_map[color] += 1
                        close_enough = True
                        break
                if not close_enough:
                    color_map[pixel] = 1
        # sort dis dict
        sorted_dict = dict(sorted(color_map.items(), key=lambda item: item[1], reverse = True))
        # slice dis dict
        map_colors = list(sorted_dict.keys())[:num]
        # this next line helps me error check and can be removed later.
        for x in enumerate(map_colors): print(x)
        # initialize a new canvas
        self.width = BLOCK_SIZE * BLOCKS_PER_ROW
        block_rows = math.ceil(len(map_colors) / BLOCKS_PER_ROW)
        self.height = block_rows * BLOCK_SIZE
        self.image = tuple_matrix('000000', self.width, self.height)
        # start draw_rect()-ing
        row = 0
        color = 0 # num_colors index
        for i in range(block_rows):
            col = 0
            for j in range(BLOCKS_PER_ROW):
                # in case there's fewer colors than requested
                if color >= len(map_colors):
                    print("\nThere are less colors in the image than you requested.")
                    print("Your color map has been adjusted accordingly.")
                    break 
                self.draw_rect(row, col, BLOCK_SIZE, BLOCK_SIZE, f'{map_colors[color]:H}')
            # increment everything
                col += BLOCK_SIZE
                color += 1
            row += BLOCK_SIZE        
        # save it
        self.save_canvas("color_map.ppm")
        print(f'\nColor map saved to color_map.ppm\n')

    def __getitem__(self, key: Any) -> Any:
    # when you reference the example in the book, are you talking about
    # the simple one on page 5 the the example on page 408?
    # Also, are the Type Hints corect or should I make them Int since that's what
    # they'll always be checking? or slice?
    # or is it just this simple?
        return self.image[key]

    def overlay_image(self, image: str, start_col: int = 0, start_row: int = 0) -> None:
        # pop out a new image object        
        overlay = PPM_Image('FROM_FILE', image)
        # security checkpoint: dimensions and registration please.
        row_start = abs(start_row) if start_row < 0 else 0
        row_end = min(overlay.height, self.height - start_row)
        col_start = abs(start_col) if start_col < 0 else 0
        col_end = min(overlay.width, self.width- start_col)
        if row_start >= row_end or col_start >= col_end:
            print("\nListen buddy, you're the one who picked this canvas.")
            print("You missed the canvas entirely. Do better.")
            sleep(2)
            print("\nPlease.\n")
            sleep(2)
            return None
        # unpack the canvas as a list for mutability so we can change some memory pointers
        mutable_image = [list(row) for row in self.image]
        for row_index, row in enumerate(overlay.image[row_start:row_end]):
            for col_index, col in enumerate(row[col_start:col_end]):
                # track distance from start col/row thanks to enumerate
                x = max(0, start_col) + col_index
                y = max(0, start_row) + row_index
                if not col.is_transparent():
                    mutable_image[y][x] = col
        # gotta return that tuple integrity before we finish.
        self.image = tuple(tuple(row) for row in mutable_image)
        print("\nImage a has been overlayed.")
        print("Dont forget to save this canvas or add more.\n")

# helper functions -------------------------------------
def tuple_matrix(hex_code: str, cols: int, rows: int) -> PPM_Image:
    return tuple(tuple(Pixel(hex_code) for i in range(cols)) for j in range(rows))