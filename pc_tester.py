import time
import psutil
import platform
import threading
import shutil
import os

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

def cpu_test(duration):
    print("Test Type: Usage test")
    end_time = time.time() + duration
    while time.time() < end_time:
        [x**2 for x in range(1000000)]

def ram_test(duration):
    print("Test Type: Usage test")
    data = []
    end_time = time.time() + duration
    while time.time() < end_time:
        data.append(bytearray(10**6))  # Allocate ~1MB
        time.sleep(0.01)
    del data

def disk_test(duration):
    print("Test Type: Downloading test")
    end_time = time.time() + duration
    with open("temp_test_file.txt", "w") as f:
        while time.time() < end_time:
            f.write("0" * 10**6)  # Write 1MB
            f.flush()
    try:
        os.remove("temp_test_file.txt")
    except:
        pass

def gpu_test(duration):
    if not TORCH_AVAILABLE:
        print("Please install PyTorch for GPU tests, or just do another one.")
        return False
    print("Test Type: Usage test")
    if not torch.cuda.is_available():
        print("No GPU detected for this test.")
        return False
    end_time = time.time() + duration
    while time.time() < end_time:
        a = torch.rand(1000, 1000).cuda()
        b = torch.matmul(a, a)
    return True

def run_tests(part, test_type, count):
    durations = {
        "maximum": 60,
        "normal": 10,
        "percentage": lambda p: max(1, int(60 * (p / 100)))
    }

    for i in range(count):
        print(f"\nRunning test {i + 1}/{count}...")
        if test_type == "maximum":
            duration = durations["maximum"]
        elif test_type == "normal":
            duration = durations["normal"]
        else:
            duration = durations["percentage"](test_type)

        start = time.time()

        if part == "cpu":
            cpu_test(duration)
        elif part == "ram" or part == "memory":
            ram_test(duration)
        elif part == "disk":
            disk_test(duration)
        elif part == "gpu":
            success = gpu_test(duration)
            if not success:
                return

        end = time.time()
        print(f"Test {i + 1} completed in {round(end - start, 2)} seconds.")

    print("\nResults:")
    print(f"Total time: {count * duration} seconds")
    print(f"Completed {count} test(s) on {part.upper()} using {test_type} mode.")

# --- UI Part ---
valid_parts = ["cpu", "gpu", "ram", "memory", "disk"]
print("What type of computer part would you like to test?")
print("Answers: CPU / GPU / RAM or Memory / Disk")
part = input("Type Here: ").lower()

if part not in valid_parts:
    print("Invalid input. Exiting.")
    exit()

test_count = int(input(f'Testing "{part.upper()}", how many tests would you like to run?\n(enters 3)\n'))

print('Choose an answer (TYPE IT IN):')
print("Maximum (Tests maximum power of chosen computer part for 1 minute)")
print("(Any Number)% (Tests the chosen computer part specifically as what you chose)")
print("Normal Test (Does the default test)")
intensity_input = input("(chooses normal)\n").lower()

if "max" in intensity_input:
    test_type = "maximum"
elif "%" in intensity_input:
    try:
        percent = int(intensity_input.strip('%'))
        test_type = percent
    except:
        print("Invalid percentage. Exiting.")
        exit()
else:
    test_type = "normal"

print("\nTesting...")
run_tests(part, test_type, test_count)
