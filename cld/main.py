from sage import GreatSage
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Great Sage arguments.')
    parser.add_argument('--verbose', action = 'store_true', default = False, help = 'enable verbosity')
    parser.add_argument('--diagram', action = 'store_true', default = False, help = 'enable causal loop diagram geenration' )

    args = parser.parse_args()
    print("Args: \n", args)
    question = input("Enter your problem description here: ")
    bot = GreatSage( 
        verbose = args.verbose, 
        diagram = args.diagram, 
        question=question
        )
    relationships = bot.think()
    if relationships is not None:
        print("Final Relationship: \n", relationships)