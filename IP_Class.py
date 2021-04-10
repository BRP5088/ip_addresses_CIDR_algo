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