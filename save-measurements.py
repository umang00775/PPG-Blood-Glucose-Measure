import csv
import time
import os
import shutil

def save_measurement_to_csv(pid, device, sys, dia, hr, x):
    filename = '../data/df-ac-measurements.csv'
    if os.stat(filename).st_size == 0:
        # Write header
        with open(filename, 'a') as f:
            writer = csv.writer(f)
            header = ['id', 'date', 'device', 'sys', 'dia', 'hr'] + ['x'+str(i) for i in range(len(x))]
            writer.writerow(header)
    
    if device == 'noir':
        dev = 'Pi NoIR Camera V2'
    else:
        dev = 'iPhone 6s'
    
    timestr = time.strftime("%Y-%m-%d-%H:%M:%S")
    
    fields = [str(pid), timestr, dev, str(sys), str(dia), str(hr)] + [str(elt) for elt in x]
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
