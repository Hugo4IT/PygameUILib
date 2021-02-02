# PygameUILib by Hugo4IT
### WORK IN PROGRESS, PLEASE DONT USE YET
#### Please go to bottom of the page for progress info
A simple, fast GUI solution for Pygame. [WORK-IN-PROGRESS] Please do not use yet, big changes are planned, so your code will probably not work in future versions. PygameUILib only has 1 dependency: pygame. Meaning that this library doesn't require any other library to function. This library also includes a CSS interpreter for styling, this interpreter has a big O notation of O(n) meaning that it is very fast and doesn't scale exponentially based on filesize!

#### Speed
I have done some speed tests with this css interpreter and these are the results, time is measured in seconds and all stylesheet results were stored in memory so the garbage collector didn't interfere. Large CSS File is a `4200 line 160kb` CSS file full of code
  #### Ryzen 5 3600x:
  ```
  Test 1 - Large CSS File:
    Time (seconds): 0.4530792236328125
    Memory usage after test (MegaBytes): 12.734375
  Test 2 - 100 Large CSS Files:
    Time (seconds): 47.259774684906006
    Memory usage after test (MegaBytes): 49.2890625
  ```
And while these scores are definetly not perfect, it is at least decent and enough for any project of almost any size
    
## Installation:
- #### Windows
  - Open command prompt
  - Enter `pip install PygameUILib`
  - Done
- #### Windows (Super beginner)
  - Copy this text: `pip install PygameUILib`
  - Press `Windows Icon` + `R`
  - Type `cmd`
  - Hit `Enter ↵`
  - A black window should have popped up
  - Right click on the black window
  - Hit `Enter ↵`
  - Done
- #### Linux/MacOS:
  - Open the app `Terminal` (Name may vary when using linux)
  - Enter `pip install PygameUILib`
  - Done

## How to use/Documentation
Take a look at the documentation and a beginner guide on my [Website](https://Hugo4IT.com/PygameUILib)
(Documentation currently work-in-progress, please wait until it releases)
