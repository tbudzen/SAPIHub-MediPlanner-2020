import os
import glob
import shutil
import codecs
import pickle
import sys
import numpy

from ann_model import AnnProcessor

from age_sex_importer import AgeSexImporter

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, BaggingClassifier

from sklearn.neighbors import KNeighborsClassifier

from sklearn.tree import DecisionTreeClassifier

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import CategoricalNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import ComplementNB

from sklearn.linear_model import SGDClassifier

from sklearn.neural_network import MLPClassifier

from sklearn.svm import LinearSVC

from sklearn.pipeline import Pipeline

def open_source_dataset(dataset_source_filename):
	dataset = open(dataset_source_filename, "r")
	x = []
	y = []
	lines = dataset.readlines()
	dataset.close()
	print('Source dataset line count = ' + str(len(lines)))
	for line in lines:
		#print('Line: ' + str(line))
		sline = line.split(';')
		#print('Source line: ' + str(sline))

		try:
			s0 = sline[0]
			s1 = sline[1]
			x.append(s0)
			y.append(s1)
		except IndexError:
			print('open_source_dataset(): Index error with ' + str(sline) + '')

	return (x, y)

def open_status_dataset_1(dataset_status_filename):
	dataset = open(dataset_status_filename, "r")
	x = []
	y = []
	lines = dataset.readlines()
	dataset.close()
	print('Status dataset #1 line count = ' + str(len(lines)))
	for line in lines:
		sline = line.split(';')
		try:
			#icd_1 = int(sline[2]) * 10000
			#icd_2 = icd_1 + int(sline[3]) * 100
			#icd_3 = icd_2 + int(sline[4])
			icd_1 = int(sline[2])
			icd_2 = int(sline[3])
			icd_3 = int(sline[4])

			x.append([
int(sline[0]), 
int(sline[1]), 
icd_1, 
icd_2, 
icd_3, 
int(sline[5]), 
int(sline[6]), 
int(sline[7]), 
int(sline[8]), 
int(sline[9]),
int(sline[10])
])

			y.append(int(sline[11]))
		except ValueError:
			print(str(y))
	return (x, y)

def open_status_dataset_2(dataset_status_filename):
	dataset = open(dataset_status_filename, "r")
	x = []
	y = []
	ycnt = 0
	lines = dataset.readlines()
	dataset.close()
	print('Status dataset #2 line count = ' + str(len(lines)))
	for line in lines:
		#print(dataset_status_filename + ': Line: ' + str(line))
		sline = line.split(';')
		#print('Source line: ' + str(sline))
		try:
			s0 = sline[14]
			s1 = sline[11]
			
			if int(s1) > 0:
				ycnt += 1

			x.append(s0)
			y.append(s1)

			#print(s0 + " - " + s1)
		except IndexError:
			print('open_status_dataset_2(): Index error with ' + str(sline) + '')

		#print("Non-zero entites count: " + str(ycnt))

	return (x, y)

def open_status_dataset_3(dataset_status_filename):

	dataset = open(dataset_status_filename, "r")
	x = []
	y = []
	ycnt = 0
	lines = dataset.readlines()
	dataset.close()
	print('Status dataset #3 line count = ' + str(len(lines)))
	for line in lines:
		#print(dataset_status_filename + ': Line: ' + str(line))
		sline = line.split(';')
		#print('Source line: ' + str(sline))
		try:
			s0 = sline[15]
			s1 = sline[11]
			
			if int(s1) > 0:
				ycnt += 1

			x.append(s0)
			y.append(s1)

			#print(s0 + " - " + s1)
		except IndexError:
			print('open_status_dataset_3(): Index error with ' + str(sline) + '')

		#print("Non-zero entites count: " + str(ycnt))

	return (x, y)

