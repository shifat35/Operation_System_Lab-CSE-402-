

def fcfs_scheduling(processes):
   
    
    processes = sorted(processes, key=lambda x: x[1])

    result = []
    current_time = 0
    gantt_chart = []

    for pid, at, bt in processes:
       
        start_time = max(current_time, at)
        completion_time = start_time + bt

        tat = completion_time - at      
        wt = tat - bt                   

        result.append({
            "P id": pid,
            "AT": at,
            "BT": bt,
            "CT": completion_time,
            "TAT": tat,
            "WT": wt
        })

        gantt_chart.append((pid, start_time, completion_time))
        current_time = completion_time

    return result, gantt_chart


def print_table(result):
    print(f"{'P id':<6}{'AT':<5}{'BT':<5}{'CT':<5}{'TAT':<5}{'WT':<5}")
    print("-" * 31)
    for r in result:
        print(f"{r['P id']:<6}{r['AT']:<5}{r['BT']:<5}{r['CT']:<5}{r['TAT']:<5}{r['WT']:<5}")


def print_gantt_chart(gantt_chart):
    top = "|"
    bottom = ""
    for pid, start, end in gantt_chart:
        top += f" {pid} |"
    print("\nGantt Chart:")
    print(top)

    # print timeline numbers
    line = f"{gantt_chart[0][1]}"
    for pid, start, end in gantt_chart:
        line += f"{'':>6}{end}"
    print(line)


def main():
   
    processes = [
        ("P0", 3, 1),
        ("P1", 5, 3),
        ("P2", 2, 2),
        ("P3", 1, 2),
        ("P4", 6, 3),
    ]

    result, gantt_chart = fcfs_scheduling(processes)

    print("FCFS CPU Scheduling Result (sorted by Arrival Time)\n")
    print_table(result)
    print_gantt_chart(gantt_chart)

    total_tat = sum(r["TAT"] for r in result)
    total_wt = sum(r["WT"] for r in result)
    n = len(result)

    avg_tat = total_tat / n
    avg_wt = total_wt / n

    print(f"\nAverage Turnaround Time (TAT) = {avg_tat:.2f}")
    print(f"Average Waiting Time (WT)     = {avg_wt:.2f}")


if __name__ == "__main__":
    main()