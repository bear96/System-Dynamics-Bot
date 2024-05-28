from sage import GreatSage
import os
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Great Sage arguments.')
    parser.add_argument('--output_dir', type=str, default= './output', help='path to store outputs')
    parser.add_argument('--file_dir', type= str, default = None, help = 'path to the file containing the query if exists')
    parser.add_argument('--instances', type = int, default = 1, help = 'number of instances of CLD bot to be used (recommended 1, more if text is ambiguous)')
    parser.add_argument('--verbose', action = 'store_true', default = False, help = 'enable verbosity')
    parser.add_argument('--diagram', action = 'store_true', default = False, help = 'enable causal loop diagram geenration' )

    args = parser.parse_args()
    print("Args: \n", args)
    if not args.file_dir:
        question = input("Enter your problem description here: ")
    else:
        question = None
    bot = GreatSage( 
        verbose = args.verbose, 
        diagram = args.diagram, 
        question=question
        )
    relationships = bot.think()
    if relationships is not None:
        print("Final Relationship: \n", relationships)