import time, DAN, requests, random
import os, sys
import threading
import DAN
from pydub import AudioSegment
from pydub.playback import play
import csv

ServerURL = 'http://garden.iottalk.tw'  #with no secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = None  #if None, Reg_addr = MAC address

DAN.profile['dm_name'] = 'music_ctl'
DAN.profile['df_list'] = ['music_ctl_i']
DAN.profile['d_name'] = None  # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)

action_list = []
freq_list = []
fp = open('night.txt', 'r')
for line in fp:
    line_action = line.strip().split(',')
    freq_list.append(line_action[2])
    action_list.append(line_action[0])
# end of parsing
fp.close()
'''
f = open('beat_times.csv', 'r')
for row in csv.reader(f):
    #print(row[0])
    action_list.append(row[0])
f.close()
'''
sequence = 0
send_signal = 0
change = 0
now = 0
last = 0


def job_of_send_info():
    global sequence, action_list, send_signal, change, now, last, freq_list
    while (sequence < len(action_list)):

        #Pull data from a device feature called "Dummy_Control"
        #value1=DAN.pull('Dummy_Control')
        #if value1 != None:
        #   send_signal = 1
        #print (value1[0])

        #Push data to a device feature called "Dummy_Sensor"
        # job_of_play_music()

        #change = action_list[sequence]
        #change = int(change[0])
        change = int(freq_list[now]) / 200
        change = int(change)
        # change = change+1
        # change = change % 8
        if (change == 0):
            color1 = 0
            color2 = 0
            color3 = 255
        elif (change == 1):
            color1 = 135
            color2 = 255
            color3 = 255
        elif (change == 2):
            color1 = 0
            color2 = 255
            color3 = 0
        elif (change == 3):
            color1 = 255
            color2 = 255
            color3 = 0
        elif (change == 4):
            color1 = 255
            color2 = 102
            color3 = 0
        elif (change == 5):
            color1 = 255
            color2 = 0
            color3 = 0
        elif (change == 6):
            color1 = 255
            color2 = 0
            color3 = 255
        else:
            color1 = 153
            color2 = 0
            color3 = 255
        sequence += 1
        print(change, freq_list[now])
        #color_list = []
        if (sequence + 1 == len(action_list)):
            DAN.push('music_ctl_i', 0, 0, 0)
        else:
            DAN.push('music_ctl_i', color1, color2, color3)
        last = now
        now = now + 1
        time.sleep(float(action_list[now]) - float(action_list[last]))

    # end
    DAN.push('music_ctl_i', 0, 0, 0)


def job_of_play_music():
    global send_signal

    def call():
        print('play', 'song')
        song = AudioSegment.from_wav("night.wav")
        play(song)

    #time.sleep(0.1)
    p = threading.Thread(target=call)
    p.setDaemon(True)
    p.start()


if __name__ == '__main__':
    while (DAN.state != 'SET_DF_STATUS'):
        time.sleep(0.1)
    job_of_play_music()
    job_of_send_info()
    DAN.push('music_ctl_i', 0, 0, 0)
