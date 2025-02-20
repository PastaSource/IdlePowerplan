import argparse
import time
import powerplan
import win32api
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation

def setup_logger(logging_level):
    # Define logger
    logger = logging.getLogger(__name__)  
    # Set logging level from provided arg
    logger.setLevel(logging_level)
    # Remove previous log
    log_handler = RotatingFileHandler(
        f"{datetime.now().strftime('%Y-%m-%d')} IdlePowerplan.log", backupCount = 5
    )
    # Define format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt = "%H:%M:%S")
    # Set format and handler
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)    
    return logger

def args():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description = "A simple script to change power plans after a pretermined period of user inactivity",
    )
    
    # Define arguments with default values
    parser.add_argument(
        '-c', '--check_frequency',
        type=int,
        default=10,
        metavar='',
        help="How often to check for user activity in seconds (default: %(default)s)"
    )
    parser.add_argument(
        '-i', '--idle_target',
        type=int,
        default=120,
        metavar='',
        help="Idle target time in seconds (default: %(default)s)"
    )
    parser.add_argument(
        '-d', '--debug',
        type=int,
        choices=[0, 1],
        default=0,
        metavar='',
        help="Debug mode: 0 = off, 1 = on (default: %(default)s)"
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Define the arguments
    check_frequency = args.check_frequency
    idle_target = args.idle_target
    logging_level = args.debug
    
    if logging_level == 1:
        logging_level = logging.INFO
    else:
        logging_level = logging.ERROR
    
    return check_frequency, logging_level, idle_target

def last_input(logger):
    # Returns an int that increases whenever user input is detected
    try:
        return win32api.GetLastInputInfo()
    except Exception as e:
        logger.error(f"Error GetLastInputInfo: {e}")

def is_audio_playing(logger):
    # Returns true if audio amplitude is detected
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioMeterInformation._iid_, 0, None)
        meter = interface.QueryInterface(IAudioMeterInformation)
        return meter.GetPeakValue() > 0.0
    except Exception as e:
        logger.error(f"Error checking audio: {e}")
        return False
        
def power_plan_change(logger, power_plan):
    if power_plan:
        # Enable balanced plan
        logger.info(f"input is {power_plan} so enabling balanced")
        try:
            powerplan.change_current_scheme_to_balanced()
        except Exception as e:
            logger.error(f"Error changing powerplan: {e}")
        return False
    else:
        # Enable power saving plan
        logger.info(f"input is {power_plan} so enabling powersaver")
        try:
            powerplan.change_current_scheme_to_powersaver()
        except Exception as e:
            logger.error(f"Error changing powerplan: {e}")
        return True   
        
def idle_increment(logger, c_input, idle_seconds, check_frequency):
    l_input = last_input(logger)
    logger.info(f"c_input {c_input} - l_input {l_input}")
    # If match then no new user input has been detected
    if c_input == l_input:
        # Returns incremented value and new c_input value
        return (idle_seconds + check_frequency), l_input
        logger.info("idle time increase")
    else:
        # idle_seconds is reset to 0 and new c_input is returned
        logger.info("reset idle time from function")
        return 0, l_input
        
def main():
    check_frequency, logging_level, idle_target = args()
    chosen_check_frequency = check_frequency
    logger = setup_logger(logging_level)
    logger.info(f"check_frequency: {check_frequency}, logging_level: {logging_level}, idle_target: {idle_target}")
    idle_seconds = 0 # Idle duration in seconds
    is_power_saving = False # True for power saving, true for balance
    c_input = last_input(logger) # Stores a number that increments with each user interaction
    time.sleep(check_frequency)
    while True:
        # Function will either return a value incremented by check_frequency or a value
        # of zero, c_input is returned, this value will either remain static or increase
        idle_seconds, c_input = idle_increment(logger, c_input, idle_seconds, check_frequency)
        # Enable power saving plan if all conditions are met
        if idle_seconds >= idle_target and not is_power_saving:
            logger.info("idle_seconds greater than idle_target")
            # To reduce overhead the audio detection function is only called when the 
            # idle_target has been met
            if is_audio_playing(logger):
                # If audio playback is detected, idle counter is reset to 0
                logger.info("Audio playing, resetting idle time")
                idle_seconds = 0
            # Power saving plan enabled
            else:
                logger.info("Now audio playing")
                logger.info("power saving enabled, increasing check frequency")
                is_power_saving = power_plan_change(logger, is_power_saving)
                check_frequency = 1 # Increase check frequency for snappier response
        # If idle_seconds is below target, balanced plan is restored
        elif idle_seconds < idle_target and is_power_saving:
            logger.info("disabling power saving and reducing check frequency")
            is_power_saving = power_plan_change(logger, is_power_saving) 
            check_frequency = chosen_check_frequency # Lower check_frequency = less system overhead
        logger.info(f"System idle for {idle_seconds} seconds")
        logger.info(f"Is sytem power saving? {is_power_saving}")
        time.sleep(check_frequency)

if __name__ == "__main__":
    main()
