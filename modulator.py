import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.lines as mlines
import random
import string

gcl = 'blue'
cx = 0
cy = 0

def base(num, base):
    converted_string, modstring = "", ""
    currentnum = num
    if not 1 < base < 37:
        raise ValueError("base must be between 2 and 36")
    if not num:
        return '0'
    while currentnum:
        mod = currentnum % base
        currentnum = currentnum // base
        converted_string = chr(48 + mod + 7*(mod > 10)) + converted_string
    return converted_string

def ascii2bin(buf):
    ret =  ''.join(format(ord(x), 'b') for x in buf)
    while(len(ret) % 8) != 0 :
        ret = "0" + ret
    return ret

def randStr(length):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))

def straightLine(a, b):
    return np.array([int(a) for i in range(len(b))])

def verticalLine(y1, y2, x1):
    y = np.linspace(y1, y2)
    x = np.array([x1 for i in range(len(y))])
    plt.plot(x, y, color = gcl)

def horizontalLine(y1, x1, x2):
    x = np.linspace(x1, x2)
    y = np.array([y1 for i in range(len(x))])
    plt.plot(x, y, color=gcl)

def potlEncodeNRZ(data):
    cx = 0
    y = 0
    x = 0
    lastbit = data[0]
    for bit in data:
        x = np.linspace(cx, cx+1)
        y = np.array([int(bit) for i in range(len(x))])
        plt.plot(x, y, color='blue')
        cx += 1
        if (bit!=lastbit and lastbit!= ""):
            y = np.linspace(0,1)
            plt.plot(np.array([cx-1 for i in range(len(y))]), y, color=gcl)
        lastbit = bit

def potlEncode(data, zi):   #zi=true -> NRZI | false -> AMI
    start = True
    cx = 0
    y = 0
    x = 0
    lastbit = data[0]
    pt = 0
    tpt = 0
    lastpt = 0
    for bit in data:
        x = np.linspace(cx, cx+1)
        if (bit == "0" and not zi):
            tpt = pt
            pt = 0
        if (bit == "1"):
            if tpt == 0:
                pt = 1
                tpt = pt
            else:
                pt *= -1
        y = straightLine(pt, x)
        plt.plot(x, y, color=gcl)
        if (bit == "0" and not zi):
            pt = tpt
        cx += 1
        if (not start and zi and pt != lastpt):
            y = np.linspace(lastpt, pt)
            plt.plot(np.array([cx-1 for i in range(len(y))]), y, color=gcl)
            
        if (not zi and not start and bit == "1" and lastbit == "1"):
            y = np.linspace(lastpt, pt)
            plt.plot(np.array([cx-1 for i in range(len(y))]), y, color=gcl)
        if (not zi and not start and bit!=lastbit and lastbit!= ""):
            y = np.linspace(0,1)
            if (pt == -1):
                y = np.linspace(0, -1)
            plt.plot(np.array([cx-1 for i in range(len(y))]), y, color=gcl)
        lastpt = pt
        lastbit = bit
        start = False

def freqEncode(data):
    cx = 0
    for bit in data:
        step = np.pi*10
        time = np.linspace(cx, cx+step);
        if bit == "1":
            amplitude = np.sin(time/5)
        else:
            amplitude = np.sin(time)
        plt.plot(time, amplitude, color=gcl)
        cx += step
        

def amplEncode(data):
    cx = 0
    for bit in data:
        time = np.linspace(cx, cx+2*np.pi);
        amplitude = np.sin(time)
        if (bit == "1"):
            amplitude *= 2
        plt.plot(time, amplitude, color=gcl)
        cx += 2*np.pi

def phaseEncode(data):
    cx = 0
    step = 2*np.pi
    for bit in data:
        time = np.linspace(cx, cx+step);
        if (bit == "0"):
            amplitude = np.sin(step-time)
        else:
            amplitude = np.sin(time)
        plt.plot(time, amplitude, color=gcl)
        cx += step

def bipolarEncode(data):
    cx = 0;
    for bit in data:
        if (bit == "0"):
            verticalLine(0, 0.5, cx)
            horizontalLine(0, cx, cx+0.5)
            verticalLine(0, 0.5, cx+0.5)
            horizontalLine(0.5, cx+1, cx+0.5)
        else:
            verticalLine(0.5, 1, cx)
            horizontalLine(1, cx, cx+0.5)
            verticalLine(0.5, 1, cx+0.5)
            horizontalLine(0.5, cx+1, cx+0.5)
        cx += 1

def manchesterEncode(data):
    cx = 0
    i = 0
    mstep = 1
    lastbit = data[0]
    for bit in data:
        if (i > len(data)-2):
            i -= 2
        if (bit == data[i+1]):
            mstep = 0.5
        else:
            mstep = 1
            
        if (bit == "0"):
            if (bit == lastbit):
                verticalLine(0, 1, cx)
            horizontalLine(1, cx, cx+mstep)
            verticalLine(0, 1, cx+mstep)
            horizontalLine(0, cx+mstep, cx+(mstep*2))
        else:
            if (bit == lastbit):
                verticalLine(0, 1, cx)
            horizontalLine(0, cx, cx+mstep)
            verticalLine(0, 1, cx+mstep)
            horizontalLine(1, cx+mstep, cx+(mstep*2))
        cx += mstep*2
        lastbit = bit
        i += 1

def enc2b1q(data):
    cx = 0
    cy = 0
    block = ""
    lasty = 0
    lastblock = data[0]+data[1]
    for i in range(0, len(data), 2):
        block = data[i]+data[i+1]
        if (block == "00"):
            cy = -2.5
        if (block == "01"):
            cy = -0.833
        if (block == "10"):
            cy = 2.5
        if (block == "11"):
            cy = 0.833
        if (lastblock != block):
            verticalLine(lasty, cy, cx)
        horizontalLine(cy, cx, cx+1)
        lastblock = block
        lasty = cy
        cx += 1
            

sbuf = input("Message to encode: ")
raw = ascii2bin(sbuf)
print(sbuf, ":", len(raw), "bits:", raw)

plt.figure()
plt.suptitle(sbuf)
plt.subplot(2, 1, 1)
plt.title('AMI', fontsize=12)
potlEncode(raw, False)#AMI
plt.subplot(2, 1, 2)
plt.title('NRZ', fontsize=12)
potlEncodeNRZ(raw)#NRZ

plt.figure()
plt.suptitle(sbuf)
plt.subplot(2, 1, 1)
plt.title('NRZI', fontsize=12)
potlEncode(raw, True)#NRZI
plt.subplot(2, 1, 2)
plt.title('Phase Encoding', fontsize=12)
phaseEncode(raw)#Phase

plt.figure()
plt.suptitle(sbuf)
plt.subplot(2, 1, 1)
plt.title('Amplitude Encoding', fontsize=12)
amplEncode(raw)#Amplitude
plt.subplot(2, 1, 2)
plt.title('Frequency Encoding', fontsize=12)
freqEncode(raw)#Frequency

plt.figure()
plt.suptitle(sbuf)
plt.subplot(2, 1, 1)
plt.title('Bipolar Impulse Encoding', fontsize=12)
bipolarEncode(raw)#Bipolar
plt.subplot(2, 1, 2)
plt.title('Manchester Encoding', fontsize=12)
manchesterEncode(raw)#Manchester

plt.figure()
plt.suptitle(sbuf)
plt.title('2B1Q', fontsize=12)
enc2b1q(raw)

plt.show()
