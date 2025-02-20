
# IdlePowerplan
A lightweight Python script to change the power plan in Windows after a predetermined period of user inactivity.

---

This Python script is able to detect both user input, and whether or not any audio is playing on the system, and will change the Windows power plan from balanced to power saving once there has been a predetermined period of user inactivity and no audio currently playing. This combination ensures the script will not enable idle mode if user input is detected, and using anything that has an audio output e.g. watching a video, playing a game, etc. 
# Requirements
Windows (tested on 10 22H2)
Python 3 (tested with 3.12)
Python modules:
 - Powerplan
 - pywin32
 - pycaw

>  pip install powerplan pywin32 pycaw


# Usage
 - Check frequency | -c, --check_frequency | default: 10 seconds
User input is detected by using win32api.GetLastInputInfo(), this obtains info from a native Windows function where the value is incremented when any kind of user input is detected. The check frequency only adjusts how often this fuction is queried, increasing or decreasing this value will **not** improve accuracy, but instead it will improve the accuracy of the system going idle at the desired idle target at the expense of increased system overhead.
 - Idle target | -i, --idle_target | default: 120 seconds
 How long until the script decides the system is idle before changing to the power plan.
 - Debug mode | -d, --debug | default: 0 (off)
 By default this value is set to only capture errors, if you're having issues please set this to 1 before submitting an issue.
 - Windows power plan customisation
 Within Windows for maximum efficiency I suggest that you edit your power saving power plan profile. Customise as desired. In "processor power management"  set "maximum processor state" to a percentage of your choosing. This will be a percentage of your processors maximum stock clock speed (so not turbo). I've set this to 33%. 
 In my testing this script did not activate the power saving plan already visible in my "power options" page. If this happens to you please you use **enable_powersave.py** script, customise your plan as desired, then manually switch back to balanced.

# Limitations

 - This script does not discriminate, it doesn't know whether you've left your PC whilst you have only Reddit open or if you've left your PC whilst it's doing a computationally intensive task. In the future, I'd like to include the ability to set a blacklist mode that will disable the script if a certain program is open.

    

