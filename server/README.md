How the data is formatted (Probably under 1 KB):
```
0           --- If not zero, this is a chat message, and the rest of the format can be ignored

1, 2        --- player/server ids (from, to)

3, 4, 5     --- client pos (x, y, z)
6, 7, 8     --- client velocity (x, y, z)
9, 10, 11    --- client acceleration (x, y, z)

12, 13, 14  --- client rotation (x, y, z)
15, 16, 17  --- client rotation speed (x, y, z)
18, 19, 20  --- client rotation acceleration (x, y, z)

21          --- new bullet? If 0 no new bullet

22          --- Killed by player id (if negativ not killed)
```
