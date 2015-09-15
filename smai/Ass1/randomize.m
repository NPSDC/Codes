function [ out_data ] = randomize( input_data )
% This function randomizes the given cell
rand = randperm(length(input_data{1}));
for i = 1:length(rand)
	for j = 1:length(input_data)
		out_data{j}(i) = input_data{j}(rand(i));
	end
end





