import subprocess
import platform
import os
import re

JAVA_BIN_G          = "java"
STLK_PRG_LIN        = "/home/peter/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI"
STLK_PRG_WIN        = r"C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe"
STLK_FW_UPDATER_WIN = r"C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\Drivers\FirmwareUpgrade\STLinkUpgrade.jar"
STLK_FW_UPDATER_LIN = "/home/peter/STMicroelectronics/STM32Cube/STM32CubeProgrammer/Drivers/FirmwareUpgrade/STLinkUpgrade.jar"

TEST_PROGRAM = "Test.elf"

def update_stlink_firmware():
    try:
        # Detect the platform
        system = platform.system()

        if system == "Windows":
            # Windows path for STM32CubeProgrammer or ST-Link Utility
            stlink_programmer = STLK_FW_UPDATER_WIN
            java_bin = JAVA_BIN_G
        elif system == "Linux":
            # Linux path for STM32CubeProgrammer
            stlink_programmer = STLK_FW_UPDATER_LIN
            java_bin = JAVA_BIN_G
        else:
            raise Exception("Unsupported OS: Only Windows and Linux are supported")

        # Step 1: Update ST-Link Firmware (assuming the tool will auto-update)
        update_command = [java_bin, "-jar", stlink_programmer, "-msvcp"]
        print(f"Updating ST-Link firmware using: {update_command}")
        result = subprocess.run(update_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            print(f"Error updating firmware: {result.stderr}")
            return False
        print(f"Firmware updated successfully: {result.stdout}")

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def set_option_bits_nSWBOOT0():
    try:
        # Detect the platform
        system = platform.system()

        if system == "Windows":
            # Windows path for STM32CubeProgrammer
            stlink_programmer = STLK_PRG_WIN
        elif system == "Linux":
            # Linux path for STM32CubeProgrammer
            stlink_programmer = STLK_PRG_LIN
        else:
            raise Exception("Unsupported OS: Only Windows and Linux are supported")
        
        scan_command = [stlink_programmer, "-l"]
        print(f"Scanning for available ST-Link devices using: {scan_command}")
        result = subprocess.run(scan_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"Error scanning for ST-Link devices: {result.stderr}")
            return None

        # Parse the output to find the first available device
        output = result.stdout
        #print(f"Scan result:\n{output}")

        # Use regular expressions to extract the serial numbers (assuming they follow the format "SN : <serial_number>")
        matches = re.findall(r"SN\s*:\s*(\S+)", output)

        if not matches:
            print("No ST-Link devices found.")
            return None

        # Step 2: Connect to the first available device (get the first serial number)
        first_serial = matches[0]
        print(f"Found ST-Link device with serial number: {first_serial}")

        # Step 3: Connect to the ST-Link device using its serial number
        connect_command = [stlink_programmer, "-c", f"port=SWD", f"sn={first_serial}", "-ob", "nSWBOOT0=0"]
        print(f"Connecting to ST-Link device with command: {connect_command}")
        result = subprocess.run(connect_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"Error connecting to ST-Link device: {result.stderr}")
            return None

        print(f"Connected successfully:\n{result.stdout}")
        return first_serial

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    

def load_test_program():
    try:
        # Detect the platform
        system = platform.system()

        if system == "Windows":
            # Windows path for STM32CubeProgrammer
            stlink_programmer = STLK_PRG_WIN
        elif system == "Linux":
            # Linux path for STM32CubeProgrammer
            stlink_programmer = STLK_PRG_LIN
        else:
            raise Exception("Unsupported OS: Only Windows and Linux are supported")
        
        scan_command = [stlink_programmer, "-l"]
        print(f"Scanning for available ST-Link devices using: {scan_command}")
        result = subprocess.run(scan_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"Error scanning for ST-Link devices: {result.stderr}")
            return None

        # Parse the output to find the first available device
        output = result.stdout
        #print(f"Scan result:\n{output}")

        # Use regular expressions to extract the serial numbers (assuming they follow the format "SN : <serial_number>")
        matches = re.findall(r"SN\s*:\s*(\S+)", output)

        if not matches:
            print("No ST-Link devices found.")
            return None

        # Step 2: Connect to the first available device (get the first serial number)
        first_serial = matches[0]
        print(f"Found ST-Link device with serial number: {first_serial}")

        # Step 3: Connect to the ST-Link device using its serial number
        connect_command = [stlink_programmer, "-c", f"port=SWD", f"sn={first_serial}", "-d", TEST_PROGRAM, "-rst"]
        print(f"Connecting to ST-Link device with command: {connect_command}")
        result = subprocess.run(connect_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"Error connecting to ST-Link device: {result.stderr}")
            return None

        print(f"Connected successfully:\n{result.stdout}")
        return first_serial

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Main function to update firmware and change option bits
def main():
    if update_stlink_firmware():
        print("ST-Link firmware updated successfully.")
    else:
        print("Failed to update ST-Link firmware.")
        return

    if set_option_bits_nSWBOOT0():
        print("nSWBOOT0 option bit set successfully.")
    else:
        print("Failed to set nSWBOOT0 option bit.")

    if load_test_program():
        print("Test program loaded successfully.")
    else:
        print("Failed to load test program.")

if __name__ == "__main__":
    main()
