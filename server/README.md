How the data is formatted (Probably under 1 KB):
```
0, 1        --- player/server ids (from, to)

2, 3, 4     --- client pos (x, y, z)
5, 6, 7     --- client velocity (x, y, z)
8, 9, 10    --- client acceleration (x, y, z)

11, 12, 13  --- client rotation (x, y, z)
14, 15, 16  --- client rotation speed (x, y, z)
17, 18, 19  --- client rotation acceleration (x, y, z)

20, 21, 22  --- new bullet pos (x, y, z) (If zero, no new bullet)
23, 24, 25  --- new bullet speed (x, y, z)
26, 27, 28  --- new bullet acceleration (x, y, z)

29, 30, 31  --- new bullet rotation (x, y, z)
32, 33, 34  --- new bullet rotation speed (x, y, z)
35, 36, 37  --- new bullet rotation acceleration (x, y, z)

38          --- Killed by player id (if zero not killed)
```
