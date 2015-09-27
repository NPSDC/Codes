red_points = [[1,1,7]; [1, 6, 3]; [1, 7, 8]; [1, 8, 9]; [1, 4, 5]; [1, 7, 5]];
blue_points = [[1, 3, 1]; [1, 4, 3]; [1, 2, 4]; [1, 7, 1]; [1, 1, 3]; [1, 4, 2]];
%Initial Weight Vector
a0 = rand();
a1 = rand();
a2 = rand();
a = [a0; a1; a2];
b = 1;
eta = 0.5;

n = 6;
threshold = 0.0001;
a_single = single_sample(red_points, blue_points, 0, a, n);
a_single_marg = single_sample(red_points, blue_points, b, a, n);
a_relax = Relaxation(red_points, blue_points, b, a, n, eta);
a_LMS = LMS(red_points, blue_points, 0, a, n, eta, threshold);
clf;
plot(red_points(:,2), red_points(:,3), 'r.');hold on;
plot(blue_points(:,2), blue_points(:,3), 'b.'); hold on;
plot([-a_single(1)/a_single(2), 0], [0, -a_single(1)/a_single(3)], 'g-');hold on;
plot([-a_single_marg(1)/a_single_marg(2), 0], [0, -a_single_marg(1)/a_single_marg(3)]);hold on;
plot([-a_relax(1)/a_relax(2), 0], [0, -a_relax(1)/a_relax(3)],'y');hold on;
plot([-a_LMS(1)/a_LMS(2), 0], [0, -a_LMS(1)/a_LMS(3)], 'm');hold on;
legend('Class1','class2','single', 'margin','relaxation', 'LMS');
%axis([0, 10, 0, 10]);
hold off;
 
