import sqlparse as sp
import csv
import numpy as np
import os
import itertools

def find_existing_tables():
	f = open('SampleDataset-Assignment 1/metadata.txt')
	content = f.readlines()
	f.close()
	tables_dict = {}
	content = map(str.split, content)
	content = list(np.array(content).flatten())
	flag_table = 0
	flag_col = 0
	for i in xrange(len(content)):
		if(content[i] == '<begin_table>'):
			flag_table = 1
			flag_col = 0
			continue
	
		if(content[i] == '<end_table>'):
			flag_col = 0
			continue

		if(flag_table == 1):
			table_name = content[i] 
			tables_dict[table_name] = []
			flag_col = 1
			flag_table = 0
			continue

		if(flag_col == 1):
			tables_dict[table_name].append(content[i])
			continue
	
	return tables_dict

def get_records():
	tables_dict = find_existing_tables()	
	Dir = 'SampleDataset-Assignment 1'
	records = dict()
	for table in tables_dict.keys():
		records[table] = dict()
		for col in tables_dict[table]:
			records[table][col] = list()
		table_name = table + '.csv'
		j = 0
		with open(os.path.join(Dir, table_name), 'rb') as csvfile :
			reader = csv.reader(csvfile)
			for row in reader:
				for j in xrange(len(records[table])):
					records[table][tables_dict[table][j]].append(int(row[j]))
					
			
	return records

class Select(object):
	def __init__(self, sel_colnames, sel_agg, sel_tables):
		self.colnames = sel_colnames
		self.agg = sel_agg
		self.tables = sel_tables

	def find_indexes(self, cols, existing_tables):
		cols_indexes = dict()
		for table in existing_tables.keys():
			if(table in cols.keys()):
				cols_indexes[table] = list()
				for c in xrange(len(existing_tables[table])):
					for col in cols[table]:
						if(col == existing_tables[table][c]):
							cols_indexes[table].append(c)
							break
		return cols_indexes

	def find_col_indexes(self, existing_tables):
		cols_indexes = self.find_indexes(self.colnames, existing_tables)
		return cols_indexes

	def find_agg_indexes(self, existing_tables):
		agg_indexes = dict()
		for func in self.agg.keys():
			agg_indexes[func] = self.find_indexes(self.agg[func], existing_tables)
		return agg_indexes

	def execute(self, existing_records):
		if(bool(self.agg) and bool(self.colnames)):
			print('Not same number of rows')
			return -1
		existing_tables = find_existing_tables()

		if(bool(self.colnames)):
			cols_indexes = self.find_col_indexes(existing_tables)
			records = self.create_record(cols_indexes, existing_tables, existing_records, 1)
			self.display(records)
		else:
			agg_indexes = self.find_agg_indexes(existing_tables)
			records = self.create_record(agg_indexes, existing_tables, existing_records, 2)
			#print records
			self.display(records)
		
	def create_record(self, cols, existing_tables, existing_records, type):
		records = dict()
		if(type == 1):
			records = self.create_record_more(cols, existing_tables, existing_records)
			#records = self.create_record_more(cols, existing_tables, Dir)
		if(type == 2):
			new_rec = dict()
		 	for funcs in cols.keys():
		 		records[funcs] = self.create_record_more(cols[funcs], existing_tables, existing_records)
		 		new_rec = self.get_agg(funcs.lower(), records[funcs], new_rec)
			records = new_rec
		return records

	def get_agg(self, key, rec, new_rec):
		if(key == 'max'):
			new_rec = self.max(rec, new_rec)
		if(key == 'min'):
			new_rec = self.min(rec, new_rec)
		if(key == 'avg'):
			new_rec = self.avg(rec, new_rec)
		if(key == 'sum'):
			new_rec = self.sum(rec, new_rec)
		if(key == 'distinct'):
			new_rec = self.distinct(rec, new_rec)
		return new_rec

	def create_record_more(self, cols, existing_tables, existing_records):
		records = dict()
		lengths = list()
	
		existing_records_used = dict()
		for table in cols.keys():
			if(table not in existing_records_used.keys()):
				existing_records_used[table] = dict()
			if(table not in records.keys()):
				records[table] = dict()
			for col in cols[table]:
				existing_records_used[table][existing_tables[table][col]] = existing_records[table][existing_tables[table][col]]
				if(existing_tables[table][col] not in records.keys()):
					records[table][existing_tables[table][col]] = list()
				else:
					records[table][existing_tables[table][table+'.'+col]] = list()
		#print records
		#print existing_records_used
		for table in existing_records_used.keys():
			k = existing_records_used[table].keys()[0]
			lengths.append(len(existing_records[table][k]))

		indexes = list(itertools.product(*(map(range, lengths))))		
		for i in indexes:
			for j in xrange(len(i)):
				for	table in existing_records_used.keys():
					if(table == records.keys()[j]):
						for column in records[table]:
							records[table][column].append(existing_records_used[table][column][i[j]])
		#print records

		# 	with open(os.path.join(Dir, table_name), 'rb') as csvfile :
		# 		reader = csv.reader(csvfile)
		# 		for row in reader:
		# 			for col in cols[table]:
		# 				records[existing_tables[table][col]].append(int(row[col]))
	
		return records

	def max(self, records, new_dict):
		for table in records.keys():
			if(table not in new_dict.keys()):
				new_dict[table] = dict()

			for col in records[table].keys():
				key = 'max('+col+')'
				new_dict[table][key] =  list()
				ans = max(records[table][col])
				new_dict[table][key].append(ans)
		return new_dict

	def min(self, records, new_dict):
		for table in records.keys():
			if(table not in new_dict.keys()):
				new_dict[table] = dict()

			for col in records[table].keys():
				key = 'min('+col+')'
				new_dict[table][key] =  list()
				ans = min(records[table][col])
				new_dict[table][key].append(ans)
		return new_dict

	def avg(self, records, new_dict):
		for table in records.keys():
			if(table not in new_dict.keys()):
				new_dict[table] = dict()
			
			for col in records[table].keys():
				ans = float(sum(records[table][col]))/float(len(records[table][col]))
				key = 'avg('+col+')'
				new_dict[table][key] =  list()
				new_dict[table][key].append(ans)
		return new_dict		

	def sum(self, records, new_dict):
		for table in records.keys():
			if(table not in new_dict.keys()):
				new_dict[table] = dict()
			
			for col in records[table].keys():
				ans = sum(records[table][col])
				key = 'sum('+col+')'
				new_dict[table][key] =  list()
				new_dict[table][key].append(ans)
		return new_dict

	def distinct(self, records, new_dict):
		for table in records.keys():
			if(table not in new_dict.keys()):
				new_dict[table] = dict()
			
			for col in records[table].keys():
				ans = np.unique(records[table][col])
				key = 'distinct('+col+')'
				new_dict[table][key] =  list(ans)
			return new_dict

	def display(self, records):
		length = len(records[records.keys()[0]][records[records.keys()[0]].keys()[0]])
		for i in records.keys():
			for k in records[i].keys():
				if(len(records[i][k]) != length):
					print 'invalid'
					return -1
				print k + '\t',
		print('\n')
		for j in xrange(length):
			for i in records.keys():
				for k in records[i].keys():
					print str(records[i][k][j]) + '\t',
			print('\n')
		print('Total '+str(length)+' rows')
