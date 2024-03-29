#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import sys
import os
import time

import requests
import requests_cache

from inky import InkyWHAT

from PIL import Image, ImageFont, ImageDraw
from font_source_serif_pro import SourceSerifProSemibold
from font_source_sans_pro import SourceSansProSemibold

def get_all_readwise_highlights(readwise_token):
    """ Returns a list of json objects corresponding to highlights extracted from the Readwise website.
    The function takes 1 parameter, which is the token used for accessing the user's Readwise highlights
    through the Readwise API.
    Shamelessly ripped from https://github.com/tibobrc/Blinkist-to-Readwise
    """

    all_current_readwise_highlights = []
    get_url = "https://readwise.io/api/v2/highlights/"
    # Use a loop to load more highlights in case not all highlights were returned.
    while get_url is not None:
        api_response = requests.get(
            url=get_url,
            headers={"Authorization": "Token " + readwise_token},
            params={
                'page_size': 1000
            }
        )
        if api_response.status_code != 200:
            print("Error: Extract of highlights from Readwise failed with status code " +
                  str(api_response.status_code) + '. Please check that the provided Readwise token is correct.')
            return None
        data = api_response.json()
        get_url = data['next']
        all_current_readwise_highlights = all_current_readwise_highlights + \
            data['results']
        time.sleep(5)
    return all_current_readwise_highlights

def get_all_readwise_books(readwise_token):
    all_current_readwise_books = []
    get_url = "https://readwise.io/api/v2/books/"
    
    # Use a loop to load more books in case not all books were returned.
    while get_url is not None:
        api_response = requests.get(
            url=get_url,
            headers={"Authorization": "Token " + readwise_token},
            params={
                'page_size': 1000
            }
        )
        if api_response.status_code != 200:
            print("Error: Extract of books from Readwise failed with status code " +
                  str(api_response.status_code) + '. Please check that the provided Readwise token is correct.')
            return None
        data = api_response.json()
        get_url = data['next']
        all_current_readwise_books = all_current_readwise_books + \
            data['results']
        time.sleep(5)
    return all_current_readwise_books

# This function will take a quote as a string, a width to fit
# it into, and a font (one that's been loaded) and then reflow
# that quote with newlines to fit into the space required.

def reflow_quote(quote, width, font):
    words = quote.split(" ")
    reflowed = '"'
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getsize(word)[0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n  " + word

    reflowed = reflowed.rstrip() + '"'

    return reflowed

def setRandomText(highlightOptions, colour="red"):

    # Set up the correct display and scaling factors
    inky_display = InkyWHAT(colour)
    inky_display.set_border(inky_display.WHITE)
    # inky_display.set_rotation(180)

    # Create a new canvas to draw on

    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    # Load the fonts

    font_size = 16

    w = inky_display.WIDTH
    h = inky_display.HEIGHT
    padding = 50

    def do_reflow(font_size, quote, author):
        author_font = ImageFont.truetype(SourceSerifProSemibold, font_size)
        quote_font = ImageFont.truetype(SourceSansProSemibold, font_size) 
        max_width = w - padding
        max_height = h - padding - author_font.getsize("ABCD ")[1]      
        reflowed = reflow_quote(quote, max_width, quote_font)
        p_w, p_h = quote_font.getsize(reflowed)  # Width and height of quote
        p_h = p_h * (reflowed.count("\n") + 1)   # Multiply through by number of lines
        return p_w, p_h, max_width, max_height, author_font, quote_font, reflowed

    below_max_length = False

    # Only pick a quote that will fit in our defined area
    # once rendered in the font and size defined.

    while not below_max_length:
        random_quote = random.choice(highlightOptions)
        quote = random_quote["text"]
        author = '― ' + random_quote["book"]["author"]

        p_w, p_h, max_width, max_height, author_font, quote_font, reflowed = do_reflow(font_size, quote, author)

        if p_h < max_height:
            below_max_length = True              # The quote fits! Break out of the loop.

        else:
            continue

    fits = True

    while fits == True:
        font_size = font_size + 1
        p_w, p_h, max_width, max_height, author_font, quote_font, reflowed = do_reflow(font_size, quote, author)
        if p_h >= max_height:
            fits = False              # The quote is too big, use one smaller
            font_size = font_size - 1
            p_w, p_h, max_width, max_height, author_font, quote_font, reflowed = do_reflow(font_size, quote, author)
        else:
            continue

    # x- and y-coordinates for the top left of the quote

    quote_x = (w - max_width) / 2
    quote_y = ((h - max_height) + (max_height - p_h - author_font.getsize("ABCD ")[1])) / 2

    # x- and y-coordinates for the top left of the author

    author_x = quote_x
    author_y = quote_y + p_h

    # Draw red rectangles top and bottom to frame quote

    draw.rectangle((padding / 4, padding / 4, w - (padding / 4), quote_y - (padding / 4)), fill=inky_display.RED)
    draw.rectangle((padding / 4, author_y + author_font.getsize("ABCD ")[1] + (padding / 4) + 5, w - (padding / 4), h - (padding / 4)), fill=inky_display.RED)

    # Add some white hatching to the red rectangles to make
    # it look a bit more interesting

    hatch_spacing = 12

    for x in range(0, 2 * w, hatch_spacing):
        draw.line((x, 0, x - w, h), fill=inky_display.WHITE, width=3)

    # Write our quote and author to the canvas

    draw.multiline_text((quote_x, quote_y), reflowed, fill=inky_display.BLACK, font=quote_font, align="left")
    draw.multiline_text((author_x, author_y), author, fill=inky_display.RED, font=author_font, align="left")

    print(reflowed + "\n" + author + "\n")

    # Display the completed canvas on Inky wHAT

    inky_display.set_image(img)
    inky_display.show()

def get_book_for_highlight(id, all_books):
    for book in all_books:
        if book["id"] == id:
            result = book
            break
        else:
            result = {}
    return result

def setHighlight():
    requests_cache.install_cache(cache_name='highlights_cache', expire_after=1)
    token = os.environ.get("READWISE_TOKEN")

    all_highlights = get_all_readwise_highlights(token)
    all_books = get_all_readwise_books(token)

    highlight_options = []

    for highlight in all_highlights:
        highlight["book"] = get_book_for_highlight(highlight["book_id"], all_books)
        highlight_options.append(highlight)

    setRandomText(highlight_options)

if __name__ == '__main__':
    setHighlight()
