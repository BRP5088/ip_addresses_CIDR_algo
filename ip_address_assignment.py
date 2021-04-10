from IP_Class import *

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