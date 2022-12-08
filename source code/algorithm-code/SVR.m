function [y_SVR,error_SVR,model] = SVR(x,y)
    [c,g] = meshgrid(-10:0.5:10,-10:0.5:10);
    [m,n] = size(c);
    cg = zeros(m,n);
    eps = 10^(-4);
    v = 5;
    bestc = 0;
    bestg = 0;
    error = Inf;
    for i = 1:m
        for j = 1:n
            cmd = ['-v ',num2str(v),' -t 2',' -c ',num2str(2^c(i,j)),' -g ',num2str(2^g(i,j) ),' -s 3 -p 0.1'];
            cg(i,j) = libsvm_svmtrain(y',x',cmd);
            if cg(i,j) < error
                error = cg(i,j);
                bestc = 2^c(i,j);
                bestg = 2^g(i,j);
            end
            if abs(cg(i,j) - error) <= eps && bestc > 2^c(i,j)
                error = cg(i,j);
                bestc = 2^c(i,j);
                bestg = 2^g(i,j);
            end
        end
    end
    cmd = [' -t 2',' -c ',num2str(bestc),' -g ',num2str(bestg),' -s 3 -p 0.01'];
    model = libsvm_svmtrain(y',x',cmd);
    [Predict,error,y_SVR] = svmpredict(y',x',model);
    y_SVR = y_SVR';
    error_SVR = abs(y_SVR - y);
end

