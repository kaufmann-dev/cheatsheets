#### Resize video to specific size (Includes Audio)
```bash
./size-limit-encoder.sh input.mp4 4
```
*Calculates video bitrate by subtracting audio bitrate, keeping the final file accurately under the size limit even with audio.*

#### Resize video to specific size .webm (Advanced, Includes Audio)
```bash
python restrict.py -a -s 4 input.mp4
```
*Feature-rich python script that handles complex encoding (auto downscaling, subtitles, etc.) with precise size limits.*

#### Resize video to specific size (Video-only budget)
```bash
./resize.sh input_video.mp4 <target_size_in_MB>
```
*Warning: Video bitrate uses the entire size limit budget. If the input file has audio, the resulting file will exceed the target limit!*

#### Hexagonal Object Positioning Calculator
```bash
python hexagonal-position-calculator.py
```
*Calculates exact transformation coordinates (x, z) for 6 objects positioned around a central hexagon, given the hexagon's width and additional spacing distance.*

#### JavaScript & jQuery Utilities (`utils.js`)
```javascript
randomIntFromInterval(min, max); // Generate random integer between min and max
jQuery.fn.hasScrollBar();        // Check if an element has a vertical scrollbar
jQuery.fn.clickToggle(fn1, fn2); // Toggle between two click handler functions
jQuery.fn.search(selector);      // Filter elements by matching text content
```
*A collection of helper functions for standard JS and jQuery UI interactions.*