def train_status(dataset_status_filename_1, dataset_status_filename_2, status_rfc_filename, status_bc_filename, status_date_bc_filename):
	
	print('Opening status dataset #1: ' + dataset_status_filename_1 + '...')
	x, y = open_status_dataset_1(dataset_status_filename_1)
	print('Status dataset #1 loaded.')

	#rfc = BaggingClassifier(n_estimators=50) 
	#rfc = KNeighborsClassifier()
	rfc = RandomForestClassifier(n_estimators=100) #, criterion="entropy") 
	#rfc = MLPClassifier()
	#Low result: rfc = DecisionTreeClassifier()
	#rfc = LinearSVC()

	# 100, no entropy - OK=78 NOK=244

		# Overall attribute accuracy:	0.2422
		# Attribute accuracy
		# Average per attribute type:
		# 	Status	Source
		# 	0.4816	0.1188


	# 25, no entropy - OK=83 NOK=245
		# Overall attribute accuracy:	0.2530
		# Attribute accuracy
		# Average per attribute type:
		# Status	Source
		# 0.4968	0.1188

	#rfc = ExtraTreesClassifier(n_estimators=50, criterion="entropy")

	print('Fitting classifier #1 to dataset...')
	rfc = rfc.fit(x, y)
	print('Status classifier #1 fitted to dataset.')
	scores = rfc.score(x, y)
	print('Score of status dataset #1 is ' + str(scores))
	pickle.dump(rfc, open(status_rfc_filename, 'wb'))

	########################################################################

	print('Opening status dataset #2: ' + dataset_status_filename_1 + '...')
	x2, y2 = open_status_dataset_2(dataset_status_filename_1)
	print('Status dataset #2 loaded.')

	bc = Pipeline([('v', CountVectorizer()), ('c', LinearSVC())]) # 

	print('Fitting classifier #2 to dataset...')
	bc = bc.fit(x2, y2)
	print('Status classifier #2 fitted to dataset.')
	scores = bc.score(x2, y2)
	print('Score of status dataset #2 is ' + str(scores))
	pickle.dump(bc, open(status_bc_filename, 'wb'))

	########################################################################

	print('Opening status dataset #3: ' + dataset_status_filename_1 + '...')
	x3, y3 = open_status_dataset_3(dataset_status_filename_1)
	print('Status dataset #3 loaded.')

	bc = Pipeline([('v', CountVectorizer()), ('c', LinearSVC())]) # 

	print('Fitting classifier #3 to dataset...')
	bc = bc.fit(x3, y3)
	print('Status classifier #3 fitted to dataset.')
	scores = bc.score(x3, y3)
	print('Score of status dataset #3 is ' + str(scores))
	pickle.dump(bc, open(status_date_bc_filename, 'wb'))

def train_source(dataset_source_filename, bc_filename):

	print('Opening source dataset ' + dataset_source_filename + '...')
	x, y = open_source_dataset(dataset_source_filename)
	print('Source dataset loaded.')

	bc = Pipeline([('v', CountVectorizer()), ('c', LinearSVC())]) # OK 80 / NOK 230
	#bc = Pipeline([('v', CountVectorizer()),  ('t', TfidfTransformer()), ('c', LinearSVC())]) # 
	#bc = Pipeline([('v', CountVectorizer()), ('t', TfidfTransformer()), ('c', LinearSVC())]) 
	#bc = Pipeline([('v', CountVectorizer()), ('t', TfidfTransformer()), ('c', ComplementNB())]) 
	#bc = Pipeline([('v', CountVectorizer()), ('t', TfidfTransformer()), ('c', MLPClassifier(hidden_layer_sizes=10))]) 
	#bc = Pipeline([('v', CountVectorizer()), ('t', TfidfTransformer()), ('c', RandomForestClassifier())]) 
	#bc = Pipeline([('v', CountVectorizer()), ('t', TfidfTransformer()), ('c', MultinomialNB())]) 
	#bc = Pipeline([('v', CountVectorizer()), ('t', TfidfTransformer()), ('c', SGDClassifier())]) 
	
	print('Fitting classifier to dataset...')
	bc.fit(x, y)
	print('Source classifier fitted to dataset.')
	scores = bc.score(x, y)
	print('Score of source dataset is ' + str(scores))
	pickle.dump(bc, open(bc_filename, 'wb'))

