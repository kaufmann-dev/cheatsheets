#### Encode MP4 to a maximum size
```bash
video-size input.mp4 4
```
*Automatically chooses bitrate, resolution, frame rate, and audio quality, then only saves an output that fits at or below the requested MB size.*

#### Encode MP4 to a maximum size without audio
```bash
video-size input.mp4 4 --video-only
```
*Drops audio and uses the full size budget for video.*

#### Resize video to specific size .webm (Advanced, Includes Audio)
```bash
python restrict.py -a -s 4 input.mp4
```
*Feature-rich python script that handles complex encoding (auto downscaling, subtitles, etc.) with precise size limits.*

#### SiriKali lockbox CLI wrapper
```bash
lockbox config
lockbox mount
lockbox unmount
```
*Configures, mounts, opens, and unmounts one SiriKali encrypted folder from the terminal without opening the GUI.*

#### Hexagonal Object Positioning Calculator
```bash
python hexagonal-position-calculator.py
```
*Calculates exact transformation coordinates (x, z) for 6 objects positioned around a central hexagon, given the hexagon's width and additional spacing distance.*

#### JavaScript Utilities (`utils.js`)
```javascript
randomIntFromInterval(min, max);             // Generate random integer between min and max
hasScrollbar(element);                       // Check if an element has a vertical scrollbar
clickToggle(element, fn1, fn2);              // Toggle between two click handler functions
filterByText(input, document.querySelectorAll(".item")); // Filter elements by matching text
```
*A collection of dependency-free helper functions for standard JavaScript UI interactions.*
