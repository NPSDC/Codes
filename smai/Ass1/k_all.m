function[mean_com,sd_com] = k_all(sample, d)
	mean_com = zeros(4, 5);
	sd_com =zeros(4,5);
	for i = 2:5
		[mean_com(i,:), sd_com(i,:)] = k_fold(i, sample, d);
	end
	n = 1:5;	
	figure();
	f2 = errorbar(n, mean_com(2,:), sd_com(2,:)/2,'g'); hold on;
	f3 = errorbar(n, mean_com(3,:), sd_com(3,:)/2,'r'); hold on;
	f4 = errorbar(n, mean_com(4,:), sd_com(4,:)/2,'b'); hold on;
	f5 = errorbar(n, mean_com(5,:), sd_com(5,:)/2,'k'); 
	legend([f2, f3, f4, f5], {'2-fold', '3-fold', '4-fold', '5-fold'});
	xlabel('nearest neighbours' );
	ylabel('mean');
	
end