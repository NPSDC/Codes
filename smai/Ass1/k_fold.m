

function [ mean, sd ] = k_fold(k, sample, p )

	size_sample = size(sample);
	no_of_rows = size_sample(1);
	len_of_seg = int32(no_of_rows/k);
	start_indexes =  1:len_of_seg:no_of_rows;
	actual = 1:no_of_rows;
	m = 1;
	n = 1;
	mean = 0;
	count = 0;
	obs = zeros(k,1);
	for p = 1:5
		for i = 1:k
			for j = 1:no_of_rows
				if(j >= start_indexes(i) && j < start_indexes(i) + len_of_seg )
					test(m) = actual(j);
					m = m + 1;
				else
					training(n) = actual(j);
					n = n + 1;
				end			
			end
			output_rows = knn_classifier(sample(test, 1:size_sample(2) - 1), sample(training, 1:size_sample(2) - 1),...
			 sample(training, size_sample(2)), p, 1);

			%output_rows == sample(test, size_sample(2))
			count = 0;
			for j=1:size(output_rows)
				if(output_rows(j) == sample(test(j), size_sample(2)))			
					count = count + 1;
				end
			end
			
			obs(i) = count/double(len_of_seg);
			count = 0;
			
			m = 1;
			n = 1;
		end	 
		
		mean(p) = sum(obs)/k;
		sd(p) = std(obs);

	end
	
end

