red_points = [[1,1,7]; [1, 6, 3]; [1, 7, 8]; [1, 8, 9]; [1, 4, 5]; [1, 7, 5]];
blue_points = [[1, 3, 1]; [1, 4, 3]; [1, 2, 4]; [1, 7, 1]; [1, 1, 3]; [1, 4, 2]];
%Initial Weight Vector
a0 = rand();
a1 = rand();
a2 = rand();
a = [a0; a1; a2];
b = 1;
eta = 0.01;

n = 6;
threshold = 0.0005;
a = LMS(red_points, blue_points, b, a, n, eta, threshold);
clf;
plot(red_points(:,2), red_points(:,3), 'r.');hold on;
plot(blue_points(:,2), blue_points(:,3), 'b.'); hold on;
plot([-a(1)/a(2), 0], [0, -a(1)/a(3)], 'g-');hold on;
%axis([0, 10, 0, 10]);
hold off;
 
