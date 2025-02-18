# IdlePowerplan
A lightweight Python script to change the power plan in Windows after a predetermined period of user inactivity.

---

I created this script to solve a problem with my girlfriends laptop. Whenever her laptop was left to idle Windows would decide to run various processes: Defender scans, disk optimisation, updates, etc. However these processes would cause the fans to kick in with their incredibly aggressive curves meaning it sounded like a jet engine when the CPU was only at 55c running some background processes in idle. I initially tried to solve this using Process Lasso, I created a power saving plan with max CPU utilisation capped at 33%, and set it so that after 2 minutes of no user activity the system would switch to this plan, still allowing background processes to run but also ensuring the CPU doesn't heat up and causes the laptop to turn into a jet. This worked decently well, though it couldn't detect when video was playing, so if we were watching something on YouTube, the power plan would change, clock down the CPU, and the video would start stuttering.

---

This Python script is able to detect both user input and whether or not any audio is playing on the system, and will only change to the power saving plan once there has been a predetermined period of user inactivity and there is no audio currently playing.

---

I created this script to be as efficient as possible, reducing overhead, minimising API calls to a bare minimum. Because of this, this script is not super accurate in its default state. If you input 120 seconds as your desired idle time, it probably won't go idle specifically after 120 seconds, it'll probably idle anywhere between 110-130 seconds. This is with the default check_frequency of 10 seconds. If you desire a greater degree of accuracy you can increase this to be as fast as you want, but again, I set this parameter to be slow to minimise any performance impact. The check_frequency is increased to 1 second during idle for a snappier response once user activity is detected. If that is not fast enough for you, you could speed this up even further.
