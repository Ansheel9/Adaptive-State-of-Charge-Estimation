from battery import Battery
from kalman import ExtendedKalmanFilter as EKF
from protocol import launch_experiment_protocol
import numpy as np
import math as m
import matplotlib.pyplot as plt


def get_EKF(R0, R1, C1, std_dev, T):
    x = np.matrix([[0.5], [0.0]])
    exp_coeff = m.exp(-T / (C1 * R1))
    # state transition model
    F = np.matrix([[1, 0], [0, exp_coeff]])
    # control-input model
    B = np.matrix([[-T / (Q_tot * 3600)], [ R1 * (1 - exp_coeff)]])
    # variance from std_dev
    var = std_dev ** 2
    # measurement noise
    R = var
    # state covariance
    P = np.matrix([[var, 0], [0, var]])
    # process noise covariance matrix
    Q = np.matrix([[var/50, 0], [0, var/50]])

    def HJacobian(x):
        return np.matrix([[sim_battery.OCV_model.deriv(x[0,0]), -1]])

    def Hx(x):
        return sim_battery.OCV_model(x[0,0]) - x[1,0]

    return EKF(x, F, B, P, Q, R, Hx, HJacobian)


def plot_everything(time, Vtrue, Vmes, true_SoC, est_SoC, current):
    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)
    ax1.set_title('')    
    ax1.set_xlabel('Time / s')
    ax1.set_ylabel('voltage / V')
    ax2.set_xlabel('Time / s')
    ax2.set_ylabel('Soc')
    ax3.set_xlabel('Time / s')
    ax3.set_ylabel('Current / A')
    ax1.plot(time, Vtrue, label="True voltage")
    ax1.plot(time, Vmes, label="Mesured voltage")
    ax2.plot(time, true_SoC, label="True SoC")
    ax2.plot(time, est_SoC, label="Estimated SoC")
    ax3.plot(time, current, label="Current")
    ax1.legend()
    ax2.legend()
    ax3.legend()
    plt.show()


if __name__ == '__main__':
    Q_tot = 3.2
    R0 = 0.062
    R1 = 0.01
    C1 = 3000
    T = 10

    sim_battery = Battery(Q_tot, R0, R1, C1)
    sim_battery.actual_capacity = 0
    std_dev = 0.015
    Kf = get_EKF(R0, R1, C1, std_dev, T)
    time = [0]
    true_SoC = [sim_battery.state_of_charge]
    est_SoC = [Kf.x[0,0]]
    Vtrue = [sim_battery.voltage]
    Vmes = [sim_battery.voltage + np.random.normal(0,0.1,1)[0]]
    current = [sim_battery.current]

    def update_all(Itrue):
        sim_battery.current = Itrue
        sim_battery.update(T)

        time.append(time[-1]+T)
        current.append(Itrue)

        Vtrue.append(sim_battery.voltage)
        Vmes.append(sim_battery.voltage + np.random.normal(0, std_dev, 1)[0])
        
        Kf.predict(u=Itrue)
        Kf.update(Vmes[-1] + R0 * Itrue)
        
        true_SoC.append(sim_battery.state_of_charge)
        est_SoC.append(Kf.x[0,0])
        
        return sim_battery.voltage
    
    launch_experiment_protocol(Q_tot, T, update_all)
    plot_everything(time, Vtrue, Vmes, true_SoC, est_SoC, current)