class sql_parser(object):
	def __init__(self, sql_query):
		self.sql_query = sql_query
		self.type = list()
		self.colnames =dict() #{table:[colname]}
		self.agg = dict() # {function:[{table:[colname]}]}
		self.tables = dict()
		self.create = dict()

	def parse(self):
		query = self.sql_query
		if(query[len(query) - 1] == ';'):
			query = query[:- 1]
			query_vars = query.split()
			if(self.check_type(query_vars[0]) == -1):
				return -1
			if(self.type == 'select'):
				if(self.check_tables(query_vars) == -1):
					return -1
			elif(self.type == 'create'):
				if(query_vars[1].lower() != 'table'):
					print "Error"
					return -1
				if(query_vars[-1][-1] != ')'):
					return -1
				if(self.check_create(query_vars[2:]) == -1):
					return -1
				

	def check_type(self, type):
		allowed_commands = ['select', 'insert', 'delete', 'truncate', 'drop', 'create']
		type = type.lower()
		if(type in allowed_commands):
			self.type = type
			return 0
		else:
			print(type + ' is not valid')
			return -1

	def check_colnames(self, query_vars, from_index, existing_tables):
		for i in range(1, from_index):
			var_list = query_vars[i].split(',')
			for j in var_list:
				if(len(j.split('(')) > 1):
					continue
				dot_split = j.split('.')
				if(len(dot_split) == 2 ):
					if(len(dot_split[1]) != 0):
						if(dot_split[0] in self.tables['sel']):
							if(dot_split[0] not in self.colnames.keys()):
								self.colnames[dot_split[0]] = list()
						else:
							print('table '+ dot_split[0] + " does not exist")
							return -1
						if(dot_split[1] in existing_tables[dot_split[0]]):
							self.colnames[dot_split[0]].append(dot_split[1])
						else:
							print('colname '+ dot_split[1] + " does not exist")
							return -1
				else:
					if(len(j) == 0):
						continue
					else:
						if(j == '*'):
							for table in self.tables['sel']:
								self.colnames[table] = existing_tables[table]
						else:
							for table in self.tables['sel']:
								if(j in existing_tables[table]):
									if(table not in self.colnames.keys()):
										self.colnames[table] = list()
									self.colnames[table].append(j)
									break
							else:		
								print('colname '+ j + " does not exist or not chosen after from")
								return -1
		return 0	

	def check_agg(self, query_vars, from_index, existing_tables):
		possible_functions = ['max', 'sum', 'avg', 'min', 'distinct']
		for i in range(1, from_index):
			var_list = query_vars[i].split(',')
			for j in var_list :
				brack_split = j.split('(')
				if(len(brack_split) == 2):
					if(brack_split[0].lower() not in possible_functions):
						print(brack_split[0] + " not apt function")
						return -1
					if(brack_split[1][-1] != ')'):
						print 'invalid ' + '('.join(brack_split)
					else:
						brack_split[1] = brack_split[1][:-1]
						if(brack_split[0] not in self.agg.keys()):
							self.agg[brack_split[0]] = dict()
						dot_split = brack_split[1].split('.')
						if(len(dot_split) == 2):
							if(dot_split[0] in self.tables['sel']):
								if(dot_split[0] not in self.agg[brack_split[0]].keys()):
									self.agg[brack_split[0]][dot_split[0]] = []
								if(dot_split[1] in existing_tables[dot_split[0]]):
									self.agg[brack_split[0]][dot_split[0]].append(dot_split[1])
								else:
									print 'colname ' + dot_split[1] + " not found"
									return -1
							else:
								print('table ' + dot_split[0] + " does not exist")
								return -1

						else:													
							for table in self.tables['sel']:
								if(dot_split[0] in existing_tables[table]):
									if(table not in self.agg[brack_split[0]].keys()):
										self.agg[brack_split[0]][table] = []
									self.agg[brack_split[0]][table].append(dot_split[0])
									break
							else:
								print('colname '+ dot_split[0] + " does not exist or not chosen after from")
								return -1
		return 0						

	def check_tables(self, query_vars):
		index_from = None
		index_where = None
		existing_tables = find_existing_tables()

		try:
			index_from = map(str.lower,query_vars).index('from')
			index_where = map(str.lower,query_vars).index('where')
		except ValueError as e:
			if(index_from is None):
				print('from not there')
				return -1

		i = index_from + 1
		if(index_where is None):
			end_index = len(query_vars)
		else:
			end_index = index_where

		self.tables['sel'] = list()
		while(i < end_index):
			val = query_vars[i]
			val_list = val.split(',')
			for j in val_list:
				if(len(j) > 0):					
					if(j in existing_tables.keys()):
						self.tables['sel'].append(j)
					else:
						print "table name " + j + ' does not exist'
						return -1
			i += 1

		if(self.check_colnames(query_vars, index_from, existing_tables) == -1):
			return -1
		if(self.check_agg(query_vars, index_from, existing_tables) == -1):
			return -1
		return 1

	def check_create(self, query_vars):
		datatypes = ['char', 'varchar', 'boolean', 'decimal', 'int', 'smallint', 'real', 'float', 'date', 'timestamp']	
		vars = ' '.join(query_vars).split('(')
		if(len(vars) != 2):
			print("Error length")
			return -1
		else:
			table_name = vars[0]
			self.create[table_name] = dict()
			new_vars = vars[1].split(',')
			length = len(new_vars)
			for index in xrange(length):
				if(index == length - 1):
					new_vars[index] = new_vars[index][:-1]
				
				temp_vars = new_vars[index].split(' ')
				if(temp_vars[0] == ''):
					temp_vars = temp_vars[1:]
				if(len(temp_vars) == 2):
					col = temp_vars[0]
					if(col in self.create[table_name].keys()):
						print("Col already exists")
						return -1
					else:
						dtype = temp_vars[1]
						if(temp_vars[1].split('(')[0] in datatypes):
							self.create[table_name][col] = dtype
				else:
					print("Error length2")
					return -1
class Create(object):
	def __init__(self, create_dic):
		self.create_dic = create_dic
	def execute(self):
		Dir = 'SampleDataset-Assignment 1'
		table_name = self.create_dic.keys()[0]
		colnames = self.create_dic[table_name].keys()
		with open(os.path.join(Dir,'metadata.txt'), 'a') as meta:
			meta.write('\r\n')
			meta.write('<begin_table>\r\n')
			meta.write(table_name + '\r\n')
			for i in colnames:
				meta.write(i + '\r\n')
			meta.write('<end_table>')
		with open(os.path.join(Dir,table_name + '.csv'), 'w') as f:
			w = csv.writer(f)


def main():
	records = get_records()
	while(1):
		sql_ob = sql_parser(raw_input())
		status = sql_ob.parse()
		if(status == -1):
			continue
		type =  sql_ob.type
		if(type == 'select'):
			sel_obj = Select(sql_ob.colnames, sql_ob.agg, sql_ob.tables)
			status = sel_obj.execute(records)
			if(status == -1):
				continue
		elif(type == 'create'):
			create_ob = Create(sql_ob.create)
			create_ob.execute()

if(__name__ == '__main__'):
	main()