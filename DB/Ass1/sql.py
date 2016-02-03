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

	def execute(self, existing_records, existing_tables):
		if(bool(self.agg) and bool(self.colnames)):
			print('Not same number of rows')
			return -1
		
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
		self.work_with_where(existing_tables, existing_records)
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

		return records

	def work_with_where(self, existing_tables, existing_records):
		indexes = dict()
		val = 0
		op = 0
		for table in self.tables['where'].keys():
			if(table not in indexes.keys()):
				indexes[table] = dict()
			for cols in self.tables['where'][table].keys():
				flag = 0
				if(cols not in indexes[table].keys()):
					indexes[table][cols] = list()
				for i in xrange(len(self.tables['where'][table][cols])):
					if(i % 2 == 0):
						#print self.tables['where'][table][cols][i]
						if(len(self.tables['where'][table][cols][i]) > 1):
							if(self.tables['where'][table][cols][i][1:].isdigit()):
								flag = 1
						else:
							if(self.tables['where'][table][cols][i].isdigit()):
								flag = 1
						if(flag == 1):
							#print 'yeah'
							val = self.tables['where'][table][cols][i]
							val = int(val)
					else:
						op = self.tables['where'][table][cols][i]
						#print existing_records[table][cols]
						if(op == '='):
							indexes[table][cols].append(list(np.where(np.array(existing_records[table][cols]) == val)))
						elif(op == '>'):
							indexes[table][cols].append(list(np.where(np.array(existing_records[table][cols]) > val)))
						elif(op == '>='):
							indexes[table][cols].append(list(np.where(np.array(existing_records[table][cols]) >= val)))
						elif(op == '<'):
							indexes[table][cols].append(list(np.where(np.array(existing_records[table][cols]) < val)))
						elif(op == '<='):
							indexes[table][cols].append(list(np.where(np.array(existing_records[table][cols]) <= val)))
						
		
		# if(self.oper is not None):
				
		# print indexes

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
		self.oper = None
		self.create = dict()
		self.insert = dict()
		self.delete = dict()
		self.drop = None
		self.truncate = None

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
			elif(self.type == 'insert'):
				if(len(query_vars) != 4):
					print 'Incomplete Statement'
					return -1
				if(query_vars[1].lower() != 'into'):
					print "Error"
					return -1
				if(query_vars[3][:6].lower() != 'values'):
					print "Error1"
					return -1
				if(self.check_insert(query_vars) == -1):
					return -1

			elif(self.type == 'delete'):
				if(query_vars[1].lower() != 'from'):
					print "Error"
					return -1
				if(query_vars[3].lower() != 'where'):
					print "Error"
					return -1
				if(self.check_delete(query_vars[2:]) == -1):
					return -1

			elif(self.type == 'drop'):
				if(query_vars[1].lower() != 'table'):
					print "Error"
					return -1
				if(self.check_drop(query_vars[2], 1) == -1):
					return -1

			elif(self.type == 'truncate'):
				if(query_vars[1].lower() != 'table'):
					print "Error"
					return -1
				if(self.check_drop(query_vars[2], 2) == -1):
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

	def check_colnames(self, query_vars, from_index, index_where, existing_tables):
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

		if(index_where is not None):
			leg_opers = [ '<=', '<', '>=', '>', '=']
			i = index_where + 1
			query_vars = query_vars[i:]
			end_index = len(query_vars)
			if('and' in map(str.lower,query_vars)):
				index_op = map(str.lower,query_vars).index('and')
				self.oper = query_vars[index_op]
			elif('or' in map(str.lower,query_vars)):
				index_op = map(str.lower,query_vars).index('or')
				self.oper = query_vars[index_op]
			
			new_vars = ''.join(query_vars).split(self.oper)
			if(self.oper):
				if(len(new_vars) < 2):
					print 'Invalid'
					return -1
		
			for var in new_vars:
				val = map(var.find, leg_opers)
				for o in xrange(len(val)):
					if(val[o] != -1):
						break

				if(o+1 == 6):
					print('no valid operator found')
					return -1

				log_oper = leg_opers[o]
				actual_vars = var.split(log_oper)
				if(len(actual_vars) != 2):
					print("invalid")
					return -1
				for p in xrange(2):
					if(p == 0):
						dot_split = actual_vars[p].split('.')
						if(len(dot_split) == 2):
							if(dot_split[0] in self.tables['sel']):
								if(dot_split[0] not in self.tables['where'].keys()):
									self.tables['where'][dot_split[0]] = dict()
							else:
								print 'invalid table name'
								return -1
							if(dot_split[1] in existing_tables[dot_split[0]]):
								table_name = dot_split[0]
								col_name = dot_split[1]
								self.tables['where'][dot_split[0]][dot_split[1]] = list()
							else:
								print 'invalid column name'
								return -1
						else:
							flag = 0 
							for table in self.tables['sel']:
								if(dot_split[0] in existing_tables[table]):
									if(table not in self.tables['where'].keys()):
										self.tables['where'][table] = dict()
									if(dot_split[0] not in self.tables['where'][table].keys()):
										self.tables['where'][table][dot_split[0]] = list()
									flag = 1
									table_name = table
									col_name = dot_split[0]
									break
							if(flag == 0):
								print 'invalid column name'
								return -1
					else:
						self.tables['where'][table_name][col_name].append(actual_vars[p])
						self.tables['where'][table_name][col_name].append(log_oper)


		#print self.tables['where']	

			# if(i == end_index):
			# 	print 'Incomplete where clause'
			# 	return -1
			# while(i < end_index):
			# 	val = query_vars[i]
			# 	if(val == )
			# 	dot_sep = val.split('.')

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
		self.tables['where'] = dict()
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

			
		if(self.check_colnames(query_vars, index_from, index_where, existing_tables) == -1):
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

	def check_insert(self, query_vars):
		existing_tables = find_existing_tables()
		table_name = None
		if(query_vars[2] in existing_tables.keys()):
			self.insert[query_vars[2]] = dict()
			table_name = query_vars[2]
		else:
			print "Wrong table name"
			return -1
		if(query_vars[3][6] == '(' and query_vars[3][-1] == ')'):   #values()
			query_vars[3] = query_vars[3].replace('values(','')
			query_vars[3] = query_vars[3].replace(')','')
			comma_sep = query_vars[3].split(',')
			if(query_vars[3].find('=') == - 1):				
				if(len(comma_sep) == len(existing_tables[table_name])):
					columns = existing_tables[table_name]
					for i in xrange(len(existing_tables[table_name])):
						self.insert[table_name][columns[i]] = comma_sep[i]
				else:
					print len(comma_sep),len(existing_tables[table_name]) 
					print 'Column count does not match'
					return -1
			else:
				for i in comma_sep:
					val = i.split('=')
					if(len(val) == 2):
						if(val[0] in existing_tables[table_name]):
							self.insert[table_name][val[0]] = val[1]
						else:
							print 'invalid column name'
							return -1
					else:
						print 'invalid'
						return -1

		else:
			print 'invalid Statement'
			return -1

	def check_delete(self, query_vars):
		table_name = query_vars[0]
		existing_tables = find_existing_tables()
		if(table_name in existing_tables.keys()):
			self.delete[table_name] = dict()
			if(query_vars[2] in existing_tables[table_name]):
				self.delete[table_name][query_vars[2]] = query_vars[4]
			else:
				print 'Invalid col_name'
				return -1
		else:
			print 'invalid table name'
			return -1

	def check_drop(self, table_name, val):
		existing_tables = find_existing_tables()
		if(table_name in existing_tables.keys()):
			if(val == 1):
				self.drop = table_name
			else:
				self.truncate = table_name
			
		else:
			print 'invalid table_name'
			return -1

