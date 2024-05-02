# Credits: inspired by this the submodule from this repo: https://github.com/JPAntonisse/privacy-policy-evaluator
# This is the main running file for the Privacy Policy Score/Rating out of 10, the higher the score -> more concerning

# Note: the privacy policy needs to be in a .txt file
# Instructions to get the privacy policy score:
# python ppe.py evaluate "path to .txt file"
# Output: Float score ranging from 0-10

# if it doesn't work, run:
# python setup.py
# pip install sklearn
from privacy_policy_score.privacy_policy_evaluator import commands, helpers, wordscoring
from typing import Callable


def main(args=None):
    """
    Main Starting Code
    """
    # Parse input
    args = commands.parser.parse_args(args)
    try:
        # Select the function in this document that is the first argument
        arg_func: Callable = globals()[args.function]
        # Call the function
        arg_func(args)
    except KeyError:
        commands.parser.parse_args(['-h'])
        pass

def evaluate(args):
    """
    Evaluate a score
    :param args:
    """
    # Read textfile
    text = helpers.read_file(args.file)
    # Get the Score
    score = wordscoring.score_text(text)
    print(score['mean_privacy'])
    return score
 


if __name__ == '__main__':
    main()
