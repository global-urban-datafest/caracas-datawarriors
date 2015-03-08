import optparse

from engine import db_interface
from engine.sentiment import trainset_constructor

parser = optparse.OptionParser()
parser.add_option('-f', '--filename', help='training set file', type='string', dest='filename')
(opts, args) = parser.parse_args()

mandatories = ['filename']
for m in mandatories:
    if not opts.__dict__[m]:
        print "mandatory option missing"
        parser.print_help()
        exit(-1)

db = db_interface.DBInterface('localhost')
constructor = trainset_constructor.TrainsetConstructor(opts.filename, db)

constructor.run()
