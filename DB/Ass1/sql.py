import sqlparse as sp
import csv
import numpy as np

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
			print(self.colnames)
			print(self.tables)

	def check_type(self, type):
		allowed_commands = ['select', 'insert', 'delete', 'truncate', 'drop', 'create']
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
		possible_functions = ['max', 'sum', 'average', 'min', 'distinct']
		for i in range(1, from_index):
			var_list = query_vars[i].split(',')
			for j in val_list :
				brack_split = j.split('(')
				if(len(brack_split) == 2):
					if(brack_split[0] not in possible_functions):
						print(brack_split[0] + " not apt function")
						return -1
					else:
						if(brack_split[0] not in self.agg.keys()):
							self.agg[brack_split[0]] = dict()
						dot_split = brack_split[1].split('.')
						if(length(dot_split) == 2):
							if(dot_split[0] in self.tables['sel']):
								if(dot_split[0] not in self.agg[brack_split[0]].keys()):
									self.agg[brack_split[0]][dot_split[0]] = []
								self.agg[brack_split[0]][dot_split[0]].append(dot_split[1])
							else:
								print('table ' + dot_split[0] + " does not exist")
								return -1

						else:
							for(table in self.tables['sel']):
								if(dot_split[0] in existing_tables[table])


	def check_tables(self, query_vars):
		index_from = None
		index_where = None
		existing_tables = find_existing_tables()

		try:
			index_from = query_vars.index('from')
			index_where = query_vars.index('where')
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

		return 1


def main():
	while(1):
		sql_ob = sql_parser(raw_input())
		status = sql_ob.parse()
		if(status == -1):
			continue

if(__name__ == '__main__'):
	main()