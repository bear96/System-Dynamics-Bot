from sage import GreatSage
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Great Sage arguments.')
    parser.add_argument('--verbose', action = 'store_true', default = False, help = 'enable verbosity')
    parser.add_argument('--diagram', action = 'store_true', default = False, help = 'enable causal loop diagram generation' )
    parser.add_argument('--write_relationships', action = 'store_true', default = False, help = 'write the final relationships to a text file')
    parser.add_argument('--xmile', action = 'store_true', default = False, help = 'save the generated diagram as XMILE for use in Stella and other associated tools which support XMILE' )

    args = parser.parse_args()
    print("Args: \n", args)
    question = input("Enter your problem description here: ")
    bot = GreatSage( 
        verbose = args.verbose, 
        diagram = args.diagram,
        write_relationships = args.write_relationships,
        xmile = args.xmile, 
        question= question
        )
    relationships = bot.think()
    if relationships is not None:
        print("Final Relationship: \n", relationships)