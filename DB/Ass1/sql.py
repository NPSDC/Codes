import sqlparse as sp
import csv
import numpy as np
import os

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

	def execute(self):
		if(bool(self.agg) and bool(self.colnames)):
			print('Not same number of rows')
			return -1
		existing_tables = find_existing_tables()

		if(bool(self.colnames)):
			cols_indexes = self.find_col_indexes(existing_tables)
			records = self.create_record(cols_indexes, existing_tables, 1)
			self.display(records)
		else:
			agg_indexes = self.find_agg_indexes(existing_tables)
			records = self.create_record(agg_indexes, existing_tables, 2)
			self.display(records)
		
	def create_record(self, cols, existing_tables, type):
		Dir = 'SampleDataset-Assignment 1'
		records = dict()
		if(type == 1):
			records = self.create_record_more(cols, existing_tables, Dir)
		if(type == 2):
			new_rec = dict()
		 	for funcs in cols.keys():
		 		records[funcs] = self.create_record_more(cols[funcs], existing_tables, Dir)
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

	def create_record_more(self, cols, existing_tables, Dir):
		records = dict()
		for table in cols.keys():
			for col in cols[table]:
				if(existing_tables[table][col] not in records.keys()):
					records[existing_tables[table][col]] = list()
			table_name = table + '.csv'
	
			with open(os.path.join(Dir, table_name), 'rb') as csvfile :
				reader = csv.reader(csvfile)
				for row in reader:
					for col in cols[table]:
						records[existing_tables[table][col]].append(int(row[col]))
	
		return records

	def max(self, records, new_dict):
		for col in records.keys():
			ans = max(records[col])
			key = 'max('+col+')'
			new_dict[key] =  list()
			new_dict[key].append(ans)
		return new_dict

	def min(self, records, new_dict):
		for col in records.keys():
			ans = min(records[col])
			key = 'min('+col+')'
			new_dict[key] =  list()
			new_dict[key].append(ans)
		return new_dict

	def avg(self, records, new_dict):
		for col in records.keys():
			ans = float(sum(records[col]))/float(len(records[col]))
			key = 'avg('+col+')'
			new_dict[key] =  list()
			new_dict[key].append(ans)
		return new_dict		

	def sum(self, records, new_dict):
		for col in records.keys():
			ans = sum(records[col])
			key = 'sum('+col+')'
			new_dict[key] =  list()
			new_dict[key].append(ans)
		return new_dict

	def distinct(self, records, new_dict):
		for col in records.keys():
			ans = np.unique(records[col])
			key = 'min('+col+')'
			new_dict[key] =  list(ans)
		return new_dict

	def display(self, records):
		length = len(records[records.keys()[0]])
		for i in records.keys():
			if(len(records[i]) != length):
				print 'invalid'
				return -1
			print i + '\t',
		print('\n')
		for j in xrange(length):
			for i in records.keys():
				print str(records[i][j]) + '\t',
			print('\n')
		print('Total '+str(length)+' rows')
class sql_parser(object):
	def __init__(self, sql_query):
		self.sql_query = sql_query
		self.type = list()
		self.colnames =dict() #{table:[colname]}
		self.agg = dict() # {function:[{table:[colname]}]}
		self.tables = dict()

	def parse(self):
		query = self.sql_query
		if(query[len(query) - 1] == ';'):
			query = query[:len(query) - 1]
			query_vars = query.split()
			if(self.check_type(query_vars[0]) == -1):
				return
			# if(self.check_colnames(query_vars) == -1):
			# 	return
			# self.check_agg(query_vars)
			if(self.check_tables(query_vars) == -1):
				return
			# print(self.colnames)
			# print(self.agg)
			# print(self.tables)

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


def main():
	while(1):
		sql_ob = sql_parser(raw_input())
		status = sql_ob.parse()
		if(status == -1):
			continue
		type =  sql_ob.type
		if(type == 'select'):
			sel_obj = Select(sql_ob.colnames, sql_ob.agg, sql_ob.tables)
			status = sel_obj.execute()
			if(status == -1):
				continue

if(__name__ == '__main__'):
	main()