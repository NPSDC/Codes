function [ a ] = single_sample( red_points, blue_points, b, a, n )
%Performs a single_sample perceptron operation

    norm_blue_points = -blue_points;
    while(1) 
        flag1 = 0;
        flag2 = 0;
        for i = 1:n
            if(dot(transp(a), transp(red_points(i,:))) <= b)        
                flag1 = 1;
                break;
            end
            if(dot(transp(a), transp(norm_blue_points(i,:))) <= b)
                flag2 = 1;
                break;
            end
        end
        if(flag1 == 1)
            %disp(red_points(i,:));
            a = a + transp(red_points(i,:));
            %disp(a);
        elseif(flag2 == 1)
            %disp(blue_points(i,:));
            a = a + transp(norm_blue_points(i,:));
            %disp(a);
        else
            break;
        end
        %{
        clf;
        plot(red_points(:,2), red_points(:,3), 'r.'); hold on;
        plot(blue_points(:,2), blue_points(:,3), 'b.'); hold on;
        plot([-a(1)/a(3), 0], [0, -a(1)/a(2)], 'g-');
        axis([0, 10, 0, 10]);
        %}
    end 

end

