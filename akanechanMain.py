import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

# 教本のコードを張り付けたけど、警告がめっちゃ出る
# ラズパイ用に回避するプラグインあるんかね？探そう

# （１）茜ちゃんが朝起こしてくれる（cron起動予定）
# （２）タクトスイッチを押下で停止
# （３）トグルスイッチがオフの状態で停止
# （４）1/1000くらいで朝から抜いてくれるシチュを追加（１０分程度で）

try:
    while True:
        if GPIO.input(24) == GPIO.HIGH:
            GPIO.output(25, GPIO.HIGH)
        else:
            GPIO.output(25, GPIO.LOW)
        sleep(0.01)

except KeyboardInterrupt:
    pass

GPIO.cleanup()