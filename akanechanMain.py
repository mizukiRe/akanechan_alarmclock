import RPi.GPIO as GPIO
import pygame.mixer
from time import sleep
import subprocess
import os, sys
import random
import datetime


GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

# 教本のコードを張り付けたけど、警告がめっちゃ出る
# ラズパイ用に回避するプラグインあるんかね？探そう

# （１）茜ちゃんが朝起こしてくれる（cron起動予定）
# （２）タクトスイッチを押下で停止
# （３）スライドスイッチがオフの状態で停止
# （４）1/1000くらいで朝からえっちなことしてくれるシチュを追加（１０分程度で）

# 引数のディレクトリにある音声ファイルをランダムで選んでフルパスを返す
def getRandomVoiceFullFilepass(music_pass):
    # ファイル名を取得
    files = os.listdir(music_pass)
    print("ファイル数:",str(len(files)))
    for file in files:
        print("\t",file)
        
    # 乱数で選曲
    r = random
    r.seed()
    play_no = r.randint(0, len(files)-1)
    print(play_no,"曲目を再生")
    file = files[play_no]

    fullpass = music_pass + file
    return fullpass

MP3_PATH = '/home/pi/Music/akanechan/akanechan_ohayou_01.mp3'

start_time = datetime.datetime.now()
# whileの条件でエラーなるのでとりあえずtrueになるように変数にセット
dt = datetime.datetime.now()

now = datetime.datetime.now()

# 開始時刻＋１hまではスライドスイッチをオフを受け付ける
# cronは実際の目覚ましの時間-1hを設定する想定
while(start_time + datetime.timedelta(hours=1) > dt):

    # ローカルな現在の日付と時刻を取得
    dt = datetime.datetime.now()
    # 現在の時間を保存
    t = dt.time()
    print(t)  # 15:58:08.356501
    
    print("茜ちゃんが褒めてくれる")

    try:
        if GPIO.input(24) == GPIO.HIGH:
            GPIO.output(25, GPIO.HIGH)
            print("akanechan")
            sleep(10)
            
        else:
            # スライドスイッチがOFFになったときの挙動
            music_pass = "/home/pi/Music/akanechan/amaamahome/"
            GPIO.output(25, GPIO.LOW)
            
            fullpass = getRandomVoiceFullFilepass(music_pass)

            args = ['omxplayer', '-o', 'alsa', fullpass]

            process = subprocess.Popen(args)
            sleep(60)
            GPIO.cleanup()
            exit()

    except KeyboardInterrupt:
        pass

# あとでプログラム自体を分ける
if ( t > datetime.time(13,00,00) and t < datetime.time(14,00,00)):
    music_pass = "/home/pi/Music/akanechan/ohiru/"
    print("false")
else:
    print("true")
    music_pass = "/home/pi/Music/akanechan/ohayou/"

fullpass = getRandomVoiceFullFilepass(music_pass)
args = ['omxplayer', '-o', 'alsa', fullpass]

process = subprocess.Popen(args)
sleep(5)

try:
    if GPIO.input(24) == GPIO.HIGH:
        GPIO.output(25, GPIO.HIGH)
    else:
        GPIO.output(25, GPIO.LOW)
    sleep(0.01)

except KeyboardInterrupt:
    pass

GPIO.cleanup()


