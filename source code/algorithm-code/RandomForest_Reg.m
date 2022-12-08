clear
clc
% example 8: calculating importance
extra_options.importance = 1; %(0 = (Default) Don't, 1=calculate)

model = regRF_train(x_train',y_train', 100, 4, extra_options);
Y_hat = regRF_predict(x_test',model);
error_regRF = abs(Y_hat' - y_test);
mean0 = mean(error_regRF);
mse0 = mse(error_regRF);
