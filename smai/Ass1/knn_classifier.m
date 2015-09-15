function [ output ] = knn_classifier( test, training, group, k, d)
    dim = size(test);
    output = zeros(dim(1), 1);
    for i = 1:dim(1)
        grp = inf(k,1);
        distances = inf(k, 1);
        abs_distances = inf(k, 1);
        grp2 = inf(k,1);
        for j = 1:size(training, 1)
            dist = sum((training(j,:)- test(i,:)).^2);
            dist2 = sum(abs(training(j,:)- test(i,:)));
            [large1, index1] = max(abs_distances);
            [large, index] = max(distances);
            if(dist < large)
                distances(index) = dist;
                grp(index) = group(j);
            end
            if(dist2 < large1)
                abs_distances(index1) = dist2;
                grp2(index1) = group(j);
            end
        end
        if(d == 1)
            counts = tabulate(grp);
                    
            [m , ind] = max(counts(:, 2));
            output(i) = counts(ind);
        end
        if(d==2)
            counts = tabulate(grp2);
                    
            [m , ind] = max(counts(:, 2));
            output(i) = counts(ind);
        end
    end
    
       
end