function [ a ] = LMS( red_points, blue_points, b, a, n , eta , threshold )
%Implements LMS
    norm_blue_points = -blue_points;
    k = 1;
    
    while(1)
       a_old = a;
       
       eta = eta/k;
       for i = 1:2*n
           if(i <= n)
               delta_j = eta*(b - dot(transp(a), red_points(i,:)))*transp(red_points(i,:));
               a = a + delta_j;
               %start = mod(i , n) + 1;
           else
               delta_j = eta*(b - dot(transp(a), norm_blue_points(i-n,:)))*transp(norm_blue_points(i-n,:));
               a = a + delta_j;
               %start = mod(i , n) + 1;
               
            end
       end
       if(sum(abs(a - a_old) <= threshold ) == 3)                       
           break;
       end
       %disp(a);
       k = k+1;
       
    end
end

