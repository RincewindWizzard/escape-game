#!/usr/bin/python3
from struct import pack
from time import sleep, time
import serial, sys, re, readline, random, signal, os, io, subprocess
from subprocess import Popen, PIPE, STDOUT
import serial.tools.list_ports
import colorama
from colorama import Fore, Back, Style
colorama.init()

password = 'janus'

# Einstellungen für die Funksteckdosen
network  = 0b00100 # Hebel 1-5
btn      = 0 # Hebel B


header_logo = r"""
                           __________                   __        __      __   
                           \______   \_______  ____    |__| ____ |  | ___/  |_ 
                            |     ___/\_  __ \/  _ \   |  |/ __ \|  |/ /\   __\
                            |    |     |  | \(  <_> )  |  \  ___/|    <  |  |  
                            |____|     |__|   \____/\__|  |\___  >__|_ \ |__|  
                                                   \______|    \/     \/       
      __________                               __  .__                         
      \______   \_______  ____   _____   _____/  |_|  |__   ____  __ __  ______
       |     ___/\_  __ \/  _ \ /     \_/ __ \   __\  |  \_/ __ \|  |  \/  ___/
       |    |     |  | \(  <_> )  Y Y  \  ___/|  | |   Y  \  ___/|  |  /\___ \ 
       |____|     |__|   \____/|__|_|  /\___  >__| |___|  /\___  >____//____  >
                                     \/     \/          \/     \/           \/ 
"""

ennoia = "TODO: text"
gramma = "TODO: text"

# prints some gibberish to simulate a system boot
def print_gibberish():
  start = time()
  with open(os.path.join(os.path.dirname(__file__), 'gibberish'), 'r') as f:
    lines = f.readlines()
    for line in lines:
      print(line, end='')
      sleep(random.random() / 30)
      if time() - start > 2: break
  

def switch_socket(network, btn, state):
  msg = pack('BBB', network, btn, not state) # TODO: should be state
  for i in range(3):
    if port: port.write(msg)

def set_power(state):
  switch_socket(network, btn, state)

def cls():
  sys.stdout.write("\x1b[2J\x1b[H")

def sendmail(subject, msg):
  try:
    p = Popen(["mail", "-s", subject, "prometheus@magierdinge.de"], stdin=PIPE)
    p.communicate(input=bytes(msg, 'UTF-8'))
  except Exception as e:
    print(e)

def prompt(msg):
  cmd = input(msg).lower()
  if cmd == 'hilfe':
    sendmail('Escape Game', 'Die Gruppe braucht Hilfe.')
    print('Hilfe ist unterwegs.')
  return cmd



def start_prometheus():
  try:
      cls()
      print(Fore.GREEN, end='')

      while not prompt('Bitte Passwort eingeben: ') == password:
        print('Falsches Passwort!')

      print_gibberish()
      cls()
      print(header_logo)
      print('Starte das Kontroll-Programm für Projekt Prometheus')
      sleep(0.5)

      print('Verbinde mit Prometheus Datenbank', end='')
      for i in range(3):
        print('.', end='')
        sys.stdout.flush()
        sleep(1)
      print(" Verbindung hergestellt.")
      while True:
        cmd = prompt('$ ')
        if cmd == 'lumos':
          set_power(True)
        elif cmd == 'nox':
          set_power(False)
        elif cmd == 'odyne':
          print('Lösung gefunden!')
          sendmail('Escape Game', 'Die Gruppe hat die Lösung gefunden!')
        elif cmd == 'gramma':
          print(gramma)
        elif cmd == 'ennoia':
          print(ennoia)
        elif cmd == 'arche':
          set_power(False)
          return
        elif cmd == 'hilfe':
          ...
        else:
          print('Unbekannter Befehl')
  except KeyboardInterrupt:
    ...
  except EOFError:
    ...


if __name__ == '__main__':
  while True:
    # use the first serial port available
    if len(serial.tools.list_ports.comports()) > 0:
      with serial.Serial(serial.tools.list_ports.comports()[0].device, 9600) as port:
        start_prometheus()
    else:
      print('Konnte mich nicht mit der Steuerkonsole verbinden!')
      sleep(1)
      port = None
      start_prometheus()

