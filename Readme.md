# Adaptive SoC Estimation for Electric Vehicles :battery: 

<p align="center">
  <img src="https://github.com/Ansheel9/Adaptive-SoC-Estimation/blob/main/imgs/charging.jpg">
</p>

## Team
- Supervisor: Dr.Krishnama Raju
- Member: Abhigyan Chatterjee
- Member: Ansheel Banthia
- Member: Divyanshu Mehta
- Member: M.V.R. Subhash

## Abstract
Living in the automation age and use of electric vehicles are becoming more common with every incoming day the proper utilization and estimation of the state of charge is very much required.

An accurate and fast estimation of state of charge of a battery will improve its efficiency and hence projects a clear picture to the customer when to charge and the most optimal journey will be possible.

We come with this motive to suggest and implement the data driven approach of calculation of the state of charge and use the state-of-the-art machine learning algorithms to find a solution to the problem as the traditional algorithms had a long processing time to evaluate the state of charge and were also computationally heavy.

## Getting Started

### EKF

### Howto
1. Sturcture:
```shell
EKF/
├── main.py
    ├── battery.py
    ├── kalman.py
    ├── protocol.py
    ├── utils.py
```
2. Run `main.py`

---
### CNN-LSTM

### Howto
1. Download `SimulatedSampleDataset` dataset from [here](https://github.com/Ansheel9/Adaptive-SoC-Estimation/tree/main/Code/CNN-LSTM/SimulatedSampleDataset)

2. Sturcture:
```shell
CNN-LSTM/
├── SimulatedSampleDataset
	├── soc01.csv  
	├── soc02.csv 
	...
├── main.py
    ├── SOC.py
    ├── SOC_test.py
    ├── Data.py
└── net_params.pkl
```
3. Modify the `path` to your actual data path

4. Run `main.py`

### Hyperparameters
```
EPOCHES     = 1500
RATE        = 8e-3
HIDDEN_SIZE = 48
Optimizer   = Adam
```

## Result

### EKF

Plot showing the input voltage, SoC & current over time:
![](https://github.com/Ansheel9/Adaptive-SoC-Estimation/blob/main/imgs/ekf.png)

---
### CNN-LSTM

Plot showing the RMSEs of the training and testing performance with varying epoch:
![](https://github.com/Ansheel9/Adaptive-SoC-Estimation/blob/main/imgs/rmse.png)

Plot showing the prediction result vs time & RMSE Loss:
![](https://github.com/Ansheel9/Adaptive-SoC-Estimation/blob/main/imgs/cnn-lstm.png)
