class Process:
    def __init__(self, process_id, burst_time, arrival_time):
        self.process_id = process_id
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.start_time = 0
        self.end_time = 0

def print_gantt_chart(process, time, reason=""):
    if reason == "Process terminated":
        print(f"{time} {process.process_id} {reason}")
    else:
        print(f"{time} {process.process_id} {reason} - {process.remaining_time} ms remaining")

def round_robin(processes, quantum):
    ready_queue = processes.copy()
    time = 0
    while ready_queue:
        current_process = ready_queue.pop(0)
        current_process.start_time = time

        if current_process.remaining_time <= quantum:
            time += current_process.remaining_time
            current_process.remaining_time = 0
            current_process.end_time = time
            print_gantt_chart(current_process, current_process.start_time, "Process terminated")
        else:
            time += quantum
            current_process.remaining_time -= quantum
            ready_queue.append(current_process)
            print_gantt_chart(current_process,  current_process.start_time, "Quantum expired")

    print(time, " Complete")
    return processes

def shortest_job_first(processes):
    ready_queue = processes.copy()
    ready_queue.sort(key=lambda x: x.burst_time)
    time = 0
    while ready_queue:
        current_process = ready_queue.pop(0)
        current_process.start_time = time
        time += current_process.burst_time
        current_process.end_time = time
        print_gantt_chart(current_process, current_process.start_time, "Process terminated")

    return processes

def shortest_remaining_time_first(processes):
    ready_queue = []
    time = 0
    while processes or ready_queue:
        for process in processes:
            if process.arrival_time <= time:
                ready_queue.append(process)
                processes.remove(process)
        if ready_queue:
            ready_queue.sort(key=lambda x: x.remaining_time)
            current_process = ready_queue.pop(0)
            current_process.start_time = time
            time += 1
            current_process.remaining_time -= 1
            if current_process.remaining_time == 0:
                current_process.end_time = time
                print_gantt_chart(current_process, current_process.start_time, "Process terminated")
            else:
                print_gantt_chart(current_process, current_process.start_time, "Preempted")

    return processes

def statistics(processes):
    total_turnaround_time = 0
    total_waiting_time = 0
    for process in processes:
        turnaround_time = process.end_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        total_turnaround_time += turnaround_time
        total_waiting_time += waiting_time
        print(f"{process.process_id} {turnaround_time} {waiting_time}")

    avg_turnaround_time = total_turnaround_time / len(processes)
    avg_waiting_time = total_waiting_time / len(processes)
    print(f"Average {avg_turnaround_time:.1f} {avg_waiting_time:.1f}")

if __name__ == "__main__":
    processes = []

    with open("input.txt", "r") as file:
        for line in file:
            parts = line.split()
            process_id, burst_time, arrival_time = parts[0], int(parts[1]), int(parts[2])
            processes.append(Process(process_id, burst_time, arrival_time))

    print("Round Robin Scheduling")
    round_robin(processes.copy(), quantum=3)
    statistics(processes)

    print("\nShortest Job First Scheduling")
    shortest_job_first(processes.copy())
    statistics(processes)

    print("\nShortest Remaining Time First Scheduling")
    shortest_remaining_time_first(processes.copy())
    statistics(processes)
