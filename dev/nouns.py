import sys, re;

lemmas = {};
trads = {};

for line in open('lexicon.bxr.tsv').readlines(): #{
	if line.strip() == '': continue;

	row = line.strip('\n').split('\t');

	if row[1] != 'NOUN': continue;

	row[3] = row[3].lower().strip();
	row[4] = row[4].lower().strip();

	if row[4] not in lemmas: #{
		lemmas[row[4]] = [];
	#}
	if row[4] not in trads: #{
		trads[row[4]] = [];
	#}

	lemmas[row[4]].append(row[3]);
	if ',' in row[5]: 
		for w in row[5].split(','): trads[row[4]].append(w.strip());
	else: 
		trads[row[4]].append(row[5]);

#	print(row);

#}

feats = {};

for w in lemmas: #{
	if w not in feats: #{
		feats[w] = [];
	#}

	if re.match('.*[иүэаоөуыея]$', w): feats[w].append('-V');
	if re.match('.*[бвгджзйклмнпрстфхһцчшь]$', w): feats[w].append('-C');

	for form in lemmas[w]: #{
		if w[-1] == 'н' and form.count('н') == 0: feats[w].append('-н*');
		if w.count('(н)') > 0: feats[w].append('-н*');
		if re.match('.*[^н]ууд', form): feats[w].append('-UUд');
		if re.match('.*[^н]үүд', form): feats[w].append('-UUд');
		if w[-1] != 'н' and re.match('.*нууд', form): feats[w].append('-нUUд');
		if w[-1] != 'н' and re.match('.*нүүд', form): feats[w].append('-нUUд');
		if w[-1] != 'н' and re.match('.*нар$', form): feats[w].append('-нAр'); 
		if w[-1] != 'н' and re.match('.*нэр$', form): feats[w].append('-нAр'); 
		if w[-1] == 'н' and len(form) > len(w) and form[len(w)-1] != 'н': feats[w].append('-н*');
	#}
#	print(w, lemmas[w], feats[w]);
#}

#наһан {'-C'} ['наһанайнгаа', 'наһанайнгаа', 'наһан', 'наһатай', 'наһатай', 'наһандаа', 'наһанһаа', 'наһа', 'наһанһаань', 'наһанһаа', 'наһандань', 'наһанайнгаа', 'наһаараа', 'наһанайм', 'наһанай', 'наһанһаань', 'наһаараа'] {'age', 'life'}


for w in lemmas: #{
	_trad = ', '.join(list(set(trads[w])));
	if '-н*' in feats[w]: #{
		_w = w.replace('(н)', 'н');
		print('%s:%s N3 ; ! "%s"' % (_w, _w[0:-1], _trad));
		continue;
	elif '-C' and '-UUд' in feats[w]: #{
		print('%s:%s N1 ; ! "%s"' % (w, w, _trad));
		continue;
	elif '-C' and '-нUUд' in feats[w]: #{
		print('%s:%s N1 ; ! "%s"' % (w, w, _trad));
		continue;
	elif '-V' and '-нUUд' in feats[w]: #{
		print('%s:%s N2 ; ! "%s"' % (w, w, _trad));
		continue;
	elif '-C' and '-нAр' in feats[w]: #{
		print('%s:%s N4 ; ! "%s"' % (w, w, _trad));
		continue;
	#}
	if '-C' in feats[w]: #{
		print('%s:%s N1 ; ! "%s"' % (w, w, _trad));
		continue;
	elif '-V' in feats[w]: #{
		print('%s:%s N2 ; ! "%s"' % (w, w, _trad));
		continue;
	else: #{
		print('!!!', w, set(feats[w]), lemmas[w], set(trads[w]))
	#}

#	print('!', w, set(feats[w]), lemmas[w], set(trads[w]));
#}
