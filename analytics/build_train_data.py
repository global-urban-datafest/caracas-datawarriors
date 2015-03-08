# -*- coding: utf-8 -*-

import optparse

from engine import db_interface
from engine.sentiment import trainset_constructor

parser = optparse.OptionParser()
parser.add_option('-f', '--filename', help='training set file', type='string', dest='filename')
parser.add_option('-h', '--hostname', help='hostname', type='string', dest='hostname')
(opts, args) = parser.parse_args()

mandatories = ['filename', 'hostname']
for m in mandatories:
    if not opts.__dict__[m]:
        print "mandatory option missing"
        parser.print_help()
        exit(-1)

db = db_interface.DBInterface(opts.hostname)
constructor = trainset_constructor.TrainsetConstructor(opts.filename, db)

constructor.run()
