from mazegenerator.mazegenerator import MazeGenerator  # type: ignore[import]


maze = MazeGenerator()
maze.generate(42)

print(maze.maze)
