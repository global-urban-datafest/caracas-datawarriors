from engine import db_interface
import optparse

parser = optparse.OptionParser()
parser.add_option('-f', '--file', type='string', dest='filenames', action='append')
parser.add_option('-h', '--hostname', type='string', dest='hostname')
(opts, args) = parser.parse_args()

mandatories = ['filename', 'hostname']
for m in mandatories:
    if not opts.__dict__[m]:
        print "mandatory option missing"
        parser.print_help()
        exit(-1)

reserved_screen_names = []
for filename in opts.filename:
    text = open(filename).read()
    reserved_screen_names.append(text.split())


db = db_interface.DBInterface(opts.hostname)
db.connect()
count_is_base = 0
(tweet_ids, screen_names) = db.get_tweet_screen_names()

for (tid, sn) in zip(tweet_ids, screen_names):
    if sn in reserved_screen_names:
        is_base = 1
    else:
        is_base = 0
    if db.set_is_base_account(tid, is_base):
        count_is_base += 1

print "updated", count_is_base, "tweets"
