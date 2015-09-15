Files = {'iris.data', 'car.data',  'wine.data', 'cmc.data'};

f1 = fopen(Files{1});
data = textscan(f1, '%f%f%f%f%s', 'delimiter', ',');
inp_data_iris = data;
fclose(f1);

inp_data_iris = randomize(data);

f2 = fopen(Files{2});
data = textscan(f2, '%s%s%s%s%s%s%s', 'delimiter', ',');
inp_data_car = data;
fclose(f2);

inp_data_car = randomize(data);

f3 = fopen(Files{3});
data = textscan(f2, '%f%f%f%f%f%f%f%f%f%f%f%f%f%f', 'delimiter', ',');
inp_data_wine = data;
fclose(f3);
inp_data_wine = randomize(data);
class_samp_iris = 0;

f4 = fopen(Files{4});
data = textscan(f2, '%f%f%f%f%f%f%f%f%f%f', 'delimiter', ',');
inp_data_cmc = data;
fclose(f4);
inp_data_cmc = randomize(data);



%%%Feature Extraction of Iris
for i = 1:length(inp_data_iris{1})
	if(strcmp(inp_data_iris{5}(i), 'Iris-setosa'))
		class_samp_iris(i) = 1;
	elseif(strcmp(inp_data_iris{5}(i), 'Iris-versicolor'))
		class_samp_iris(i) = 2;
	else
		class_samp_iris(i) = 3;
	end
end
inp_data_iris{5} = class_samp_iris;

%%%Feature Extraction of Car
buy = zeros(length(inp_data_car{1}), 1);
maint = zeros(length(inp_data_car{1}), 1);
doors = zeros(length(inp_data_car{1}), 1);
persons = zeros(length(inp_data_car{1}), 1);
lug = zeros(length(inp_data_car{1}), 1);
safety = zeros(length(inp_data_car{1}), 1);
class_samp_car = zeros(length(inp_data_car{1}), 1);

for i = 1:length(inp_data_car{1})

	if(strcmp(inp_data_car{1}(i), 'vhigh'))
		buy(i) = 6;
	elseif(strcmp(inp_data_car{1}(i), 'high'))
		buy(i) = 4.5;
	elseif(strcmp(inp_data_car{1}(i), 'med'))
		buy(i) = 3;
	else
		buy(i) = 1.5;
	end

	if(strcmp(inp_data_car{2}(i), 'vhigh'))
		maint(i) = 6;
	elseif(strcmp(inp_data_car{2}(i), 'high'))
		maint(i) = 4.5;
	elseif(strcmp(inp_data_car{2}(i), 'med'))
		maint(i) = 3;
	else
		maint(i) = 1.5;
	end

	if(strcmp(inp_data_car{3}(i), '2'))	
		doors(i) = 2;
	elseif(strcmp(inp_data_car{3}(i), '3'))	
		doors(i) = 3;
	elseif(strcmp(inp_data_car{3}(i), '4'))	
		doors(i) = 4;
	else
		doors(i) = 6;
	end

	if(strcmp(inp_data_car{4}(i), '2'))	
		persons(i) = 2;
	elseif(strcmp(inp_data_car{4}(i), '4'))	
		persons(i) = 4;
	else
		persons(i) = 6;
	end

	if(strcmp(inp_data_car{5}(i), 'small'))
		lug(i) = 2;
	elseif(strcmp(inp_data_car{5}(i), 'med'))
		lug(i) = 4;
	else
		lug(i) = 6;
	end

	if(strcmp(inp_data_car{6}(i), 'low'))
		safety(i) = 2;
	elseif(strcmp(inp_data_car{6}(i), 'med'))
		safety(i) = 4;
	else
		safety(i) = 6;
	end
	if(strcmp(inp_data_car{7}(i), 'unacc'))
		class_samp_car(i) = 1;
	elseif(strcmp(inp_data_car{7}(i), 'acc'))
		class_samp_car(i) = 2;
	elseif(strcmp(inp_data_car{7}(i), 'good'))
		class_samp_car(i) = 3;
	else
		class_samp_car(i) = 4;
	end

end

inp_data_car = [buy, maint, doors, persons, lug, safety, class_samp_car];

%%For wine
tem = transp([inp_data_iris{1}; inp_data_iris{2}; inp_data_iris{3}; inp_data_iris{4}; class_samp_iris]);
inp_data_iris = tem;
length_wine = length(inp_data_wine);
for i = 1: length_wine
	te(:,i) = inp_data_wine{mod(i,length_wine) + 1} ;
end

inp_data_wine = te;

%%For contraception
for i = 1: length(inp_data_cmc)
	temp_cmc(:,i) = inp_data_cmc{i};
end		
inp_data_cmc = temp_cmc;

inp_data = {inp_data_iris, inp_data_car, inp_data_wine, inp_data_cmc};

me = zeros(4,5,5);
std = zeros(4,5,5);
for i = 1:4
	[mean,sd] = k_all(inp_data{i}, 1);
	me(i,:,:) = mean;
	std(i,:,:) = sd;
end



