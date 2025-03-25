How the data is formatted (Probably under 1 KB):
```
0, 1, 2     --- client pos (x, y, z)
3, 4, 5     --- client yaw, pitch, roll
4, 5, 6     --- client velocity in spheric cordinates (yaw, pitch, speed)
7           --- client roll speed
8, 9, 10    --- client acceleration in spheric cordinates (yaw, pitch, speed)
11          --- client roll acceleration

12, 13, 14  --- new bullet pos (x, y, z) (If zero, no new bullet)
15, 16, 17  --- new bullet yaw, pitch, roll
18, 19, 20  --- new bullet velocity in spheric cordinates (yaw, pitch, speed)
21          --- new bullet roll speed (This will be zero for every bullet)
22, 23, 24  --- new bullet acceleration in spheric cordinates (yaw, pitch, speed) (This will be zero for every bullet)
25          --- new bullet roll acceleration(This wil be zero for every bullet)

26          --- Killed by player id (if zero not killed)
```
