#!/usr/bin/python
#
# Python script that calculates and returns the total score of a game of
# bowling.
#
# Rules:
# To briefly summarize the scoring for this form of bowling:
#  - One game of bowling is made up of ten frames.
#  - In each frame, the bowler has two throws to knock down all the pins.
#  - Possible results for a frame:
#  -- Strike ('X'): the bowler knocks down all 10 pins on the first throw. The
#     frame is over early. The score for the frame is 10 plus the total pins
#     knocked down on the next two throws.
#  -- Spare ('/'): the bowler knocks down all 10 pins using two throws. The
#     score for the frame is 10 plus the number of pins knocked down on the
#     next throw.
#  -- Open frame: the bowler knocks down less than 10 pins with his two throws.
#     The score for the frame is the total number of pins knocked down.
#  - The game score is the total of all frame scores.
#  - Special rules for the 10th frame:
#  -- A strike in the tenth frame gives the bowler two bonus throws, to fill
#     out the scoring formula for the last frame.
#  -- A spare in the tenth frame gives the bowler one bonus throw, to fill out
#     the scoring formula for the last frame.
#  -- These throws count as part of the 10th frame.
#  -- The process does not repeat - for example, knocking down all 10 pins on a
#     bonus throw does not provide any additional bonus throws.
#
# Following cases are outside the scope of the current exercise:
# - Check for valid throws (like scores that add to 11)
# - Check for the correct number of throws and frames
# - Provide any intermediate scores - it only has to provide the final score

import re
import sys


def total_score(data):
    """
    Parses a user input string and calculates the total score of the submitted
    bowling game.
    @type data: str
    @param data: String representing the throws of a single bowling game (split into frames). Eg. '12-34-5/-0/-X-X-X-X-X-X-XX'
    @rtype: int
    @return: Total calculated score.
    """
    if not data:
        return 0
    return score(regex_parse(data))


def regex_parse(data):
    """
    Utility method that transforms an input string into a list of elements
    that represent each throw taken in a single game. Non-numeric and invalid
    characters (anything besides '/' or 'X') are filtered out from the
    submitted input string.
    Example:
    A data input of '01-5/-0/-23-X-X-X-X-X-X-XX' will return the following list:
    [0, 1, 5, 5, 0, 10, 2, 3, 10, 10, 10, 10, 10, 10, 10, 10]
    @type data: str
    @param data: String of bowling scores split into frames and separated by
                  hyphens. Strikes are represented as 'X', spares are
                  represented as '/' and misses are represented as '0'.
    @rtype: list
    @return: List of integers where each element represents a single
             throw (in the order taken).
    """
    # filters all non numeric characters (except for '/' and 'X') from data
    # string and creates a list from remaining valid characters
    f_list = list(re.sub(r'[^\d/X]', '', data))
    # uses list comprehension and nested ternary expressions to assign the
    # proper numeric value for each element in the sanitized list
    return [10 - int(f_list[idx - 1]) if val is '/' else 10 if val is 'X' else
            int(val) for idx, val in enumerate(f_list)]

def score(throws, frame=1, total=0):
    """
    Recursive method that calculates the score of the bowling game one frame
    at a time and returns the total.
    @type throws: list
    @param throws: List of elements (throws) to be totaled.
    @type frame: int
    @param frame: Index of the frame being calculated. Default value: 1
    @type total: int
    @param total: Running total of the bowling game score. Default value: 0
    @rtype: int
    @returns: Final calculated total of the bowling game.
    """
    # exit case (frame 10 calculated or incomplete game)
    if frame > 10 or not throws:
        return total
    # strike
    elif throws[0] == 10:
        # bonus = next two throws following current frame
        bonus = 0
        # edge case logic for incomplete game
        if len(throws) >= 3:
            bonus = sum(throws[1:3])
        elif len(throws) > 1:
            bonus = throws[1]
        # pop off first index, increment frame count, update total
        return score(throws[1:], frame + 1, total + 10 + bonus)
    # spare
    elif sum(throws[0:2]) == 10:
        # bonus = next throw following current frame
        bonus = 0
        # edge case logic for incomplete game
        if len(throws) >= 3:
            bonus = throws[2]
        # pop off first two indexes, increment frame count, update total
        return score(throws[2:], frame + 1, total + 10 + bonus)
    # closed frame
    else:
        total += sum(throws[0:2])
        # pop off first two indexes, increment frame count, update total
        return score(throws[2:], frame + 1, total)


def run_tests():
    tests = [(300,'X-X-X-X-X-X-X-X-X-X-XX'),  # perfect game
             (90, '9-9-9-9-9-9-9-9-9-9-'),  # all open frames
             (150,'5/5/5/5/5/5/5/5/5/5/5'),  # all spares
             (167,'X7/9-X-88/-6XXX81')]    # closed frames / bonus throw
    for score, data in tests:
        result = "Testing: %s = %d: %s"
        try:
            assert score == total_score(data), 'FAIL'
            print (result % (data, score, 'PASS'))
        except AssertionError as e:
            print (result % (data, score, e))
 
if __name__ == "__main__":
    """
    Script entry point. Accepts a list of string data separated by spaces
    or runs a set of predefined unit tests if no arguments are provided.
    """
    if len(sys.argv) > 1:
        for data in sys.argv[1:]:
            print ("Input: %s Total: %d" % (data, total_score(data)))
    else:
        run_tests()