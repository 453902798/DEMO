% 参考文献：A PSO based virtual sample generation method for small sample sets: 
% Applications to regression datasets
clc 
clear all 
close all 

%% 1 建立原始预测模型
% 建立train集的预测模型，获得train集预测误差
% 数据
LHS_branin;
y = branin(x);
[x_train,y_train,x_test,y_test] = normalization(x,y);%归一化
x_nor = [x_train,x_test]; y_nor = [y_train,y_test]; %整体建模
[y_Kriging,~,dmodel] = kriging(x_train,y_train);
[y_RBF,~,net] = RBF(x_train,y_train);
[y_SVR,~,model] = SVR(x_train,y_train);
% 预测误差
[value_Kriging,~] = predictor(x_test', dmodel);value_Kriging = value_Kriging';error_Kriging = abs(value_Kriging - y_test);
value_RBF = sim(net,x_test);error_RBF = abs(value_RBF - y_test);
[~,~,value_SVR] = svmpredict(eye(size(x_test',1),1),x_test',model);value_SVR = value_SVR';error_SVR = abs(value_SVR - y_test);
% 计算权重
mean1 = mean(error_Kriging); mean2 = mean(error_RBF); mean3 = mean(error_SVR); 
w11 = 1./(mean1)^2./(1./(mean1)^2+1./(mean2)^2+1./(mean3)^2);
w12 = 1./(mean2)^2./(1./(mean1)^2+1./(mean2)^2+1./(mean3)^2);
w13 = 1./(mean3)^2./(1./(mean1)^2+1./(mean2)^2+1./(mean3)^2);
y_hybrid_test = w11*value_Kriging+w12*value_RBF+w13*value_SVR;
y_hybrid_train = w11*y_Kriging+w12*y_RBF+w13*y_SVR;
error_hybrid_test = abs(y_hybrid_test - y_test); mean4 = mean(error_hybrid_test);
error_hybrid_train = abs(y_hybrid_train - y_train);

%% 2 虚拟样本扩充
[m,n] = size(x_nor);
CL = mean(x_nor,2);

% 对每一个x变量分类，在CL左边归进NL，在CL右边归进NU
NL = [];
NU = [];
for i=1:m
   nl = 0;
   nu = 0;
   for j=1:n
       if x_nor(i,j)<=CL(i)
           nl = nl+1;
       else nu = nu+1;
       end
   end
   NL(i) = nl;
   NU(i) = nu;
end
NL = NL';
NU = NU';

% 求左右偏度skl和sku
sp = 1;
skl = (NL./(NL+NU+sp))';
sku = (NU./(NL+NU+sp))';

% 求左右虚拟样本点个数
NL_vir = round(skl.*NL);
NU_vir = round(sku.*NU);

% 求左右扩展区域,用高斯函数(三个点(CL,1)、（MIN,skl）、(MAX,sku))
MIN = min(x_nor');
MAX = max(x_nor');
x_kuo = [CL';MIN;MAX]';
y_kuo = [ones(2,1)';skl;sku]';
bias = 0.1;
[LB,UB] = Gaussian(x_kuo,y_kuo,bias);

% LB = CL - 1./sku.*(CL - MIN);
% UB = CL + 1./skl.*(MAX - CL);

%% 3 GA优化获得虚拟样本
num = 200; %生成虚拟样本个数
a = min(error_hybrid_train); b = max(error_hybrid_train); y_error = (error_hybrid_train-a)./(b-a);
[x_vir,~] = GA(LB, UB, num, x_train, y_error, w11, w12, w13);
x_vir = x_vir';
% 预测y_vir
[value_Kriging_vir,~] = predictor(x_vir', dmodel);value_Kriging_vir = value_Kriging_vir';
value_RBF_vir = sim(net,x_vir);
[~,~,value_SVR_vir] = svmpredict(eye(size(x_vir',1),1),x_vir',model);value_SVR_vir = value_SVR_vir';
y_vir = w11*value_Kriging_vir+w12*value_RBF_vir+w13*value_SVR_vir;
% 唯一化
data = [x_vir;y_vir]';
data_unique = unique(data,'rows');
x_vir2 = data_unique(:,1:2)';
y_vir2 = data_unique(:,3)';

%% 4 建立虚拟样本预测模型
[y_Kriging_vir,~,dmodel_vir] = kriging(x_vir2,y_vir2);
[y_RBF_vir,~,net_vir] = RBF(x_vir2,y_vir2);
[y_SVR_vir,~,model_vir] = SVR(x_vir2,y_vir2);
[value_Kriging_vir,~] = predictor(x_test', dmodel_vir);value_Kriging_vir = value_Kriging_vir';error_Kriging_vir = abs(value_Kriging_vir - y_test);
value_RBF_vir = sim(net_vir,x_test);error_RBF_vir = abs(value_RBF_vir - y_test);
[~,~,value_SVR_vir] = svmpredict(eye(size(x_test',1),1),x_test',model_vir);value_SVR_vir = value_SVR_vir';error_SVR_vir = abs(value_SVR_vir - y_test);
mean5 = mean(error_Kriging_vir); mean6 = mean(error_RBF_vir); mean7 = mean(error_SVR_vir); 
w21 = 1./(mean5)^2./(1./(mean5)^2+1./(mean6)^2+1./(mean7)^2);
w22 = 1./(mean6)^2./(1./(mean5)^2+1./(mean6)^2+1./(mean7)^2);
w23 = 1./(mean7)^2./(1./(mean5)^2+1./(mean6)^2+1./(mean7)^2);
y_hybrid_vir = w21*value_Kriging_vir+w22*value_RBF_vir+w23*value_SVR_vir;
error_hybrid_vir = abs(y_hybrid_vir - y_test); mean8 = mean(error_hybrid_vir);

%% 5 建立原始数据和虚拟样本的混合代理模型
% 原模型预测 mean4
y1 = y_hybrid_test;
% 虚拟样本模型预测 mean8
y2 = y_hybrid_vir;
% 最终混合预测值
w31 = 1./(mean4)^2./(1./(mean4)^2+1./(mean8)^2);
w32 = 1./(mean8)^2./(1./(mean4)^2+1./(mean8)^2);
y_hybrid_hybrid = w31*y1 +w32*y2;
error_hybrid_hybrid = abs(y_hybrid_hybrid - y_test); mean9 = mean(error_hybrid_hybrid);

% %% 6 混合数据后预测
% x_final = [x_train';x_vir2']';
% y_final = [y_train';y_vir2']';
% [y_Kriging_final,~,dmodel_final] = kriging(x_final,y_final);
% [y_RBF_final,~,net_final] = RBF(x_final,y_final);
% [y_SVR_final,~,model_final] = SVR(x_final,y_final);
% [value_Kriging_final,~] = predictor(x_test', dmodel);value_Kriging_final = value_Kriging_final';error_Kriging_final = abs(value_Kriging_final - y_test);
% value_RBF_final = sim(net,x_test);error_RBF_final = abs(value_RBF_final - y_test);
% [~,~,value_SVR_final] = svmpredict(eye(size(x_test',1),1),x_test',model);value_SVR_final = value_SVR_final';error_SVR_final = abs(value_SVR_final - y_test);
% mean10 = mean(error_Kriging_final); mean11 = mean(error_RBF_final); mean12 = mean(error_SVR_final); 
% w41 = 1./(mean10)^2./(1./(mean10)^2+1./(mean11)^2+1./(mean12)^2);
% w42 = 1./(mean11)^2./(1./(mean10)^2+1./(mean11)^2+1./(mean12)^2);
% w43 = 1./(mean12)^2./(1./(mean10)^2+1./(mean11)^2+1./(mean12)^2);
% y3 = w41*value_Kriging_final+w42*value_RBF_final+w43*value_SVR_final;
% error_final= abs(y3 - y_test); mean13 = mean(error_hybrid_hybrid);
