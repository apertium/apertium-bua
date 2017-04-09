import sys;

# 0      1        2    3        4         5	6
# 392	PUNCT		.	.			
# 137	PUNCT		,	,			
# 31	VERB	IV	байгаа	байха	be	hargle	
# 

#    833 .	PUNCT
#    704 ,	PUNCT
#     89 гэжэ	PART

principal = open(sys.argv[1]);
nou = open(sys.argv[2]);

freq = {};
dicc = {};

noinfl = ['ADP','ADV', 'AUX', 'CONJ', 'DET', 'INTJ', 'PART', 'PUNCT', 'SCONJ', 'SYM'];

for line in principal.readlines(): #{

	if '\t' not in line: #{
		continue;
	#}
	row = line.strip().split('\t');

	if (row[3], row[1]) not in dicc: #{
		dicc[(row[3], row[1])] = row;
	#}
#}

for line in nou.readlines(): #{

	if '\t' not in line: #{
		continue;
	#}

	row = line.strip().split('\t');
	newfreq = row[0];
	if row[2] != 'PROPN': #{
		row[1] = row[1].lower();
	#}
	subcat = '';
	lem = '@';
	if row[2] == 'VERB': #{
		subcat = 'TD';
	#}
	if row[2] in noinfl: #{
		lem = row[1];	
	#}
	if (row[1], row[2]) in dicc: #{
		oldrow = dicc[(row[1], row[2])]
		pos = oldrow[1]; 
		lem = oldrow[4];
		glos = '\t'.join(oldrow[5:]);
		if oldrow[2] != '': #{
			subcat = oldrow[2];
		#}
		print('%s\t%s\t%s\t%s\t%s\t%s' % (newfreq, pos, subcat, row[1], lem, glos));
	else: #{
		print('%s\t%s\t%s\t%s\t%s\t%s' % (newfreq, row[2], subcat, row[1], lem, '@'));
	#}
#}



