import sys 
from math import ceil, log2

bitPattern = { 
    '00000000': 0,
    '10000000': 128,
    '11000000': 192,
    '11100000': 224,
    '11110000': 240,
    '11111000': 248,
    '11111100': 252,
    '11111110': 254,
    '11111111': 255
}

def decimal_to_binary( num ):
    string = ''
    if type( num ) == str:
        num = int( num )
    remainder = num

    map = {}
    last_used = None

    while remainder >= 0:
        if last_used == -1:
            break

        if last_used == None:
            for num in range( 0, sys.maxsize ):
                map[ num ] = 2**num
                if 2**num > remainder:
                    last_used = num - 1
                    break

        if remainder - map[ last_used ] > -1:
            remainder -= map[ last_used ]
            string += '1'
        else:
            string += '0'

        last_used -= 1

        if len( string ) < 8:
            string = "0" * ( 8 - len( string ) ) + string

        if len( string ) > 8:
            string = string[ ( 8 - len( string ) ) + 1: ]

    return string



class ipAddress:
    def __init__(self, oct1, oct2, oct3, oct4, mask=False, hosts=None ):
        self.oct1 = oct1
        self.oct2 = oct2
        self.oct3 = oct3
        self.oct4 = oct4

        self.mask = None

        self.CIDR = 32 - ( ceil( log2( hosts ) ) ) 

        # if mask:
        #     self.subnetMask = self.generateSubnetMask()

    def __str__(self):
        return f"{ self.oct1 }.{ self.oct2 }.{ self.oct3 }.{ self.oct4 }"

    def generateSubnetMask(self):

        lst = []

        index = self.CIDR

        while index > 0:

            if index - 8 > 0:
                lst.append( 255 )
                index = index - 8
            else:




        return ipAddress( bitPattern[ decimal_to_binary( self.oct1 ) ], bitPattern[ decimal_to_binary( self.oct2 ) ], bitPattern[ decimal_to_binary( self.oct3 ) ], bitPattern[ decimal_to_binary( self.oct4 ) ] ) 





def generate_table( deptLst, ipAddress):
    deptLst = sorted( deptLst )
    
    print( deptLst )



def main():
    deptLst = [ ('A', 500), ('B', 205), ('C', 100), , ('D', 80) ]


    address = ipAddress( 156, 31, 28, 0, True, 500 )

    print( address )
    # print( address.subnetMask )
    generate_table( deptLst, ipAddress( 156, 31, 28, 0) )




if __name__ == "__main__":
    main()