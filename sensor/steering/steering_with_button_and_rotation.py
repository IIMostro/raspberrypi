from machine import Pin, PWM, ADC
import uasyncio


class Steering:

    def __init__(self):
        self.rotation = ADC(Pin(13))
        self.rotation.atten(ADC.ATTN_11DB)
        self.button = Pin(26, Pin.IN)
        self.switch_value = 0
        self.steer = PWM(Pin(14))
        self.steer.freq(50)

    async def read_button_value(self):
        self.switch_value = self.switch_value ^ self.button.value()

    async def transition_rotation_value_to_steering(self):
        # 正转 [1310 - 4696]
        if self.switch_value == 0:
            return (3386 - ((self.rotation.read() / 4096) * 3386)) + 1310
        # [5057 ~ 8440]
        else:
            return (self.rotation.read() / 4096) * 3386 + 5050

    async def steering_sport(self):
        value = await self.transition_rotation_value_to_steering()
        self.steer.duty_u16(int(value))

    async def start(self):
        while True:
            tasks = [
                self.read_button_value(),
                self.steering_sport()
            ]
            await uasyncio.gather(*tasks)
            await uasyncio.sleep_ms(10)


if __name__ == '__main__':
    event_loop = uasyncio.get_event_loop()
    steering = Steering()
    event_loop.create_task(steering.start())
    event_loop.run_forever()
