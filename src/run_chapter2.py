import argparse
from chapter2 import CFGCore, LL1


def main(args):
    
    if not args.ll1:
        CFGCore(args.f)
    else:
        print(args.ll1)
        ll1 = LL1(args.f)
        ll1.LL1_construct(args.ll1)



if __name__ == "__main__":
    # python main.py -c 2 -f .\chapter2\testfiles\g8.txt

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, help="test file path")
    parser.add_argument('--ll1',type=str,help='use ll1')

    args = parser.parse_args()
    main(args)
