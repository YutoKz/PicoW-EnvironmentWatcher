from machine import Pin, UART, I2C
import ssd1306
import utime
import math

i2c = I2C(0, sda=Pin(0), scl=Pin(1))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

def init_oled():
    display.fill(0)

def show_oled(temp, co2):
    """
    display.fill(0)
    display.text(f"{temp:.1f}", 15, 0, 1)
    display.text('degree',      64, 0, 1)
    display.text(f"{co2}",      15, 10, 1)
    display.text('ppm',         64, 10, 1)
    display.show()
    """
    # 上消す
    display.fill_rect(0, 0, 127, 25, 0)
    # 左にスクロール
    display.scroll(-1, 0)
    # 新しい点打つ
    display.line(127, 0, 127, 63, 0)
    """
    if temp <= 14:
        display.pixel(127, 63, 1)
    elif temp >= 30:
        display.pixel(127, 23, 1)
    else:
        display.pixel(127, 63-int((temp-14)/0.4), 1)
    """
    if co2 <= 400:
        display.pixel(127, 63, 1)
    if co2 >= 2000:
        display.pixel(127, 23, 1)
    else:
        display.pixel(127, 63-int((co2-400)/40), 1)
    # 数字描画
    display.text(f"{temp:.1f}", 15, 0, 1)
    display.text('degree',      64, 0, 1)
    display.text(f"{co2}",      15, 10, 1)
    display.text('ppm',         64, 10, 1)
    display.show()
