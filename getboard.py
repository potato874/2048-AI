from bs4 import BeautifulSoup
import re
import numpy as np

def get_tiles(browser):
    """
    Scrapes the webpage for raw data on the state of the board and generates a 4x4 matrix with tiles in the correct place
    """
    soup = BeautifulSoup(browser, 'lxml')


    # A lot of this is really inelegant because I'm scraping off raw HTML. I could've done this more cleanly if I had
    # a numerical representation of the board, but I don't know how to access that. Instead, I'm generating a new board based off of 
    # the class names inside <div class="tile-container">, which just follows the HTML in the actual website.

    tiles = [tile['class'] for tile in soup.select('.tile')] # This gives us the CSS class info of every tile on the board
    tile_info = np.zeros((4,4), dtype=int) # dict of the form {(xpos, ypos) : tile_val}
    for tile in tiles:
        val, x, y = int(re.match(r'tile-(\d+)', tile[1]).group(1)), int(tile[2][-3]), int(tile[2][-1])
        if val > tile_info[y-1][x-1]:
            tile_info[y-1][x-1] = val
    return tile_info

    #     if (x, y) not in tile_info:
    #         tile_info()
    # tile_info = [(tile[1], tile[2]) for tile in tiles] # Extract only the tiles' values and their position
    # tile_info = [(int(re.match(r'tile-(\d+)', val).group(1)), pos[-3], pos[-1]) for val, pos in tile_info] # extracts only the relevant numbers (tile value, xpos, ypos)
    # return tile_info # tile_info is a list of tuples (tile_val, xpos, ypos) for every tile on the board