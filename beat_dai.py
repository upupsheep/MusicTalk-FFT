import time, DAN, requests, random
import os, sys
import threading
import DAN
# from pydub import AudioSegment
# from pydub.playback import play
import pygame as pg
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
beat_strength = []
fp = open('night.txt', 'r')
for line in fp:
    line_action = line.strip().split(',')
    freq_list.append(line_action[2])
    action_list.append(line_action[0])
    beat_strength.append(float(line_action[3]))
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
        change = int(freq_list[now]) / 100
        change = int(change)
        # change = change+1
        # change = change % 8
        push_data = [0, 0, 0, 0, 0, 0, 0]
        if (change == 0):
            push_data = [0, 0, 0, 0, 0, 0, 1]
        elif (change == 1):
            push_data = [0, 0, 0, 0, 0, 1, 1]
        elif (change == 2):
            push_data = [0, 0, 0, 0, 1, 1, 1]
        elif (change == 3):
            push_data = [0, 0, 0, 1, 1, 1, 1]
        elif (change == 4):
            push_data = [0, 0, 1, 1, 1, 1, 1]
        elif (change == 5):
            push_data = [0, 1, 1, 1, 1, 1, 1]
        elif (change >= 6):
            push_data = [1, 1, 1, 1, 1, 1, 1]
        else:
            push_data = [0, 0, 0, 0, 0, 0, 0]
        # sequence += 1
        print(change, freq_list[now])
        #color_list = []
        if (beat_strength[sequence] > 6):
            print(beat_strength[sequence])
            if (sequence == len(action_list)):
                DAN.push('music_ctl_i', 0, 0, 0, 0, 0, 0, 0)
            else:
                DAN.push('music_ctl_i', push_data[0], push_data[1],
                         push_data[2], push_data[3], push_data[4],
                         push_data[5], push_data[6])
        last = now
        now = now + 1
        sequence += 1
        time.sleep(float(action_list[now]) - float(action_list[last]))

    # end
    DAN.push('music_ctl_i', 0, 0, 0, 0, 0, 0, 0)


def play(music_file):
    # pick a midi or MP3 music file you have in the working folder
    # or give full pathname
    #music_file = "Drumtrack.mp3"
    '''
    freq = 44100  # audio CD quality
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 2048  # number of samples (experiment to get right sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    '''
    pg.mixer.init()

    # optional volume 0 to 1.0
    pg.mixer.music.set_volume(0.8)

    # play music
    print("Playing...")
    clock = pg.time.Clock()
    pg.mixer.music.load(music_file)
    pg.mixer.music.play()
    # check if playback has finished
    while pg.mixer.music.get_busy():
        clock.tick(30)


def job_of_play_music(music_file):
    """ create a thread to play music """

    def call():
        play(music_file)

    p = threading.Thread(target=call)
    p.setDaemon(True)
    p.start()


if __name__ == '__main__':
    while (DAN.state != 'SET_DF_STATUS'):
        time.sleep(0.1)
    job_of_play_music('night.wav')
    job_of_send_info()
    DAN.push('music_ctl_i', 0, 0, 0)
