from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d

text = "+10.20A, +034.70, 1".replace("+", "").replace("A","")
value = text.split(',')
value = list(map(float, value))
print (value)

electricValues = []
temperatureValues = []

electricValues.append(value[0])
temperatureValues.append(value[1])
relayValue = value[2]

# example
electricValues.append(9.1)
temperatureValues.append(20.3)
electricValues.append(15.2)
temperatureValues.append(10.9)

plt.rc('font', family='Malgun Gothic')
plt.xlabel("Time")
plt.ylabel("Degree")


plt.subplot(1, 2, 1) # 서브플롯을 나누고 1번 플롯으로 문맥을 전환한다.
plt.plot(electricValues, '--') # green / dot
plt.plot(electricValues, 'go') # green / dot
plt.title('전류')

plt.subplot(1, 2, 2) # 서브플롯을 나누고 1번 플롯으로 문맥을 전환한다.
plt.grid(True)
plt.plot(temperatureValues, '-') # blue / dot
plt.plot(temperatureValues, 'bo') # blue / dot
plt.title('온도')

# plt.plot(x, y, 'go')
relayText = "릴레이 On" if relayValue==1 else "릴레이 Off"
plt.suptitle('Controller DashBoard : ' + relayText)
plt.show()

"""import winreg
import serial
import time

class BluetoothSpp:
    key_bthenum = r"SYSTEM\CurrentControlSet\Enum\BTHENUM"
    # IMPORTANT!!
    # you need to change this by searching the registry
    DEBUG_PORT = 'C00000001'

    def get_spp_com_port(self, bt_mac_addr):
        print(bt_mac_addr)
        bt_mac_addr = bt_mac_addr.replace(':', '').upper()
        for i in self.gen_enum_key('', 'LOCALMFG'):
            print(i)
            for j in self.gen_enum_key(i, bt_mac_addr):
                print(j)
                if self.DEBUG_PORT in j:
                    subkey = self.key_bthenum+'\\'+ i+'\\'+j
                    port = self.get_reg_data(subkey, 'FriendlyName')
                    assert('Standard Serial over Bluetooth link' in port[0])
                    items = port[0].split()
                    port = items[5][1:-1]
                    print(port)
                    return port

    def gen_enum_key(self, subkey, search_str):
        hKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.key_bthenum + '\\' + subkey)

        try:
            i = 0
            while True:
                output = winreg.EnumKey(hKey, i)
                if search_str in output:
                    yield output
                i += 1

        except:
            pass

        winreg.CloseKey(hKey)

    def get_reg_data(self, subkey, name):
        hKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            subkey)
        output = winreg.QueryValueEx(hKey, name)
        winreg.CloseKey(hKey)
        return output

if __name__ == '__main__':
    mac_addr = '11:22:33:44:55:66'
    bt_spp = BluetoothSpp()
    com_port = bt_spp.get_spp_com_port(mac_addr)
"""