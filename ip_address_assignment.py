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



class ipAddress:
    def __init__(self, oct1, oct2, oct3, oct4, mask=False ):
        self.oct1 = oct1
        self.oct1 = oct2
        self.oct1 = oct3
        self.oct4 = oct4

        self.mask = None

        if mask:
            self.subnetMask = self.generateSubnetMask()

    def __str__(self):
        print( f"{ self.oct1 }.{ self.oct2 }.{ self.oct3 }.{ self.oct4 }")

    def generateSubnetMask(self):
        return 'sd'





def generate_table( deptLst, ipAddress):



def main():
    deptLst = [ ('A', 500), ('B', 205), ('C', 100), ('D', 80) ]


    address = ipAddress( 156, 31, 28, 0) )

    print( address )
    # generate_table( deptLst, ipAddress( 156, 31, 28, 0) )




if __name__ == "__main__":
    main()