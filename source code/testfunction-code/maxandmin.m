%% 1
min0 = min(error_hybrid_test);
max0 = max(error_hybrid_test);
min1 = min(error_hybrid_hybrid);
max1 = max(error_hybrid_hybrid);

%% 2
% [LB,UB] = Gaussian(x_kuo,y_kuo,bias);
LB = CL - 1./sku'.*(CL - MIN');
UB = CL + 1./skl'.*(MAX' - CL);
% 改变扩充的隶属度函数：三角隶属度函数/高斯隶属度函数

% 获得虚拟样本
num = 200; %生成虚拟样本个数
[d,~] = size(x);
x_vir = generation_uniform(LB, UB, num, d);% 改变采样方式：均匀采样/高斯采样
[value_Kriging_vir,~] = predictor(x_vir', dmodel);value_Kriging_vir = value_Kriging_vir';
value_RBF_vir = sim(net,x_vir);
[~,~,value_SVR_vir] = svmpredict(eye(size(x_vir',1),1),x_vir',model);value_SVR_vir = value_SVR_vir';
y_vir = w11*value_Kriging_vir+w12*value_RBF_vir+w13*value_SVR_vir;

% 建立虚拟样本预测模型
[y_Kriging_vir,~,dmodel_vir] = kriging(x_vir,y_vir);
[y_RBF_vir,~,net_vir] = RBF(x_vir,y_vir);
[y_SVR_vir,~,model_vir] = SVR(x_vir,y_vir);
[value_Kriging_vir,~] = predictor(x_test', dmodel_vir);value_Kriging_vir = value_Kriging_vir';error_Kriging_vir = abs(value_Kriging_vir - y_test);
value_RBF_vir = sim(net_vir,x_test);error_RBF_vir = abs(value_RBF_vir - y_test);
[~,~,value_SVR_vir] = svmpredict(eye(size(x_test',1),1),x_test',model_vir);value_SVR_vir = value_SVR_vir';error_SVR_vir = abs(value_SVR_vir - y_test);
mean5 = mean(error_Kriging_vir); mean6 = mean(error_RBF_vir); mean7 = mean(error_SVR_vir); 
w21 = 1./(mean5)^2./(1./(mean5)^2+1./(mean6)^2+1./(mean7)^2);
w22 = 1./(mean6)^2./(1./(mean5)^2+1./(mean6)^2+1./(mean7)^2);
w23 = 1./(mean7)^2./(1./(mean5)^2+1./(mean6)^2+1./(mean7)^2);
y_hybrid_vir = w21*value_Kriging_vir+w22*value_RBF_vir+w23*value_SVR_vir;
error_hybrid_vir = abs(y_hybrid_vir - y_test); mean8 = mean(error_hybrid_vir);

% 建立原始数据和虚拟样本的混合代理模型
% 原模型预测 mean4
y1 = y_hybrid_test;
% 虚拟样本模型预测 mean8
y2 = y_hybrid_vir;
% 最终混合预测值
w31 = 1./(mean4)^2./(1./(mean4)^2+1./(mean8)^2);w32 = 1./(mean8)^2./(1./(mean4)^2+1./(mean8)^2);
y_hybrid_hybrid = w31*y1 + w32*y2;
error_hybrid_hybrid = abs(y_hybrid_hybrid - y_test); mean9 = mean(error_hybrid_hybrid);mse9 = mse(error_hybrid_hybrid);

min2 = min(error_hybrid_hybrid);
max2 = max(error_hybrid_hybrid);

%% 3
% [LB,UB] = Gaussian(x_kuo,y_kuo,bias);
LB = CL - 1./sku'.*(CL - MIN');
UB = CL + 1./skl'.*(MAX' - CL);
% 改变扩充的隶属度函数：三角隶属度函数/高斯隶属度函数

% 获得虚拟样本
num = 200; %生成虚拟样本个数
[d,~] = size(x);
x_vir = generation_gaussian(LB, UB, num, d);% 改变采样方式：均匀采样/高斯采样
[value_Kriging_vir,~] = predictor(x_vir', dmodel);value_Kriging_vir = value_Kriging_vir';
value_RBF_vir = sim(net,x_vir);
[~,~,value_SVR_vir] = svmpredict(eye(size(x_vir',1),1),x_vir',model);value_SVR_vir = value_SVR_vir';
y_vir = w11*value_Kriging_vir+w12*value_RBF_vir+w13*value_SVR_vir;

% 建立虚拟样本预测模型
[y_Kriging_vir,~,dmodel_vir] = kriging(x_vir,y_vir);
[y_RBF_vir,~,net_vir] = RBF(x_vir,y_vir);
[y_SVR_vir,~,model_vir] = SVR(x_vir,y_vir);
[value_Kriging_vir,~] = predictor(x_test', dmodel_vir);value_Kriging_vir = value_Kriging_vir';error_Kriging_vir = abs(value_Kriging_vir - y_test);
value_RBF_vir = sim(net_vir,x_test);error_RBF_vir = abs(value_RBF_vir - y_test);
[~,~,value_SVR_vir] = svmpredict(eye(size(x_test',1),1),x_test',model_vir);value_SVR_vir = value_SVR_vir';error_SVR_vir = abs(value_SVR_vir - y_test);
mean5 = mean(error_Kriging_vir); mean6 = mean(error_RBF_vir); mean7 = mean(error_SVR_vir); 
w21 = 1./(mean5)^2./(1./(mean5)^2+1./(mean6)^2+1./(mean7)^2);
w22 = 1./(mean6)^2./(1./(mean5)^2+1./(mean6)^2+1./(mean7)^2);
w23 = 1./(mean7)^2./(1./(mean5)^2+1./(mean6)^2+1./(mean7)^2);
y_hybrid_vir = w21*value_Kriging_vir+w22*value_RBF_vir+w23*value_SVR_vir;
error_hybrid_vir = abs(y_hybrid_vir - y_test); mean8 = mean(error_hybrid_vir);

% 建立原始数据和虚拟样本的混合代理模型
% 原模型预测 mean4
y1 = y_hybrid_test;
% 虚拟样本模型预测 mean8
y2 = y_hybrid_vir;
% 最终混合预测值
w31 = 1./(mean4)^2./(1./(mean4)^2+1./(mean8)^2);w32 = 1./(mean8)^2./(1./(mean4)^2+1./(mean8)^2);
y_hybrid_hybrid = w31*y1 + w32*y2;
error_hybrid_hybrid = abs(y_hybrid_hybrid - y_test); mean9 = mean(error_hybrid_hybrid);mse9 = mse(error_hybrid_hybrid);

min3 = min(error_hybrid_hybrid);
max3 = max(error_hybrid_hybrid);

%% 4
[LB,UB] = Gaussian(x_kuo,y_kuo,bias);
% LB = CL - 1./sku'.*(CL - MIN');
% UB = CL + 1./skl'.*(MAX' - CL);
% 改变扩充的隶属度函数：三角隶属度函数/高斯隶属度函数

% 获得虚拟样本
num = 200; %生成虚拟样本个数
[d,~] = size(x);
x_vir = generation_uniform(LB, UB, num, d);% 改变采样方式：均匀采样/高斯采样
[value_Kriging_vir,~] = predictor(x_vir', dmodel);value_Kriging_vir = value_Kriging_vir';
value_RBF_vir = sim(net,x_vir);
[~,~,value_SVR_vir] = svmpredict(eye(size(x_vir',1),1),x_vir',model);value_SVR_vir = value_SVR_vir';
y_vir = w11*value_Kriging_vir+w12*value_RBF_vir+w13*value_SVR_vir;

% 建立虚拟样本预测模型
[y_Kriging_vir,~,dmodel_vir] = kriging(x_vir,y_vir);
[y_RBF_vir,~,net_vir] = RBF(x_vir,y_vir);
[y_SVR_vir,~,model_vir] = SVR(x_vir,y_vir);
[value_Kriging_vir,~] = predictor(x_test', dmodel_vir);value_Kriging_vir = value_Kriging_vir';error_Kriging_vir = abs(value_Kriging_vir - y_test);
value_RBF_vir = sim(net_vir,x_test);error_RBF_vir = abs(value_RBF_vir - y_test);
[~,~,value_SVR_vir] = svmpredict(eye(size(x_test',1),1),x_test',model_vir);value_SVR_vir = value_SVR_vir';error_SVR_vir = abs(value_SVR_vir - y_test);
mean5 = mean(error_Kriging_vir); mean6 = mean(error_RBF_vir); mean7 = mean(error_SVR_vir); 
w21 = 1./(mean5)^2./(1./(mean5)^2+1./(mean6)^2+1./(mean7)^2);
w22 = 1./(mean6)^2./(1./(mean5)^2+1./(mean6)^2+1./(mean7)^2);
w23 = 1./(mean7)^2./(1./(mean5)^2+1./(mean6)^2+1./(mean7)^2);
y_hybrid_vir = w21*value_Kriging_vir+w22*value_RBF_vir+w23*value_SVR_vir;
error_hybrid_vir = abs(y_hybrid_vir - y_test); mean8 = mean(error_hybrid_vir);

% 建立原始数据和虚拟样本的混合代理模型
% 原模型预测 mean4
y1 = y_hybrid_test;
% 虚拟样本模型预测 mean8
y2 = y_hybrid_vir;
% 最终混合预测值
w31 = 1./(mean4)^2./(1./(mean4)^2+1./(mean8)^2);w32 = 1./(mean8)^2./(1./(mean4)^2+1./(mean8)^2);
y_hybrid_hybrid = w31*y1 + w32*y2;
error_hybrid_hybrid = abs(y_hybrid_hybrid - y_test); mean9 = mean(error_hybrid_hybrid);mse9 = mse(error_hybrid_hybrid);

min4 = min(error_hybrid_hybrid);
max4 = max(error_hybrid_hybrid);

%%
min_total = [min0,min2,min3,min4,min1];
max_total = [max0,max2,max3,max4,max1];
