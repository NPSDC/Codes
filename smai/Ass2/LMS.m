function [ a ] = LMS( red_points, blue_points, b, a, n , eta , threshold )
%Implements LMS
    norm_blue_points = -blue_points;
    k = 1;
    start = 1;
    while(1)
       a_old = a;
       flag = 0;
       eta = eta;
       for i = start:n
           if((dot(transp(a), red_points(i,:)) - b) < 0)
               delta_j = eta*(b - dot(transp(a), red_points(i,:)))*transp(red_points(i,:));
               a = a + delta_j;
               start = mod(i , n) + 1;
               flag = 1;
               break;
           end
       end
       for i = start:n
           if((dot(transp(a), norm_blue_points(i,:)) - b) < 0)
               delta_j = eta*(b - dot(transp(a), norm_blue_points(i,:)))*transp(norm_blue_points(i,:));
               a = a + delta_j;
               start = mod(i , n) + 1;
               flag = 1;
               break;
           end
       end
       disp(i);
       disp(delta_j);
       if(sum(abs(a - a_old) <= threshold ) ==3)                       
           break;
       end
       %disp(a);
       k = k+1;
    end
end

