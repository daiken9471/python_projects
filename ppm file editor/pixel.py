# @author David Aiken 9/6/26
from dataclasses import dataclass, field
from typing import *
import array

@dataclass
class Pixel:
    '''
    Implements a single pixel in RGB color values

    Attributes:
    rgb: array of 3 integers
        Defines each color value

    Methods:
    set_rgb(*args):
        sets the color components of the pixel depending on how many values
        are provided.
    set_to_hex(hex_code):
        sets the color components of the pixel based on the given hex-code.
    set_red(val), set_green(val), set_blue(val):
        sets the given color component to the given value.
    set_to_white(), set_to_black(), set_to_red(), set_to_green(), set_to_blue():
        sets the pixel to the specified color.
    is_close(rhs_pixel, threshold):
        determines if the current pixel's values are within the the given threshold
        of the pixel you send
    '''
    rgb: array 
    RED:Final[int] = 0
    GREEN:Final[int] = 1
    BLUE:Final[int] = 2
    MAX_RGB_VALUE:Final[int] = 255
    MIN_RGB_VALUE:Final[int]  = 0
    TRANSPARENT:Final[list] = (MAX_RGB_VALUE, MAX_RGB_VALUE, MAX_RGB_VALUE)
             
    def __init__(self, *args) -> None:
        """
        sets the value the specified color component. Cam be initialized in 3 ways.
        Args: *args
            if empty, the default is white
            if 3 integers (0-255) are provided, they set RGB in that order
            if a string (hex color code) is provided, the color is set via
            the hex-code
        """
        self.__rgb = array.array("B", [self.MIN_RGB_VALUE, self.MIN_RGB_VALUE, self.MIN_RGB_VALUE])
        match args:
            case r,g,b:
                self.set_rgb(r,g,b)
            case (hex,):
                self.set_to_hex(hex)            
            case _:
                self.set_to_white()

    def __len__(self) -> int:
        return len(self.__rgb)
        
    def __repr__(self) -> str:        
        return f'({self.__rgb[self.RED]}), ({self.__rgb[self.GREEN]}), ({self.__rgb[self.BLUE]})'

    def __str__(self) -> str:
        return f'{self.__rgb[self.RED]} {self.__rgb[self.GREEN]} {self.__rgb[self.BLUE]}'

    def __format__(self, fmt_spec: str = '') -> str:
        if fmt_spec.endswith('H'):
            return dec_to_hex(*self)
        elif fmt_spec.endswith(','):
            return repr(self)
        else:
            return str(self)

    def __hash__(self) -> int:
        return hash(tuple(self.__rgb))
    
    def __getitem__(self, index:int) -> int:
        return self.__rgb[index]   
        
    def __eq__(self, other: object) -> bool:
        return self.__rgb == other
    
    def set_red_val(self, value: int) -> None:        
        self.__rgb[self.RED] = single_value_range_checker(value)

    def set_green_val(self, value: int) -> None:
        self.__rgb[self.GREEN] = single_value_range_checker(value)

    def set_blue_val(self, value: int) -> None:
        self.__rgb[self.BLUE] = single_value_range_checker(value)
        
    def set_rgb(self, *values: tuple) -> None:
        new = len3tuple_value_checker(set_that_t_to_3(values))        
        self.set_red_val(new[self.RED])
        self.set_green_val(new[self.GREEN])
        self.set_blue_val(new[self.BLUE])
        
    def set_to_white(self) -> None:
        self.__rgb[self.RED] = self.MAX_RGB_VALUE
        self.__rgb[self.BLUE] = self.MAX_RGB_VALUE
        self.__rgb[self.GREEN] = self.MAX_RGB_VALUE

    def set_to_black(self) -> None:
        self.__rgb[self.RED] = self.MIN_RGB_VALUE
        self.__rgb[self.BLUE] = self.MIN_RGB_VALUE
        self.__rgb[self.GREEN] = self.MIN_RGB_VALUE

    def set_to_red(self) -> None:
        self.__rgb[self.RED] = self.MAX_RGB_VALUE
        self.__rgb[self.GREEN] = self.MIN_RGB_VALUE
        self.__rgb[self.BLUE] = self.MIN_RGB_VALUE

    def set_to_green(self) -> None:
        self.__rgb[self.RED] = self.MIN_RGB_VALUE
        self.__rgb[self.GREEN] = self.MAX_RGB_VALUE
        self.__rgb[self.BLUE] = self.MIN_RGB_VALUE

    def set_to_blue(self) -> None:
        self.__rgb[self.RED] = self.MIN_RGB_VALUE
        self.__rgb[self.GREEN] = self.MIN_RGB_VALUE
        self.__rgb[self.BLUE] = self.MAX_RGB_VALUE

    def is_close(self, rhs_pixel: tuple, threshold: int) -> bool:
        comprar = zip(self.__rgb, rhs_pixel)
        for a,b in comprar:
            if abs(a - b) > threshold:
                return False
        return True    

    def set_to_hex(self, hex: str) -> None:
        just_the_nums = hex_validator(hex)
        decimal = hex_to_dec(just_the_nums)
        self.__rgb[self.RED] = decimal[self.RED]
        self.__rgb[self.GREEN] = decimal[self.GREEN]
        self.__rgb[self.BLUE] = decimal[self.BLUE]

    def is_transparent(self) -> bool:
    # I feel like the instructions had me comparing an array to a tuple or list
    # which wasn't working for me so I just made them both lists for the check.

    # "Do you think this should be a list or a tuple"
    # Does matter as long as they're both the same if we only returns a boolean?
        return list(self.__rgb) == list(self.TRANSPARENT)

