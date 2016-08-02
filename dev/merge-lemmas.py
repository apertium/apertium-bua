import sys;

tb = sys.argv[1];
lk = sys.argv[2];

sozluk = {};
#31	VERB	байгаа	байха	be
for line in open(lk).readlines(): #{
	row = line.strip('\n').split('\t');
	lem = row[3];
	pos = row[1];
	sur = row[2];
	
	if (sur, pos) not in sozluk: #{
		sozluk[(sur, pos)] = set();
	#}
	sozluk[(sur, pos)].add(lem);	
#}

#2	бэшээ	_	VERB	_	_	0	root	_	Offset=15-20
for line in open(tb).readlines(): #{
	if line.strip() == '': #{
		print(line);
		continue;
	#}
	row = line.strip('\n').split('\t');
	if (row[1], row[3]) in sozluk: #{
		if len(sozluk[(row[1], row[3])]) == 1: #{
			row[2] = list(sozluk[(row[1], row[3])])[0];
		else: #{
			print('ERROR: multiple lemmas', sozluk[(row[1], row[3])], file=sys.stderr);
		#}
	elif row[3] == 'PUNCT': #{
		row[2] = row[1];
	elif row[3] == 'NUM' and row[1].isnumeric(): #{
		row[2] = row[1];
	else: #{
		print('ERROR:', row[1], row[3], 'not in', sozluk, file=sys.stderr);
		sys.exit(-1);
	#}	
	print('\t'.join(row));
#}
