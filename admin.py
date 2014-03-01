#!/usr/bin/env python

from argparse import ArgumentParser

if __name__ == "__main__":
    aparser = ArgumentParser(description="labevents management interface")
    aparser.add_argument("command")

    args = aparser.parse_args()

    if args.command == "runserver":
        from labevents import app
        app.run(debug=True)
    elif args.command == "initdb":
        from labevents.models import Base
        from labevents.database import engine
        Base.metadata.create_all(engine)
    else:
        print "[!] command not found"
        sys.exit(-1)
