# PygameUILib by Hugo4IT
### WORK IN PROGRESS, PLEASE DONT USE YET
#### Please go to bottom of the page for progress info
A simple, fast GUI solution for Pygame

For progress info or submissions of ideas/elements, click [Here](https://trello.com/b/9dwC0kAZ/pygameuilib-pygameanimationlib)

## How to use:
- Download this repo
- (Optional) Run `main.pyw` to test if it works/is something for you
- Copy `PygameAnimationLib.pyw` and `PygameUILib.pyw` to your project folder
- Profit

### CURRENT DOCUMENTATION OUT OF DATE

```python
btnConfig = """
position: 400,400           // Position X,Y (Center)                    [btn.x, btn.y]
size: 300,100               // Size X,Y (From Center)                   [btn.sx, btn.sy]
color: #263238              // Color Hex/Name                           [btn.maincolor, current color = btn.color]
hovercolor: #303C42         // Color on mouse hover                     [btn.hovercolor]
clickedcolor: #A911BD       // Color on click                           [btn.clickedcolor]
rounded: True               // Rounded corners                          [btn.rounded]
radius: 30                  // Corner radius                            [btn.radius]
bordered: True              // Bordered rect                            [btn.bordered]
bordersize: 10              // Border width                             [btn.bordersize]
bordercolor: #1E282D        // Border color                             [btn.mainbordercolor, current border color = btn.bordercolor]
borderhovercolor: #E7E5F1   // Border color on hover                    [btn.borderhovercolor]
borderclickedcolor: #A892DF // Border color on click                    [btn.borderclickedcolor]
hidden: False               // Hide Button                              [btn.hidden]
responsive: True            // Reacts to movement/clicks                [btn.responsive]
nonresponsivecolor: #3E4B50 // Color when responsive = False            [btn.nonresponsivecolor]
fontcolor: #FFFFFF          // Font color (Textcolor)                   [NOT IMPLEMENTED]
fontsize: auto              // Size of font (can be int or auto)        [NOT IMPLEMENTED]
"""

labelConfig = """
fontsize: 30
position: 500,500
fontcolor: #037CD6
"""

btnTest = Button(btnConfig)
labelTest = Label("Heloo, am snek", "Arial", 30, 500, 500, "Red")
```

For progress info or submissions of ideas/elements, click [Here](https://trello.com/b/9dwC0kAZ/pygameuilib-pygameanimationlib)
