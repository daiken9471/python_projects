# @author David Aiken 9/30/26
from typing import ClassVar


class Menu:
    '''
    builds a generic menu

    When you call Menu please add an "o" to the beginning of each menu option. 
    The options are received by a dictionary and dictionary keys
    must start with a letter.

    Attributes:
    menu: the menu built by __init__

    Methods:

    display_menu():
        returns the function to be called and it parameters based
        on user input
    '''

    STATUS: ClassVar[int] = 0
    DESCRIPTION: ClassVar[int] = 1
    FUNC_CALL: ClassVar[int] = 2
    
    def __init__(self, **kwargs):        
        # uses unpacking to build a dictionary with all the options.
        # please don't forget to add "o" to the beginning of each option.        
        self.__menu = kwargs

    def display_menu(self) -> dict[str, str]:        
        for key, value in self.__menu.items():
            if value[self.STATUS] == True:      
                print(f'{key[1:]}: {value[self.DESCRIPTION]}')
        option = "o" + input(f'Enter Option: ').upper()
        # note to self: think of self.__menu as a 2d list
        # row[option] and col[STATUS/DESCRIPTION/FUNC_CALL]        
        while option not in self.__menu or self.__menu[option][self.STATUS] == False: 
            option = "o" + input(f'\nInvalid Option, Reenter Option: ').upper()
        return self.__menu[option][self.FUNC_CALL:]