def classify_source(bc_filename, dataset_source_filename):

	bc = pickle.load(open(bc_filename, 'rb'))
	x_test, y_test = open_source_dataset(dataset_source_filename)
	#result = bc.score(x_test, y_test)

	print('Classyfing source...')

	ycnt = 0
	ycnt2 = 0
	ysum = 0
	i = 0
	for x0 in x_test:
		y0 = y_test[i]
		i += 1
		if i % 1000 == 0: 
			print('Classifying item #' + str(i))

		y1 = bc.predict([x0])
		#print (str(x0) + " - " + str(y0) + " -> predicted " + str(y1))
		if y0 == 'Declared' or y1[0] == 'Declared': 
			ycnt2 += 1
		if y0 == 'Declared': 
			ycnt += 1
			if y1[0] == 'Declared': # Good prediction - goes to sum
				ysum += 1

	print(str(ysum) + " - " + str(ycnt2))
	print('Source (declaration) classification result is ' + str(float(ysum) / float(ycnt2)))


def classify_status(rfc_filename, bc_filename, dataset_status_filename, date_bc_filename):

	rfc = pickle.load(open(rfc_filename, 'rb'))
	x_test, y_test = open_status_dataset_1(dataset_status_filename)
	#result = rfc.score(x_test, y_test)
	
	bc = pickle.load(open(bc_filename, 'rb'))
	x_test_2, y_test_2 = open_status_dataset_2(dataset_status_filename)

	#print(str(x_test_2))

	print('Classyfing status...')

	significance_ycnt = 0
	significance_sum = 0
	family_ycnt = 0
	family_sum = 0
	i = 0

	mode = 1

	# mode 1 (RFC 25)  - 0.865
	# mode 1 (RFC 100) - 0.868
	# mode 2 (SVM)     - 0.811

	if mode == 1:
		for x0 in x_test:
			y0 = int(y_test[i])
			i += 1
			if i % 1000 == 0: 
				print('Classifying item #' + str(i))

			y1 = rfc.predict([x0])
			#y1 = int(bc.predict([x0])[0])
			#if int(y0) > 0: print (str(x0) + " - " + str(y0) + " - " + str(y1))

			if y0 == 1 or y1 == 1: 
				significance_ycnt += 1
			if y0 == 1 and y1 == 1: # Good prediction - goes to sum
				significance_sum += 1

			if y0 == 2 or y1 == 2: 
				family_ycnt += 1
			if y0 == 2 and y1 == 2: # Good prediction - goes to sum
				family_sum += 1
	else:
		for x0 in x_test_2:
			y0 = int(y_test_2[i])
			i += 1
			if i % 1000 == 0: 
				print('Classifying item #' + str(i))

			y1 = int(bc.predict([x0])[0])
			#if int(y0) > 0: print (str(x0) + " - " + str(y0) + " - " + str(y1))

			if y0 == 1 or y1 == 1: 
				significance_ycnt += 1
			if y0 == 1 and y1 == 1: # Good prediction - goes to sum
				significance_sum += 1

			if y0 == 2 or y1 == 2: 
				family_ycnt += 1
			if y0 == 2 and y1 == 2: # Good prediction - goes to sum
				family_sum += 1

	if significance_ycnt == 0: significance_ycnt = 1
	print('Status (significance) counters: ' + str(significance_sum) + " - " + str(significance_ycnt))
	print('Status (significance) classification result is ' + str(float(significance_sum) / float(significance_ycnt)))
	
	if family_ycnt == 0: family_ycnt = 1
	print('Status (family) counters: ' + str(family_sum) + " - " + str(family_ycnt))
	print('Status (family) classification result is ' + str(float(family_sum) / float(family_ycnt)))


def create_datasets(ann_dir, dataset_source_filename, dataset_status_filename_1, dataset_status_filename_2):
    
    print('Creating datasets...')
    AnnProcessor("train", ann_dir, "", "", "", "", dataset_source_filename, dataset_status_filename_1, dataset_status_filename_2) 
    # >>> "train" is mode, not directory
    print('Datasets created.')

def strip_annotations(ann_dir):

   	print('Stripping annotations in [' + ann_dir + ']...')

   	os.chdir(ann_dir)
   	l = glob.glob('*.ann')   
   	for filename in l:
   		print('Stripping ' + filename + '...')
   		f = codecs.open(filename, 'r', 'utf-8')
   		lines = f.readlines()
   		f.close()
   		f = codecs.open(filename, 'w', 'utf-8')
   		for line in lines:
   			if not line[0] == 'A':
   				f.write(line)
   		f.close()
   	os.chdir("..")

   	print('Annotations stripped.')

