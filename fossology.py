import sys
from subprocess import Popen, PIPE
import psycopg2

try:
	conn = psycopg2.connect("dbname='fossology' user='fossy' host='localhost' password='fossy'")
except:
	print 'I am unable to connect to the database'

cur = conn.cursor()

arguments = ['nomos', '-d'] + sys.argv[1:]

p = Popen(arguments, stdout=PIPE, stderr=PIPE, stdin=PIPE);

output = []

while True:
	line = p.stdout.readline().rstrip()
	if line != '':
		output.append(tuple([line]))
	else:
		break

insert_template = ','.join(['%s'] * len(output))
insert_query = 'insert into license_result (result) values {0}'.format(insert_template)
cur.execute(insert_query, output)	
conn.commit()
