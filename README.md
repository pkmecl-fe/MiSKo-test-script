# MiSKo update, configuration and test script
This is an update, configuration and testing script for the MiSKo student development board, written in python3. The main repository for the MiSKo board can be found [here](https://github.com/mjankovec/MiSKo3/tree/main).

The script updates the ST-Link firmware to the newest available one, sets the nSWBOOT0 option bit to 0, and loads a test program into the microcontroller.

# Dependencies
This script requires an installation of python3 (version is not important), java jre (at the time of writing, the confirmed working version is 8 update 421, 16. 7. 2024) and an installation of STM32CubeProgrammer with the STM32_Programmer_CLI executable.

# How to use
For first use, the user should follow all steps in order. Any subsequent use requires only steps 4, 5, and 6.

1. Verify java is installed and configured correctly by opening a terminal or command prompt and running `$ java --version`
2. Open the updateSTlink.py file in a code editor (VScode).
3. Update the values of:
  - JAVA_BIN_G to the java command that works on your PC,
  - If on a Linux OS, STLK_PRG_LIN to the location of the STM32_Programmer_CLI binary (default location /home/{your username}/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI).
  - If on a Linux OS, STLK_FW_UPDATER_LIN to the location of the STLinkUpgrade.jar java binary (default location /home/peter/STMicroelectronics/STM32Cube/STM32CubeProgrammer/Drivers/FirmwareUpgrade/STLinkUpgrade.jar).
  - If on a Windows OS, STLK_PRG_WIN to the location of the STM32_Programmer_CLI.exe binary (default location C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe).
  - If on a Windows OS, STLK_FW_UPDATER_WIN to the location of the STLinkUpgrade.jar java binary (default location C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\Drivers\FirmwareUpgrade\STLinkUpgrade.jar).
4. Plug in the MiSKo in to the PC USB port.
5. Run the script from the project directory `$ python3 updateSTlink.py` or `$ python updateSTlink.py`
6. Wait for script to exit - ensure no errors occured.