def find_and_copy_declared_files(from_dir): 

    print('Starting ...')

    os.chdir(from_dir)
    l = glob.glob('*.ann')   
    for filename in l:
        f = codecs.open(filename, 'r', 'utf-8')
        s = f.read()
        f.close()
        
        pos = s.find('Declared')

        if pos > -1:
            print('Declared found. Copying ' + filename + '...')
            shutil.copyfile(filename, 'declared/' + filename)
            fname, fext = os.path.splitext(filename)
            txt_filename = fname + '.txt'
            shutil.copyfile(txt_filename, 'declared/' + txt_filename)
    
    print('Finished.')

def find_and_copy_family_files(from_dir):    
       
    print('Starting ...')
    os.chdir(from_dir)
    l = glob.glob('*.txt')   
    for filename in l:
        print(filename + "...")
        
        start, end = AgeSexImporter.extract_family_record(filename)
        
        if start > 0:
            print('Family info found. Copying ' + filename + '...')
            shutil.copyfile(filename, 'family/' + filename)
            fname, fext = os.path.splitext(filename)
            ann_filename = fname + '.ann'
            shutil.copyfile(ann_filename, 'family/' + ann_filename)
    
    print('Finished.')
            
def annotate(dir, status_rfc_filename, status_bc_filename, status_bc_date_filename, source_bc_filename, dataset_source_filename, dataset_status_filename_1, dataset_status_filename_2):	

    AnnProcessor("annotate", dir, status_rfc_filename, status_bc_filename, status_bc_date_filename, source_bc_filename, dataset_source_filename, dataset_status_filename_1, dataset_status_filename_2) 

def test(dir):

	annotate(dir, "rfc.sav", "bc.sav", "bc_date.sav")

def test2():
	
	create_datasets("new_train_test_orig", "dataset_in_source.txt", "dataset_in_status_1.txt", "dataset_in_status_2.txt")
			
	train_status("dataset_in_status_1.txt", "dataset_in_status_1.txt", "status_rfc.sav", "status_bc.sav", "status_bc_date.sav")
	train_source("dataset_in_source.txt", "source_bc.sav")
		
	#-------------------------------------------------------

	# Errors: creation based on files without annotations :( :), so result in classify was 0.0
	create_datasets("new_train_test_orig", "dataset_test_source.txt", "dataset_test_status_1.txt", "dataset_test_status_2.txt")

	classify_status("status_rfc.sav", "status_bc.sav", "status_bc_date.sav", "dataset_test_status_1.txt")
	classify_source("source_bc.sav", "dataset_test_source.txt")
	
	#strip_annotations("declared")
	#create_datasets("p", "dataset_test_source.txt", "dataset_test_status_1.txt", "dataset_test_status_2.txt")
	#annotate("declared", "status_rfc.sav", "status_bc.sav" "source_bc.sav", "dataset_test_source.txt", "dataset_test_status_1.txt", "dataset_test_status_2.txt")

#find_and_copy_family_files("train")
#find_and_copy_declared_files('train')
#test("family")
#test2()
#strip_annotations('declared')

if __name__ == "__main__":
	cnt = len(sys.argv)
	if cnt == 2:
		mode = sys.argv[1]
		if mode == "test":
			test(dir)
		elif mode == "test2":
			test2()
	elif cnt == 3:
		mode = sys.argv[1]
		dir  = sys.argv[2]
		if mode == "-s":
			strip_annotations(dir)
		elif mode == "-t":
			create_datasets(dir, "dataset_in_source.txt", "dataset_in_status_1.txt", "dataset_in_status_2.txt")
			train_status("dataset_in_status_1.txt", "dataset_in_status_1.txt", "status_rfc.sav", "status_bc.sav", "status_bc_date.sav")
			train_source("dataset_in_source.txt", "source_bc.sav")
		elif mode == "-a":
			annotate(dir, "status_rfc.sav", "status_bc.sav", "status_bc_date.sav", "source_bc.sav", "dataset_test_source.txt", "dataset_test_status_1.txt", "dataset_test_status_2.txt")



# 366, 647 without T type