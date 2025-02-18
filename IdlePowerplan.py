import time
import powerplan
import win32api
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation

def last_input():
    # returns an int that increases whenever user input is detected
    return win32api.GetLastInputInfo()

def is_audio_playing():
    # returns true if audio amplitude is detected
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioMeterInformation._iid_, 0, None)
        meter = interface.QueryInterface(IAudioMeterInformation)
        return meter.GetPeakValue() > 0.0
    except Exception as e:
        print(f"Error checking audio: {e}")
        return False
        
def power_plan_change(power_plan):
    if power_plan:
        # enable balanced plan
        print(f"input is {power_plan} so enabling balanced")
        powerplan.change_current_scheme_to_balanced()
        return False
    else:
        # enable power saving plan
        print(f"input is {power_plan} so enabling powersaver")
        powerplan.change_current_scheme_to_powersaver()
        return True   
        
def idle_increment(c_input, idle_seconds, check_frequency):
    l_input = last_input()
    print(f"c_input {c_input} - l_input {l_input}")
    # if match then no new user input has been detected
    if c_input == l_input:
        # returns incremented value and new c_input value
        return (idle_seconds + check_frequency), l_input
        print("idle time increase")
    else:
        # idle_seconds is reset to 0 and new c_input is returned
        print("reset idle time from function")
        return 0, l_input
        
def main():
    idle_seconds = 0 # Idle duration in seconds
    is_power_saving = False # true for power saving, true for balance
    idle_target = 120 # How long in seconds before power saving plan is active
    check_frequency = 10 # How often to check if system is idle
    c_input = last_input() # Stores a number that increments with each user interaction
    while True:
        # Function will either return a value incremented by check_frequency or a value
        # of zero, c_input is returned, this value will either remain static or increase
        idle_seconds, c_input = idle_increment(c_input, idle_seconds, check_frequency)
        # Enable power saving plan if all conditions are met
        if idle_seconds >= idle_target and not is_power_saving:
            # To reduce overhead the audio detection function is only called when the 
            # idle_target has been met
            if is_audio_playing():
                # if audio playback is detected, idle counter is reset to 0
                print("audio playing, resetting idle time")
                idle_seconds = 0
            # Power saving plan enabled
            else:
                print("power saving enabled, increasing check frequency")
                is_power_saving = power_plan_change(is_power_saving)
                check_frequency = 1 # Increase check frequency for snappier response
        # if idle_seconds is below target, balanced plan is restored
        elif idle_seconds < idle_target and is_power_saving:
            print("disabling power saving and reducing check frequency")
            is_power_saving = power_plan_change(is_power_saving) 
            check_frequency = 10 # Lower check_frequency = less system overhead
        print(f"System idle for {idle_seconds} seconds {is_power_saving}")
        time.sleep(check_frequency)

if __name__ == "__main__":
    main()