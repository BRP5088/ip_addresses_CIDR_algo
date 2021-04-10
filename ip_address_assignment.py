import sys 
from math import ceil, log2
import IP_Class

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


def generate_table( deptLst, ip_Address):
    deptLst = sorted( deptLst, key=lambda value: value[1], reverse=True )
    lst = [ ] 

    for index, department in enumerate( deptLst ):
        tmp = []

        subnetAddress = None

        if index != 0:
            lastDepartmentBroadcastAddress = lst[ index - 1][5]
            subnetAddress = lastDepartmentBroadcastAddress.addOneToAddress()
        else:
            subnetAddress = ip_Address
        

        tmp.append( department[0] ) # gives the lst the depart ID
        tmp.append( subnetAddress )

        subnetAddress.updateCIDR( department[ 1 ] )
        mask = subnetAddress.generateSubnetMask()

        tmp.append( mask ) # adds the subnet mask to the lst
        tmp.append( subnetAddress.CIDR ) # adds the CIDR value to the lst


        ### address range
        addressRangeStart = subnetAddress.addOneToAddress()

        BroadcastAddress = addressRangeStart.getBroadcastAddress( mask )

        addressRangeEnd = ipAddress( BroadcastAddress.oct1, BroadcastAddress.oct2, BroadcastAddress.oct3, binary_to_decimal( BroadcastAddress.oct4 ) - 1 )

        tmp.append( ( addressRangeStart, addressRangeEnd ) )

        tmp.append( BroadcastAddress )
    
        lst.append( tmp )


    lst = sorted( lst, key=lambda value: value[0] )

    print( "Department  | Subnet Address     | Subnet Mask       | CIDR   | Address Range                      | Broadcast Address" )

    for block in lst:
        for index, info in enumerate( block ):

            if index == 4:
                print( f" { info[0] } to { info[1]} ", end="")
            elif index > 0:
                print( f"    { info }    ", end="" )
            else:
                print( f"    {info } ", end="" )
        print()




def main():
    # deptLst = [ ('A', 500), ('B', 205), ('C', 100), ('D', 80) ]
    # generate_table( deptLst, ipAddress( 156, 31, 28, 0) )

    deptLst = [ ('A', 526), ('B', 275), ('C', 140), ('D', 240), ('E', 100) ]
    generate_table( deptLst, ipAddress( 192, 0, 0, 0) )




if __name__ == "__main__":
    main()