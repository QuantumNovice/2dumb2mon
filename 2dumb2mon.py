import telnetlib
import time

import matplotlib.pyplot as plt
import numpy as np
import sys

class DumbNet:
    def connect(self, ip, user, passwd, debug=False):
        """ Verifies telnet login credentials. """
        user += "\r"
        passwd += "\n"
        self.client = telnetlib.Telnet(ip, timeout=1)
        self.client.read_until(bytearray("Login:".encode("utf8")))
        self.client.write(bytearray(user.encode("utf8")))

        self.client.read_until(bytearray("Password:".encode("utf8")))
        self.client.write(bytearray(passwd.encode("utf8")))

    def do_the_deed(self):
        ''' lan show'''

        self.client.write(bytearray("lan show\n".encode("utf8")))

        STDOUT = self.client.read_until(bytearray("br0:0".encode("utf8"))).decode()

        lines = STDOUT.split("\r\n")

        scrub = []
        for line in lines[:]:
            if "RX" not in line and "TX" not in line:
                lines.remove(line)
            else:
                line = line.strip()
                scrub.append(line)

        # print(scrub)

        rx_packets = int(scrub[0].split(" ")[1].split(":")[-1])
        rx_bytes = int(scrub[4].split(" ")[1].split(":")[-1])

        # print(rx_packets, rx_bytes)

        tx_packets = int(scrub[2].split(" ")[1].split(":")[-1])
        tx_bytes = int(scrub[4].split(" ")[5].split(":")[-1])

        # print(tx_packets, tx_bytes)
        #print(rx_packets, tx_packets)

        return rx_bytes, tx_bytes

    def ppp(self,iface='ppp0.1'):
        self.client.write(bytearray(f"ifconfig {iface}\n".encode("utf8")))

        STDOUT = self.client.read_until(bytearray("TX multicast".encode("utf8"))).decode()

        lines = STDOUT.split("\r\n")
        
        scrub = []
        for line in lines[:]:
            if "RX" not in line and "TX" not in line:
                lines.remove(line)
            else:
                line = line.strip()
                scrub.append(line)

        

        rx_bytes = int(scrub[4].split(" ")[1].split(":")[-1])
        tx_bytes = int(scrub[4].split(" ")[5].split(":")[-1])

        return (rx_bytes, tx_bytes)


import matplotlib.pyplot as plt
import matplotlib.animation as animation

t = DumbNet()
t.connect("ip", "user", "")


fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

ax1.set_ylabel('kbps')
ax2.set_ylabel('kbps')


_len = 100
x = np.zeros(_len)
y = np.zeros(_len)

for i in range(_len):
    rx_bytes, tx_bytes = t.ppp('ppp0.1')
    x[i] = rx_bytes
    y[i] = tx_bytes

# x = np.diff(x)
# y = np.diff(y)


def animate(i):
    global x,y
    
    rx_bytes, tx_bytes = t.ppp('ppp0.1')
    
    
    x = np.append(x[1:], rx_bytes)

    
    y = np.append(y[1:], tx_bytes )

    #x = np.diff(x)
    #y = np.diff(y)

    #x = np.diff(x)/1024
    #y = np.diff(y)/1024
    
    #print(x)


    ax1.clear()
    ax2.clear()
    ax1.set_ylabel('kbps')
    ax2.set_ylabel('kbps')
    ax1.plot(x)
    ax2.plot(y)

    


ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()
