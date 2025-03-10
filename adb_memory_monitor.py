import subprocess
import time


def bytes_to_mb(kb):
    return round(int(kb.strip()) / 1024, 2)


def monitor_memory(package_name):
    print(f"Monitoring memory usage for {package_name}\n")
    print(f"{'Time':<10} {'Java Heap':>15} {'Native Heap':>15} {'Total PSS':>15}")
    print("=" * 50)

    try:
        while True:
            output = subprocess.check_output(
                f'adb shell dumpsys meminfo {package_name}',
                shell=True, stderr=subprocess.DEVNULL
            ).decode()

            java_heap, native_heap, total_pss = "N/A", "N/A", "N/A"

            for line in output.splitlines():
                if 'Java Heap:' in line:
                    java_heap = bytes_to_mb(line.split()[2])
                elif 'Native Heap:' in line:
                    native_heap = bytes_to_mb(line.split()[2])
                elif 'TOTAL PSS:' in line:
                    total_pss = bytes_to_mb(line.split()[2])

            current_time = time.strftime('%H:%M:%S')
            print(f"[{current_time}] Java: {java_heap} MB | Native: {native_heap} MB | Total: {total_pss} MB")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    monitor_memory("com.instagram.android")
