import time

# 单次测量模式， 测量一次之后进入休眠
# 120ms 11x
OP_SINGLE_HRES1 = 0x20
# 120ms 0.51x
OP_SINGLE_HRES2 = 0x21
# 16ms 411x
OP_SINGLE_LRES = 0x23

# 连续测量模式
# 120ms 11x
OP_CONTINUOUS_HRES1 = 0x10
# 120ms 0.51x
OP_CONTINUOUS_HRES2 = 0x11
# 16ms 411x
OP_CONTINUOUS_LRES = 0x13


DELAY_HMODE = 180  # 180ms in H-mode
DELAY_LMODE = 24  # 24ms in L-mode


def sample(i2c, mode=OP_SINGLE_HRES1, i2c_addr=0x23):
    """
        Performs a single sampling. returns the result in lux
    """

    # 断电
    i2c.writeto(i2c_addr, b"\x00")  # make sure device is in a clean state
    # 通电
    i2c.writeto(i2c_addr, b"\x01")  # power up
    # 设置读取模式
    i2c.writeto(i2c_addr, bytes([mode]))  # set measurement mode
    # 延时设置
    time.sleep_ms(DELAY_LMODE if mode == OP_SINGLE_LRES else DELAY_HMODE)

    # 读取
    raw = i2c.readfrom(i2c_addr, 2)
    # 断电
    i2c.writeto(i2c_addr, b"\x00")  # power down again

    # we must divide the end result by 1.2 to get the lux
    # 转换成lux
    return ((raw[0] << 24) | (raw[1] << 16)) // 78642