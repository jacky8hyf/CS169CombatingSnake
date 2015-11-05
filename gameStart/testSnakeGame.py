__author__ = 'TrevorTa'
# Tests for snakeGame.py
#from django.test import TestCase
from snakeGame import *
from unittest import TestCase

class SnakeTestCase(TestCase):

    def testSnakeInit(self):
        snake = Snake([[1,1]], Direction.UP)
        self.assertTrue(snake.direction == Direction.UP)
        self.assertTrue(len(snake.body) == 1)
        self.assertTrue(snake.body[0] == [1,1])

    def testMoveSnake(self):
        snake = Snake([(1,1)], Direction.UP)
        snake.move()
        self.assertTrue(len(snake.body) == 1)
        self.assertTrue(snake.body[0] == [0,1])

    def testChangeDirection(self):
        snake = Snake([[1,1]], Direction.UP)
        snake.changeDirection(Direction.DOWN)
        # not allow to change to opposite direction
        self.assertTrue(snake.direction == Direction.UP)
        snake.changeDirection(Direction.LEFT)
        self.assertTrue(snake.direction == Direction.LEFT)
        snake.changeDirection(Direction.STAY)
        self.assertTrue(snake.direction == Direction.STAY)
        snake.changeDirection(Direction.RIGHT)
        self.assertTrue(snake.direction == Direction.RIGHT)
        snake.changeDirection(Direction.LEFT)
        self.assertTrue(snake.direction == Direction.RIGHT)
        snake.changeDirection(Direction.UP)
        self.assertTrue(snake.direction == Direction.UP)

    def testMoveAndChangeDirection(self):
        snake = Snake([[1,1]], Direction.UP)
        snake.move()
        self.assertTrue(len(snake.body) == 1)
        self.assertTrue(snake.body[0] == [0,1])
        snake.changeDirection(Direction.LEFT)
        snake.move()
        self.assertTrue(snake.body[0] == [0,0])
        snake.changeDirection(Direction.STAY)
        snake.move()
        self.assertTrue(snake.body[0] == [0,0])


    def testEatFood(self):
        snake = Snake([[1,1]], Direction.UP)
        snake.eatFood([1, 2]) # add to the front of the list
        snake.eatFood([1, 3])
        snake.eatFood([1, 4])
        self.assertTrue(len(snake.body) == 4)
        self.assertTrue(snake.body == [[1,4],[1,3],[1,2],[1,1]])

    def testRemoveTail(self):
        snake = Snake([[1,1],[1,2],[1,3],[1,4]], Direction.UP)
        snake.removeTail()
        self.assertTrue(len(snake.body) == 3)
        self.assertTrue(snake.body == [[1,1],[1,2],[1,3]])
        snake.removeTail()
        self.assertTrue(len(snake.body) == 2)
        self.assertTrue(snake.body == [[1,1],[1,2]])

    def testEatAndRemoveTail(self):
        snake = Snake([[1,1],[1,2],[1,3],[1,4]], Direction.UP)
        snake.removeTail()
        self.assertTrue(len(snake.body) == 3)
        self.assertTrue(snake.body == [[1,1],[1,2],[1,3]])
        snake.eatFood([1,0])
        snake.removeTail()
        self.assertTrue(len(snake.body) == 3)
        self.assertTrue(snake.body == [[1,0],[1,1],[1,2]])

class DirectionTestCase(TestCase):
    def testOppositeDirection(self):
        self.assertTrue(Direction.isOppositeDirection(Direction.LEFT, Direction.RIGHT))
        self.assertTrue(Direction.isOppositeDirection(Direction.RIGHT, Direction.LEFT))
        self.assertTrue(Direction.isOppositeDirection(Direction.UP, Direction.DOWN))
        self.assertTrue(Direction.isOppositeDirection(Direction.DOWN, Direction.UP))
        self.assertFalse(Direction.isOppositeDirection(Direction.DOWN, Direction.LEFT))
        self.assertFalse(Direction.isOppositeDirection(Direction.DOWN, Direction.RIGHT))
        self.assertFalse(Direction.isOppositeDirection(Direction.UP, Direction.RIGHT))
        self.assertFalse(Direction.isOppositeDirection(Direction.UP, Direction.UP))

    def testNewPoint(self):
        self.assertTrue(Direction.newPoint([1,0], Direction.RIGHT) == [1,1])
        self.assertTrue(Direction.newPoint([5,5], Direction.LEFT) == [5,4])
        self.assertTrue(Direction.newPoint([1,0], Direction.DOWN) == [2,0])
        self.assertTrue(Direction.newPoint([1,0], Direction.UP) == [0,0])
        self.assertTrue(Direction.newPoint([1,0], Direction.STAY) == [1,0])
        self.assertTrue(Direction.newPoint([1,3], Direction.RIGHT) == [1,4])

class BoardTestCase(TestCase):
    def testInitBoard(self):
        board = Board(5, 5, 4)
        self.assertEquals(board.w, 5)
        self.assertEquals(board.h, 5)
        self.assertEquals(board.numPlayers, 4)
        self.assertEquals(len(board.foods), 3)
        self.assertEquals(len(board.snakes), 4)