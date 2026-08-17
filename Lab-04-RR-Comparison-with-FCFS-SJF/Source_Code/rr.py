from collections import deque


def display_results(name, seq, processes, avg_tat, avg_wt, quantum=None):
    print(f"\n{'='*10} {name} {'='*10}")
    if quantum:

        print(f"Time Quantum: {quantum}")
    print("Execution Sequence:", " -> ".join(seq))
    print(f"\n{'PID':<6}{'AT':<6}{'BT':<6}{'CT':<6}{'TAT':<6}{'WT':<6}")
    print("-" * 36)


    for p in sorted(processes, key=lambda x: x["id"]):
        print(f"{p['id']:<6}{p['at']:<6}{p['bt']:<6}{p['ct']:<6}{p['tat']:<6}{p['wt']:<6}")
    print(f"\nAverage Turnaround Time = {avg_tat:.2f}")
    
    print(f"Average Waiting Time    = {avg_wt:.2f}")


def schedule_fcfs(proc_data):
    procs = [p.copy() for p in sorted(proc_data, key=lambda x: x["at"])]
    curr_time = 0
    seq = []


    for p in procs:
        if curr_time < p["at"]:
            curr_time = p["at"]
        curr_time += p["bt"]
        p["ct"] = curr_time
        p["tat"] = p["ct"] - p["at"]
        p["wt"] = p["tat"] - p["bt"]
        seq.append(p["id"])

    n = len(procs)
    avg_tat = sum(p["tat"] for p in procs) / n

    avg_wt = sum(p["wt"] for p in procs) / n
    return seq, procs, avg_tat, avg_wt


def schedule_sjf(proc_data):

    procs = [p.copy() for p in proc_data]
    n = len(procs)
    completed = 0

    curr_time = 0
    seq = []
    is_done = [False] * n

    while completed < n:
        ready = [i for i in range(n) if procs[i]["at"] <= curr_time and not is_done[i]]

        if not ready:
            curr_time += 1
            continue

        idx = min(ready, key=lambda i: procs[i]["bt"])

        curr_time += procs[idx]["bt"]
        procs[idx]["ct"] = curr_time

        procs[idx]["tat"] = procs[idx]["ct"] - procs[idx]["at"]

        procs[idx]["wt"] = procs[idx]["tat"] - procs[idx]["bt"]

        seq.append(procs[idx]["id"])
        is_done[idx] = True
        completed += 1

    avg_tat = sum(p["tat"] for p in procs) / n

    avg_wt = sum(p["wt"] for p in procs) / n
    return seq, procs, avg_tat, avg_wt


def schedule_round_robin(proc_data, q=2):
    procs = [p.copy() for p in sorted(proc_data, key=lambda x: x["at"])]
    n = len(procs)

    rem_bt = [p["bt"] for p in procs]

    curr_time = 0
    completed = 0
    seq = []
    ready_q = deque()
    in_queue = [False] * n

    while completed < n:


        for i in range(n):
            if procs[i]["at"] <= curr_time and not in_queue[i]:
                ready_q.append(i)
                in_queue[i] = True

        if not ready_q:
            curr_time += 1
            continue

        idx = ready_q.popleft()

        seq.append(procs[idx]["id"])
        exec_time = min(rem_bt[idx], q)

        rem_bt[idx] -= exec_time
        curr_time += exec_time

        for i in range(n):
            if procs[i]["at"] <= curr_time and not in_queue[i]:
                ready_q.append(i)
                in_queue[i] = True

        if rem_bt[idx] > 0:
            ready_q.append(idx)
        else:

            procs[idx]["ct"] = curr_time

            procs[idx]["tat"] = procs[idx]["ct"] - procs[idx]["at"]
            procs[idx]["wt"] = procs[idx]["tat"] - procs[idx]["bt"]
            completed += 1

    avg_tat = sum(p["tat"] for p in procs) / n
    avg_wt = sum(p["wt"] for p in procs) / n

    return seq, procs, avg_tat, avg_wt


dataset = [
    {"id": "p1", "at": 0, "bt": 7},
    {"id": "p2", "at": 1, "bt": 4},
    {"id": "p3", "at": 2, "bt": 15},
    {"id": "p4", "at": 3, "bt": 11},
    {"id": "p5", "at": 4, "bt": 20},
    {"id": "p6", "at": 4, "bt": 9},
]

fcfs_res = schedule_fcfs(dataset)
sjf_res = schedule_sjf(dataset)

rr_res = schedule_round_robin(dataset, q=2)

display_results("FCFS", *fcfs_res)
display_results("SJF", *sjf_res)

display_results("Round Robin", *rr_res, quantum=2)

print(f"\n{'='*10} COMPARISON SUMMARY {'='*10}")

print(f"{'Algorithm':<15}{'Avg TAT':<12}{'Avg WT':<12}")
print("-" * 39)

print(f"{'FCFS':<15}{fcfs_res[2]:<12.2f}{fcfs_res[3]:<12.2f}")
print(f"{'SJF':<15}{sjf_res[2]:<12.2f}{sjf_res[3]:<12.2f}")
print(f"{'Round Robin':<15}{rr_res[2]:<12.2f}{rr_res[3]:<12.2f}")
