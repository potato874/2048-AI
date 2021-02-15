"""
Instantiates a new WebDriver for selenium to control and sends keystrokes to play the game and reset when it ends
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
from board_actions import BoardDriver
import logging

# TODO: Use a logger instead of basicConfig
logging.basicConfig(filename='BoardDriver.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def play():
    # Takes the browser to play2048.co and starts a game
    browser = webdriver.Chrome()
    browser.get('https://play2048.co/')
    newGame = browser.find_element_by_class_name('restart-button')
    newGame.click()

    board = BoardDriver(browser)
    # sends keys in the sequence UP, DOWN, LEFT, RIGHT and restarts the game when the option appears
    while True:
        print(f"New board: \n{board.get_tiles()}")
        # Retrieve the best move we can perform
        best_move = board.get_best_move(board.get_tiles())
        print(f"Best move is {best_move.__name__}")
        # Execute the best move
        best_move()

        # it takes a while for the HTML to update with the board, so I need to wait a bit. Otherwise, get_tiles()
        # gives a wrong board, one where the move/s might not have been done yet

        # Try to click "Keep Going" if it shows up
        try:
            # Store the current board and score
            win_board = str(board.get_tiles())
            win_score = browser.find_element_by_class_name('score-container').text

            # Press the "Keep Going" button that shows up when we reach the 2048 tile
            continueGame = browser.find_element_by_class_name(
                'keep-playing-button')
            continueGame.click()    # Raises an exception if the button doesn't exist

            # Assuming we didn't fly into the 'except' yet, log the board's current state
            logging.info("REACHED 2048")
            logging.info('\n' + win_board)
            logging.info(f"SCORE: {win_score}")
        except:
            pass

        # If there's no "Keep Going" but retry-button shows up, press that instead
        # Since it means we lost and the board is currently in a Game Over state
        try:
            # Store the current board and score
            lose_board = str(board.get_tiles())
            lose_score = browser.find_element_by_class_name('score-container').text

            # Reset the game when we lose
            resetGame = browser.find_element_by_class_name('retry-button')
            resetGame.click()   # Raises an exception if the button doesn't exist

            # Assuming we didn't go into the 'except' yet, log the current board and score
            logging.info("GAME OVER")
            logging.info('\n' + lose_board)
            logging.info(f"SCORE: {lose_score}")
        except:
            pass


if __name__ == "__main__":
    play()
