import sys;

tb = sys.argv[1];
lk = sys.argv[2];

def sanitise(s): #{
	o = s;
	o = o.replace('θ', 'Ө'); # U+03B8 GREEK SMALL LETTER THETA
	o = o.replace('ɵ', 'ө'); # U+0275 LATIN SMALL LETTER BARRED O
	o = o.replace('h', 'һ'); # U+0068 LATIN SMALL LETTER H
	o = o.replace('γ', 'ү'); # U+03B3 GREEK SMALL LETTER GAMMA
	return o;
#}

sozluk = {};
#36	VERB	IV	байгаа	байха	be	
#4      NOUN            орондо  орон    country
#4      NOUN            орой    орой    peak, top
#4      ADV             ори     ори     all, quite, very
#4      DET             өөрынгөө        өөрын   own
#4      DET             өөрын   өөрын   own


for line in open(lk).readlines(): #{
	line = sanitise(line);
	row = line.strip('\n').split('\t');
	lem = row[4].strip();
	pos = row[1].strip();
	sur = row[3].strip();
#	print(row,'|||lem:', lem,'|pos:', pos, '|sur:',sur, file=sys.stderr);	
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

	line = sanitise(line);
	
	row = line.strip('\n').split('\t');
	if (row[1].strip(), row[3].strip()) in sozluk: #{
		if len(set(sozluk[(row[1].strip(), row[3].strip())])) == 1: #{
			row[2] = list(sozluk[(row[1].strip(), row[3].strip())])[0];
		else: #{
			print('ERROR: multiple lemmas for %s' % (row[1].lower()), sozluk[(row[1], row[3])], file=sys.stderr);
		#}
	elif (row[1].strip().lower(), row[3].strip()) in sozluk: #{
		if len(set(sozluk[(row[1].strip().lower(), row[3].strip())])) == 1: #{
			row[2] = list(sozluk[(row[1].strip().lower(), row[3].strip())])[0];
		else: #{
			print('ERROR: multiple lemmas for %s' % (row[1].lower()), sozluk[(row[1].lower(), row[3])], file=sys.stderr);
		#}
	elif row[3] == 'PUNCT': #{
		row[2] = row[1].strip();
	elif row[3] == 'NUM' and row[1][0].isnumeric(): #{
		row[2] = row[1].strip();
	else: #{
		print('ERROR:', row[1], row[3], '\tnot found.', len(sozluk), file=sys.stderr);
		sys.exit(-1);
	#}	
	print('\t'.join(row));
#}
