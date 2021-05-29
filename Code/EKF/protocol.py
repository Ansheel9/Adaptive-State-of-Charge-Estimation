def launch_experiment_protocol(Q_tot, time_step, experiment_callback):

    C_rate = 0.5
    disC_rate = 1
    disC_stages_time = 20*60
    PT = 60
    total_PT = 40*60
    Vcutoff_high = 4.2
    Vcutoff_low = 2.5

    current = -C_rate * Q_tot
    voltage = 0
    while voltage < Vcutoff_high:
        voltage = experiment_callback(current)

    while current < -0.1:
        if voltage > Vcutoff_high*1.001:
            current += 0.01 * Q_tot
        voltage = experiment_callback(current)

    time = 0
    current = disC_rate * Q_tot
    while time < disC_stages_time:
        experiment_callback(current)
        time += time_step

    time = 0
    while time < total_PT:
        time_low = 0
        current = 0
        while time_low < PT:
            experiment_callback(current)
            time_low += time_step
        time_high = 0
        current = disC_rate * Q_tot
        while time_high < PT:
            experiment_callback(current)
            time_high += time_step
        time += time_low + time_high

    time = 0
    current = disC_rate * Q_tot
    while time < disC_stages_time:
        experiment_callback(current)
        time += time_step