# HELPER FUNCTIONS --------------------------------------

# ensures a value falls within the 0-255 range 
def single_value_range_checker(value: int) -> int:        
    if value < Pixel.MIN_RGB_VALUE:
        value = Pixel.MIN_RGB_VALUE
    if value > Pixel.MAX_RGB_VALUE:
        value = Pixel.MAX_RGB_VALUE
    return value

# makes sure all values in a container are in the 0-255 range
def len3tuple_value_checker(values: tuple) -> tuple:
    newple = tuple(single_value_range_checker(value) for value in values)
    return newple

# makes sure the tuple is length 3
def set_that_t_to_3(values: tuple) -> tuple:
    curtailed_tuple = values[:3]
    difference = 0
    if len(curtailed_tuple) < 3:
        difference = 3 - len(curtailed_tuple)
    embiggened_curtailed_tuple = curtailed_tuple + (0,) * difference
    return embiggened_curtailed_tuple 

# converts a 6-digit hexidecimal code into three 0-255 r,g,b values
def hex_to_dec(hex: str) -> list:
    r = hex[0:2]
    red = r[0] * 16 + r[1]
    g = hex[2:4]
    green = g[0] * 16 + g[1]
    b = hex[4:6]
    blue = b[0] * 16 + b[1]
    return [red, green, blue]

# converts a string into the closest 6-digit hexidecimal code
def hex_validator(hex: str) -> list:
    hex_dict = {"0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8,
                 "9":9, "A":10, "B":11, "C":12, "D":13, "E":14, "F":15}
    curtailed_hex = hex[:6].upper()
    difference = 0
    if len(curtailed_hex) < 6:
        difference = 6 - len(curtailed_hex)
    embiggened_curtailed_hex = curtailed_hex + "0" * difference
    numbers_hex = []
    for char in embiggened_curtailed_hex:
        if char in hex_dict:
            numbers_hex.append(hex_dict[char])
        else: 
            numbers_hex.append(0)
    return numbers_hex

# converts three numbers into the closest 6-digit hexidecimal string.
def dec_to_hex(*args: tuple) -> str:
    hex_dict = {0:"0", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8",
                    9:"9", 10:"A", 11:"B", 12:"C", 13:"D", 14:"E", 15:"F"}
    rgb = args[:3]
    len3tuple_value_checker(rgb)
    hex = ''
    for i in rgb:
        x = i // 16
        y = i % 16
        hex += hex_dict.get(x)      
        hex += hex_dict.get(y)
    return hex