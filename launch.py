# starts the client

#import cProfile
from mayhem.Mayhem import Mayhem

if __name__ == "__main__":
    mayhem = Mayhem()
    mayhem.run()

    #cProfile.run("mayhem.run()", filename="mayhem.prof")
