function [x_train,y_train,x_test,y_test] = normalization(x,y)
    rd = randperm(size(x,2));
    s = round(size(rd,2)/5*4);
    x_train = x(:,rd(1:s));
    y_train = y(:,rd(1:s));
    x_test = x(:,rd(s+1:end));
    y_test = y(:,rd(s+1:end));
    
%     max1 = max(x')';
%     min1 = min(x')';
    max2 = max(y)';
    min2 = min(y)';
%     
%     x_train = (x_train-min1)./(max1-min1);
%     x_train = x_train';
%     x_test = (x_test-min1)./(max1-min1);
%     x_test = x_test';
    y_train = 10*(y_train-min2)./(max2-min2);
%     y_train = y_train';
    y_test = 10*(y_test-min2)./(max2-min2);
%     y_test = y_test';
end

