#! /usr/bin/env python3
# coding: utf-8
import argparse
import pdb
import logging as lg
import re

import analysis.csv as c_an
import analysis.xml as x_an

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--datafile",help="""CSV file containing pieces of information about the members of parliament""")
    parser.add_argument("-v", "--verbose", action='store_true', help="""Make the application talk!""")
    parser.add_argument("-bp", "--byparty", action='store_true', help="""Display a graph for each political party""")
    parser.add_argument("-s", "--searchname", help="""Search a member by his/her name""")
    parser.add_argument("-gf", "--groupfirst", help="""Display the n bigger groups""")

    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.verbose:
        lg.basicConfig(level=lg.DEBUG)
    try:
        datafile = args.datafile
        searchname = args.searchname
        byparty = args.byparty
        groupfirst = int(args.groupfirst)
        e = re.search(r'^.+\.(\D{3})$', args.datafile)
        extension = e.group(1)

        if datafile == None:
            raise Warning('You must indicate a datafile!')
        else:
            try:
                if extension == 'xml':
                    x_an.launch_analysis(datafile)
                elif extension == 'csv':
                    c_an.launch_analysis("Assemblée Nationale Française", datafile, searchname, groupfirst, byparty)
            except FileNotFoundError as e:
                print("Ow :( The file was not found. Here is the original message of the exception :", e)
            finally:
                print('#################### Analysis is over ######################')
    except Warning as e:
        lg.warning(e)

if __name__ == "__main__":
    main()