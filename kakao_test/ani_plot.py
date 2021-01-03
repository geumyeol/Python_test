import matplotlib.pyplot as plt

plt.ion()
f = open("D:\\develop\\python\\ Python_test\\kakao_test\\testFile.txt", 'rb')

data_size = 10

class DashBoard():
    #Suppose we know the x range
    min_x = 0
    max_x = 10

    MEDIUM_SIZE = 14
    BIGGER_SIZE = 18

    def on_launch(self):
        #Set up plot
        plt.rc('font', size=self.MEDIUM_SIZE, family='Malgun Gothic')   # controls default text sizes
        plt.rc('axes', titlesize=self.MEDIUM_SIZE)                      # fontsize of the axes title
        plt.rc('figure', titlesize=self.BIGGER_SIZE)                    # fontsize of the figure title
        self.figure, self.ax = plt.subplots(2, 1, figsize=(6, 12), facecolor='lightgray')
        #r:red, k:black, b:blue, g:green
        #색상표 : https://matplotlib.org/examples/color/named_colors.html

        #1 데이터 1
        self.lines0, = self.ax[0].plot([], [], '-', color='b')

        self.ax[0].set_ylim(0, 100) # Y축 범위
        self.ax[0].grid()
        self.ax[0].set_xlabel("Time")
        self.ax[0].set_ylabel("Value")
        self.ax[0].set_title('데이터1')

        # 2 데이터 2
        self.lines1, = self.ax[1].plot([], [], '-', color='r' )
        self.ax[1].set_ylim(0, 100)  # Y축 범위
        self.ax[1].grid()
        self.ax[1].set_xlabel("Time")
        self.ax[1].set_ylabel("Value")
        self.ax[1].set_title('데이터2')

    def on_running(self, relayValue, xdata, y0data, y1data):
        relayText = "Switch On" if relayValue == 1 else "Switch Off"
        plt.suptitle('DashBoard : ' + relayText, fontweight='bold', color="blue" if relayValue == 1 else "red")

        self.lines0.set_xdata(xdata)
        self.lines0.set_ydata(y0data)

        self.lines1.set_xdata(xdata)
        self.lines1.set_ydata(y1data)

        self.ax[0].relim()
        self.ax[0].autoscale_view()


        self.ax[1].relim()
        self.ax[1].autoscale_view()

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    # def readSerialPort(self, relayValue, xdata, y0data, y1data):
    #     ser = serial.Serial(port='COM3', baudrate=115200, parity=serial.PARITY_NONE,
    #                         stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    #     if ser.readable():
    #
    #         res = ser.readline()
    #         print(res.decode()[:len(res) - 1])


    def __call__(self):
        import time
        self.on_launch()
        y0data = []
        y1data = []
        xdata=[]
        x = 0

        while True:

            buffer = ""
            while True:
                oneByte = f.read(1)
                if oneByte == b"\r":  # method should returns bytes
                    break
                else:
                    buffer += oneByte.decode()

            res = buffer
            res = res.replace("b","").replace("$","").replace("\\r","").replace("A", "")
            value = res.split(',')

            if len(value) < 3:
                continue

            try :
                value = list(map(float, value))
                #// 시리얼 받아오기 처리하기

                if len(xdata) == data_size -2 :# data_size 이하 처리
                    xdata.pop(0)
                    y0data.pop(0)
                    y1data.pop(0)

                xdata.append(x)
                y0data.append(value[0])
                y1data.append(value[1])
                TotalValue = 0 if value[2]=="" else value[2]

                print("relayValue:",TotalValue)
                print("xdata:", xdata)
                print("y0data:", y0data)
                print("y1data:", y1data)
                self.on_running(TotalValue, xdata, y0data, y1data)
                time.sleep(0.5)
                x += 1
            except:
                print("error:", value)
                pass
        return xdata, y0data, y1data

dashboard = DashBoard()
dashboard()