'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Author: Minh Ho
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt

Apr 10th Revision 1:
    Update FCFS implementation, fixed the bug when there are idle time slices between processes
    Thanks Huang Lung-Chen for pointing out
Revision 2:
    Change requirement for future_prediction SRTF => future_prediction shortest job first(SJF), the simpler non-preemptive version.
    Let initial guess = 5 time units.
    Thanks Lee Wei Ping for trying and pointing out the difficulty & ambiguity with future_prediction SRTF.
'''
import sys

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrive_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time 
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    rem_bt = []
    wt = []
    schedule = []
    current_time = 0
    cross = 0
    sorted(process_list,key=lambda process: process.arrive_time)
    for i in range(len(process_list)):
        rem_bt.append(process_list[i].burst_time)
    while True:
        done = True
        for i in range(len(process_list)):
            if rem_bt[i] > 0 and current_time >= process_list[i].arrive_time:
                done = False
                schedule.append((current_time,process_list[i].id))
                if rem_bt[i] > time_quantum:
                    current_time = current_time + time_quantum
                    rem_bt[i] = rem_bt[i] - time_quantum
                else:
                    current_time = current_time + rem_bt[i]
                    wt.append (current_time - process_list[i].burst_time)
                    rem_bt[i] = 0
                    cross = cross + 1
        if cross == len(process_list):
            break
        if done == True:
            current_time = current_time + 1
    average_waiting_time = sum(wt)/float(len(wt))
    return (schedule, average_waiting_time)

def SRTF_scheduling(process_list):
    current_time = 0
    waiting_time = 0
    schedule = []
    current_list = []
    rem_burst = []
    total = 0
    sorted(process_list,key=lambda process: process.arrive_time)
    for process in process_list:
        rem_burst.append(process.burst_time)
    done = False
    while done == False:
        index = 0
        next_arrival = process_list[0].arrive_time
        for i in range(len(process_list)):
            if process_list[i].arrive_time > current_time:
                next_arrival =  min(next_arrival, process_list[i].arrive_time)
            if rem_burst[index]>= rem_burst[i] and process_list[i].arrive_time <= current_time:
                index = i
        if process_list[i].arrive_time - current_time > rem_burst[index]: 
            rem_burst[index]=0
            total = total + 1
            waiting_time = waiting_time + (current_time - process.arrive_time) + rem_burst[index] - process_list[i].burst_time
        else:
            rem_burst[index]=process[i].arrive_time - current_time
        schedule.append((current_time,process.id))
        current_time = current_time + min(rem_burst[index],next_arrival-current_time)
        if total == len(process_list):
            done = True
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

def SJF_scheduling(process_list, alpha):
    initial_guess = 5
    current_time = 0
    waiting_time = 0
    schedule = []
    current_list = []
    burst_time_prediction = []
    sorted(process_list,key=lambda process:process.arrive_time)
    total = 0
    for i in range(len(process_list)):
        if i == 0:
            burst_time_prediction.append(initial_guess)
        else:
            burst_time_prediction.append(alpha * process_list[i-1].burst_time + (1- alpha) * burst_time_prediction[i-1])
    while True:
        done = True
        index = 0
        for i in range(len(process_list)):
            if burst_time_prediction[index]>= burst_time_prediction[i] and process_list[i].arrive_time <= current_time:
                done = False
                index = i
        if done == False:
            burst_time_prediction[index] = 999999999
            total = total + 1
            schedule.append((current_time,process_list[index].id))
            waiting_time = waiting_time + (current_time - process_list[index].arrive_time)
        
        if total == len(process_list):
            break
        if done == True:
            current_time = current_time + 1
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

       
    return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])