class Create(object):
	def __init__(self, create_dic):
		self.create_dic = create_dic
	def execute(self, existing_records, existing_tables):
		Dir = 'SampleDataset-Assignment 1'
		table_name = self.create_dic.keys()[0]
		colnames = self.create_dic[table_name].keys()
		existing_tables[table_name] = colnames
		existing_records[table_name] = dict()
		for c in colnames:
			existing_records[table_name][c] = list()
		with open(os.path.join(Dir,'metadata.txt'), 'a') as meta:
			meta.write('\r\n')
			meta.write('<begin_table>\r\n')
			meta.write(table_name + '\r\n')
			for i in colnames:
				meta.write(i + '\r\n')
			meta.write('<end_table>')
		with open(os.path.join(Dir,table_name + '.csv'), 'w') as f:
			w = csv.writer(f)

class Insert(object):
	def __init__(self, insert_dict):
		self.insert_dict = insert_dict
	def execute(self, existing_records, existing_tables):
		table_name = self.insert_dict.keys()[0]
		col_names = self.insert_dict[table_name].keys()
		for col in col_names:
			existing_records[table_name][col].append(int(self.insert_dict[table_name][col]))
		self.insert_csv(existing_tables)

	def insert_csv(self, existing_tables):
		Dir = 'SampleDataset-Assignment 1'
		table_name = self.insert_dict.keys()[0]
		col_names = self.insert_dict[table_name].keys()
		row = list()
		for cols in existing_tables[table_name]:
			if(cols in col_names):
				row.append(self.insert_dict[table_name][cols]) 
			else:
				row.append(0)
		with open(os.path.join(Dir, table_name) + '.csv', 'ab') as csvfile :
			writer = csv.writer(csvfile)
			writer.writerow(row)
		
