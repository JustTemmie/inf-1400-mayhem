from pyglet.math import Vec3, Vec2
from engine.core_ext.collision.collision3D.Hitsphere3D import Hitsphere3D
from engine.core_ext.collision.collision2D.Hitsphere2D import Hitsphere2D
from engine.core_ext.collision.collision2D.Hitbox2D import Hitbox2D
from engine.core_ext.collision.collision3D.Hitbox3D import Hitbox3D

if __name__ == "__main__":

    hitarea1 = Hitbox3D(Vec3(0, 0, 0), Vec3(3.15/4, 0, 0), Vec3(10, 10, 10), Vec3(0, 0, 0))
    hitarea2 = Hitsphere3D(Vec3(12, 0, 0), Vec3(0, 0, 0), 5)
    print(hitarea1.colliding_with(hitarea2))
