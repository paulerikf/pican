from random import randint
i = 0

def msg():
    global i
    can_id = [
        # Example:  CAN ID - 0x123
        # [0x23, 0x1, 0, 0, 0, 0, 0, 0]
        # AMK Inverter Status
        [0x84, 0x2, 0, 0, 0, 0, 0, 0],  # 0
        [0x85, 0x2, 0, 0, 0, 0, 0, 0],  # 1
        [0x88, 0x2, 0, 0, 0, 0, 0, 0],  # 2
        [0x89, 0x2, 0, 0, 0, 0, 0, 0],  # 3
        # ECU Status
        [0x54, 0x4, 0, 0, 0, 0, 0, 0],  # 4
        # Alive Status
        [0x7f, 0x4, 0, 0, 0, 0, 0, 0],  # 5
    ]
    msgs = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0, 0],
        [0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0, 0],
        [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0, 0],
        [0x9F, 0x7, 0, 0, 0, 0, 0, 0],
        [0xC, 0, 0, 0, 0, 0, 0, 0]
    ]
    m = can_id[i % len(can_id)] + msgs[randint(0, 5)]
    # m = can_id[5] + msgs[4]
    i += 1
    return m
