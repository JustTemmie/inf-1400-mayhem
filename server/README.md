How the data is formatted (Probably under 1 KB):
```
0, 1        --- player/server ids (from, to)

2, 3, 4     --- client pos (x, y, z)
5, 6, 7     --- client velocity (x, y, z)
8, 9, 10    --- client acceleration (x, y, z)

11, 12, 13  --- client rotation (x, y, z)
14, 15, 16  --- client rotation speed (x, y, z)
17, 18, 19  --- client rotation acceleration (x, y, z)

20          --- new bullet? If 0 no new bullet

21          --- Killed by player id (if negativ not killed)
```
