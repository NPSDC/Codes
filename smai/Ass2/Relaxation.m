function [ a ] = Relaxation( red_points, blue_points, b, a, n , eta )
%Summary of this function goes here

    norm_blue_points = -blue_points;
    
    while(1) 
        a_old = a;
        for i = 1:n
            if(dot(transp(a), transp(red_points(i,:))) <= b)                        
                delta_j = b - dot(transp(a),transp(red_points(i,:)))/(norm(transp(red_points(i,:)))^2);
                a = a + eta*transp(red_points(i,:))*delta_j;
                break;
            end
            if(dot(transp(a), transp(norm_blue_points(i,:))) <= b)
                delta_j = b - dot(transp(a),transp(norm_blue_points(i,:)))/(norm(transp(norm_blue_points(i,:)))^2);
                a = a + eta*transp(norm_blue_points(i,:))*delta_j;
                break;
            end
        end
        if(a == a_old)
            break;
        end
     end
end

