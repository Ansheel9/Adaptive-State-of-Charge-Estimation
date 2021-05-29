import math as m
import matplotlib.pyplot as plt
from utils import Polynomial


class Battery:
    def __init__(self, total_Q, R0, R1, C1):
        self.total_Q = total_Q * 3600
        self.actual_Q = self.total_Q
        self.R0 = R0
        self.R1 = R1
        self.C1 = C1
        self.I = 0
        self.Vrc = 0

        # polynomial representation of OCV vs SoC
        self.OCV = Polynomial([3.1400, 3.9905, -14.2391, 24.4140, -13.5688, -4.0621, 4.5056])

    def update(self, time_delta):
        self.actual_Q -= self.current * time_delta
        exp_coeff = m.exp(-time_delta/(self.R1*self.C1))
        self.Vrc *= exp_coeff
        self.Vrc += self.R1*(1-exp_coeff)*self.current
    
    def current(self):
        return self.I

    def current(self, current):
        self.I = current

    def voltage(self):
        return self.OCV - self.R0 * self.current - self.Vrc

    def state_of_charge(self):
        return self.actual_Q/self.total_Q

    def OCV_model(self):
        return self.OCV
    
    def OCV(self):
        return self.OCV_model(self.state_of_charge)


if __name__ == '__main__':
    capacity = 3.2 
    discharge_rate = 1 
    T = 10 
    Vcutoff = 2.5

    current = capacity*discharge_rate
    my_bat = Battery(capacity, 0.062, 0.01, 3000)
    my_bat.current = current
    
    time = [0]
    SoC = [my_bat.state_of_charge]
    OCV = [my_bat.OCV]
    RC_voltage = [my_bat.Vrc]
    voltage = [my_bat.voltage]
    
    while my_bat.voltage > Vcutoff:
        my_bat.update(T)
        time.append(time[-1] + T)
        SoC.append(my_bat.state_of_charge)
        OCV.append(my_bat.OCV)
        RC_voltage.append(my_bat.Vrc)
        voltage.append(my_bat.voltage)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title('')    
    ax1.set_xlabel('SoC')
    ax1.set_ylabel('Voltage')
    ax1.plot(SoC, OCV, label="OCV")
    ax1.plot(SoC, voltage, label="Total voltage")
    plt.show()


