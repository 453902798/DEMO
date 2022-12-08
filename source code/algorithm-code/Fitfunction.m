function z=Fitfunction(x)    
    %% SVR
    load('model.mat')
    value_SVR = [];
    for j = 1:5
        [Predict,~,~] = svmpredict(j,x,model); 
        value_SVR(:,j) = Predict;
    end
    %% Kriging
    load('dmodel.mat')
    [YX,~] = predictor(x', dmodel);
    value_Kriging = YX';
    %% RBF
    load('net.mat')
    T_fit = sim(net,x');
    value_RBF = T_fit';
    %% 
    load('mean_error_Kriging_test.mat')
    load('mean_error_RBF_test.mat')
    load('mean_error_SVR_test.mat')
    w1 = [];
    w2 = [];
    w3 = [];
    value_hybrid_surrogate = [];
    for j= 1:5
        w1(j) = (1./mean_error_Kriging_test(j))^2./((1./mean_error_Kriging_test(j))^2+(1./mean_error_RBF_test(j))^2+(1./mean_error_SVR_test(j))^2);
        w2(j) = (1./mean_error_RBF_test(j))^2./((1./mean_error_Kriging_test(j))^2+(1./mean_error_RBF_test(j))^2+(1./mean_error_SVR_test(j))^2);
        w3(j) = (1./mean_error_SVR_test(j))^2./((1./mean_error_Kriging_test(j))^2+(1./mean_error_RBF_test(j))^2+(1./mean_error_SVR_test(j))^2);
        value_hybrid_surrogate(j) = w1(j)*value_Kriging(j)+w2(j)*value_RBF(j)+w3(j)*value_SVR(j);
    end
    
    z1=value_hybrid_surrogate(1);
    
    z2=value_hybrid_surrogate(2);
    
    z3=value_hybrid_surrogate(3);
    
    z4=value_hybrid_surrogate(4);
    
    z5=value_hybrid_surrogate(5);
    
    z=[z1 z2 z3 z4 z5]';

end