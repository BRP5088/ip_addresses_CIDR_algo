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
    assert num <= 255, f"Shouldn't be bigger than 255. tried converting { num }"

    string = ''
    if type( num ) == str:
        num = int( num )
    remainder = num

    map = {}
    last_used = None

    if num == 0:
        return "0" * 8

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

    return string

def binary_to_decimal( string ):
    total = 0

    string = [ x for x in reversed( string ) ]

    index = 0

    while index < len( string ):

        # print( index )
        if string[ index ] == "1":
            total = total + 2**( index )
        index = index + 1

    return total


class ipAddress:
    def __init__(self, oct1, oct2, oct3, oct4, mask=False, hosts=None ):
        self.oct1 = oct1 if type( oct1 ) == str else decimal_to_binary( oct1 )
        self.oct2 = oct2 if type( oct2 ) == str else decimal_to_binary( oct2 )
        self.oct3 = oct3 if type( oct3 ) == str else decimal_to_binary( oct3 )
        self.oct4 = oct4 if type( oct4 ) == str else decimal_to_binary( oct4 )

        self.CIDR = None
        self.subnetMask = None

        if mask:
            self.CIDR = 32 - ( ceil( log2( hosts ) ) ) 
            self.subnetMask = self.generateSubnetMask()

    def __str__(self):
        return f"{binary_to_decimal( self.oct1 ):03d}.{binary_to_decimal( self.oct2 ):03d}.{binary_to_decimal( self.oct3 ):03d}.{binary_to_decimal( self.oct4 ):03d}"

    def updateCIDR(self, hosts ):
        self.CIDR = 32 - ( ceil( log2( hosts ) ) )

    def generateSubnetMask(self):
        lst = []
        index = self.CIDR

        while index > 0:

            if index - 8 > 0:
                lst.append( decimal_to_binary( 255 ) )
            else:
                tmp = "1" * index + "0" * ( 8 - index )
                lst.append( decimal_to_binary( bitPattern[ tmp ] ) )
            
            index = index - 8

        if len( lst ) < 4:
            lst.append( decimal_to_binary( 0 ) )

        return ipAddress( bitPattern[ lst[0] ], bitPattern[ lst[1] ], bitPattern[ lst[2] ], bitPattern[ lst[3] ] )
    
    def addOneToAddress(self):
        tmp = self.oct1 + self.oct2 + self.oct3 + self.oct4
        answer = ''

        index = 31
        while index >= 0:
            if tmp[ index ] == "0":
                answer = '1' + answer
                break
            else: # found a 1
                answer = '0' + answer
            index -= 1
        
        if len( answer ) < 32:
            answer = tmp[0 : index ] + answer

        return ipAddress( answer[0 : 8], answer[8 : 16], answer[16 : 24], answer[24 : 32] )

    def getBroadcastAddress(self, mask ):

        departmaskBinary = mask.oct1 + mask.oct2 + mask.oct3 + mask.oct4
        departmentSubAddress = self.oct1 + self.oct2 + self.oct3 + self.oct4
        invDepartmask = ""

        for bit in departmaskBinary:
            if bit == "0":
                invDepartmask += "1"
            else:
                invDepartmask += "0"

        answer = ""

        for index in range(0, 32):

            if departmentSubAddress[ index ] == "1" or invDepartmask[ index ] == "1":
                answer += "1"
            else:
                answer += "0"

        return ipAddress( answer[0 : 8], answer[8 : 16], answer[16 : 24], answer[24 : 32] )