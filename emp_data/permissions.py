    # Maximum Value 7FFFFFFFFFFFFFFF ==> 9223372036854775807
    ## in binary 111111111111111111111111111111111111111111111111111111111111111
PERM_EMPLOYEE_VIEW=0
PERM_EMPLOYEE_ADD=1
PERM_EMPLOYEE_EDIT=2
PERM_EMPLOYEE_DELETE=3

PERM_SALES_VIEW=4
PERM_SALES_ADD=5
PERM_SALES_EDIT=6
PERM_SALES_DELETE=7

PERM_VM_VIEW=8
PERM_VM_ADD=9
PERM_VM_EDIT=10
PERM_VM_DELETE=11

PERM_TA_VIEW=12
PERM_TA_ADD=13
PERM_TA_EDIT=14
PERM_TA_DELETE=15

PERM_CUSTOMER_VIEW=16
PERM_CUSTOMER_ADD=17
PERM_CUSTOMER_EDIT=18
PERM_CUSTOMER_DELETE=19


def checkPermission(user_permission, permission_item):
    if permission_item < 0 or permission_item > 63:
        raise ValueError("Invalid permission item value")
    
    # Create a bitmask by left-shifting 1 by permission_item
    permission_mask = 1 << permission_item
    
    # Check if the corresponding bit is set in user_permission
    has_permission = (user_permission & permission_mask) != 0
    print("Has permission?",has_permission )
    return has_permission

def grantPermission(user_permission, permission_item):
    if permission_item < 0 or permission_item > 63:
        raise ValueError("Invalid permission item value")
    
    # Create a bitmask by left-shifting 1 by permission_item
    permission_mask = 1 << permission_item
    
    # Add the permission by performing a bitwise OR operation
    updated_permission = user_permission | permission_mask
    
    return updated_permission


def revokePermission(user_permission, permission_item):
    if permission_item < 0 or permission_item > 63:
        raise ValueError("Invalid permission item value")
    
    # Create a bitmask by left-shifting 1 by permission_item
    permission_mask = 1 << permission_item
    
    # Remove the permission by performing a bitwise AND operation with the complement of the bitmask
    updated_permission = user_permission & ~permission_mask
    
    return updated_permission

