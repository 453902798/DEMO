function [T_fit_test,YX_test,decision_values,value_hybrid_surrogate_test] = HSM_predictor(x,dmodel,net,model,w1,w2,w3)
    %% RBF
    T_fit_test = sim(net,x');

    %% kriging
    [YX_test,MSE_test] = predictor(x, dmodel);
    YX_test = YX_test';

    %% SVR
    [Predict,error,decision_values] = svmpredict(eye(size(x,1),1),x,model);
    decision_values = decision_values';

    %% 混合代理模型
    value_hybrid_surrogate_test = w1*T_fit_test+w2*YX_test+w3*decision_values;

end