class Delete(object):
	def __init__(self, del_dict):
		self.delete_dict = del_dict
	def execute(self, existing_records, existing_tables):
		table_name = self.delete_dict.keys()[0]
		col_name = self.delete_dict[table_name].keys()[0]
		val = self.delete_dict[table_name][col_name]
		if(int(val) in existing_records[table_name][col_name]):
			index = existing_records[table_name][col_name].index(int(val))
		else:
			return
		for col in existing_records[table_name].keys():
			existing_records[table_name][col].remove(existing_records[table_name][col][index])
		self.delete_csv(existing_tables)

	def delete_csv(self, existing_tables):
		Dir = 'SampleDataset-Assignment 1'
		table_name = self.delete_dict.keys()[0]
		col_name = self.delete_dict[table_name].keys()[0]
		row = list()
		stop_ind = -1
		count = 0
		row_write = list()
		val = self.delete_dict[table_name][col_name]
		with open(os.path.join(Dir, table_name) + '.csv', 'rb') as csvfile :
			reader = csv.reader(csvfile)
			for row in reader:
				for j in xrange(len(existing_tables[table_name])):
					if(existing_tables[table_name][j] == col_name):
						if(row[j] == val):
							stop_ind = count
							continue
				if(stop_ind == count):
					stop_ind = -1
					continue
				row_write.append(row)
				count += 1
		with open(os.path.join(Dir, table_name) + '.csv', 'wb') as csvfile :
			writer = csv.writer(csvfile)
			writer.writerows(row_write)

class Truncate(object):
	def __init__(self, tab):
		self.table_name = tab

	def execute(self, existing_records):
		Dir = 'SampleDataset-Assignment 1'
		table_name = self.table_name
		cols = existing_records[table_name].keys()
		for col in cols:
			existing_records[table_name][col] = []
		with open(os.path.join(Dir, table_name) + '.csv', 'wb') as csvfile :
			w = csv.writer(csvfile)

class Drop(object):
	def __init__(self, tab):
		self.table_name = tab

	def execute(self, existing_records, existing_tables):
		Dir = 'SampleDataset-Assignment 1'
		table_name = self.table_name
		cols = existing_records[table_name].keys()
		count = 0
		for col in cols:
			if(len(existing_records[table_name][col]) == 0):
				count += 1
		if(count == len(cols)):
			existing_records.pop(table_name)
			with open(os.path.join(Dir,'metadata.txt'), 'w') as meta:
				for table in existing_records.keys()[:-1]:
					meta.write('<begin_table>\r\n')
					meta.write(table + '\r\n')
					colnames = existing_tables[table]
					for i in colnames:
						meta.write(i + '\r\n')
					meta.write('<end_table>\n')
				meta.write('<begin_table>\r\n')
				meta.write(existing_records.keys()[-1] + '\r\n')
				colnames = existing_tables[existing_records.keys()[-1]]
				for i in colnames:
					meta.write(i + '\r\n')
				meta.write('<end_table>')
			os.remove(os.path.join(Dir, table_name) + '.csv')
		else:
			print 'can\'t truncate'
			return

def main():
	records = get_records()
	print records
	existing_tables = find_existing_tables()
	while(1):
		sql_ob = sql_parser(raw_input())
		status = sql_ob.parse()
		if(status == -1):
			continue
		type =  sql_ob.type
		if(type == 'select'):
			sel_obj = Select(sql_ob.colnames, sql_ob.agg, sql_ob.tables)
			status = sel_obj.execute(records, existing_tables)
			if(status == -1):
				continue
		elif(type == 'create'):
			create_ob = Create(sql_ob.create)
			create_ob.execute(records, existing_tables)
			print existing_tables
		elif(type == 'insert'):
			insert_ob = Insert(sql_ob.insert)
			insert_ob.execute(records, existing_tables)
			print records
		elif(type == 'delete'):
			del_ob = Delete(sql_ob.delete)
			del_ob.execute(records, existing_tables)
			print records
		elif(type == 'truncate'):
			truncate_ob = Truncate(sql_ob.truncate)
			truncate_ob.execute(records)
			print records
		elif(type == 'drop'):
			print sql_ob.drop
			drop_ob = Drop(sql_ob.drop)
			drop_ob.execute(records, existing_tables)
			print records

if(__name__ == '__main__'):
	main()