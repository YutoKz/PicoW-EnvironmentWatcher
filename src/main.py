import machine
import utime
from umqtt.simple import MQTTClient
from wifi import connect
from read import read_temperature, read_co2_level, read_mhz19c
from send import send_line_notification, send_mqtt_data
from oled import init_oled, show_oled

def main():
    # wifi 接続
    ip = connect()
    print(f'Connected on {ip}')
    
    temperature_tmp = 0
    co2_level_tmp = 0
    riskflag_temp = False
    riskflag_co2 = False
    
    init_oled()
    
    while True:
        # 計測
        #temperature = read_temperature()
        #co2_level = read_co2_level()
        temperature, co2_level = read_mhz19c()
        
        show_oled(temperature, co2_level)
        
        if co2_level > 5000:
            utime.sleep(10)
            continue

        # 危険域ならLINE通知
        if temperature > 30 and temperature_tmp <= 30:
            message = f"\nToo Hot: {temperature:.1f} °C\nRisk: Heat Stroke, Dehydration"
            send_line_notification(message)
            riskflag_temp = True
        if temperature < 10 and temperature_tmp >= 10:
            message = f"\n寒すぎ。: {temperature:.1f} °C\nRisk: Cold, Flu"
            send_line_notification(message)
            riskflag_temp = True
        if co2_level > 2000 and co2_level_tmp <= 2000:
            message = f"\nVentilate!: {co2_level} ppm (CO2)\nRisk: Headache, Inattention"
            send_line_notification(message)
            riskflag_co2 = True
        elif co2_level > 1000 and co2_level_tmp <= 1000:
            message = f"\nVentilate!: {co2_level} ppm (CO2)\nRisk: Discomfort, Drowsiness"
            send_line_notification(message)
            riskflag_co2 = True
        #危険域から脱したらLINE通知
        if 18 <= temperature <= 25 and riskflag_temp == True:
            message = f"\nModerate Temperature (18 ~ 25 °C)."
            send_line_notification(message)
            riskflag_temp = False
        if co2_level <= 1000 and riskflag_co2 == True:
            message = f"\nWell Ventilated (~ 1000ppm)."
            send_line_notification(message)
            riskflag_co2 = False
        

        # MQTTでデータ送信
        send_mqtt_data(temperature, co2_level)

        temperature_tmp = temperature
        co2_level_tmp = co2_level
        
        utime.sleep(10)

if __name__ == "__main__":
    main()

