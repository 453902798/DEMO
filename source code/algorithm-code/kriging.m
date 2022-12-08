function [y_kriging,error,dmodel] = kriging(x,y)
    theta = 10;lob = 1e-1;upb = 20;
    [dmodel, ~] = dacefit(x', y', @regpoly0, @corrgauss, theta, lob, upb);
    [y_kriging,MSE] = predictor(x', dmodel);
    y_kriging = y_kriging';
    error = abs(y_kriging - y);
end

