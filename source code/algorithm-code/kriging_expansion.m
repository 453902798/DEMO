clc 
clear all 
close all 

%% 1 建立原始预测模型
% 建立train集的预测模型，获得train集预测误差
% 数据
LHS_branin;
y = branin(x);
[x_train,y_train,x_test,y_test,max1,min1,max2,min2] = normalization(x,y);%归一化
[y_Kriging,~,dmodel] = kriging(x_train,y_train);
[value_Kriging,~] = predictor(x_test', dmodel);
value_Kriging = value_Kriging';
error_Kriging = abs(value_Kriging - y_test);
y_hybrid_test = value_Kriging;
y_hybrid_train = y_Kriging;
error_hybrid_test = abs(value_Kriging - y_test); mean1 = mean(error_hybrid_test);
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

% LB = CL - 1./sku'.*(CL - MIN');
% UB = CL + 1./skl'.*(MAX' - CL);

%% 3 GA优化获得虚拟样本
num = 200; %生成虚拟样本个数
a = min(error_hybrid_train); b = max(error_hybrid_train); y_error = (error_hybrid_train-a)./(b-a);
[x_vir,~] = GA_kriging(LB, UB, num, x_train, y_error);
x_vir = x_vir';
% 预测y_vir
[value_Kriging_vir,~] = predictor(x_vir', dmodel);
y_vir = value_Kriging_vir';
% 唯一化
data = [x_vir;y_vir]';
data_unique = unique(data,'rows');
x_vir2 = data_unique(:,1:2)';
y_vir2 = data_unique(:,3)';

%% 4 建立虚拟样本预测模型
[y_Kriging_vir,~,dmodel_vir] = kriging(x_vir2,y_vir2);
[value_Kriging_vir,~] = predictor(x_test', dmodel_vir);
value_Kriging_vir = value_Kriging_vir';
error_Kriging_vir = abs(value_Kriging_vir - y_test);
y_hybrid_vir = value_Kriging_vir;
error_hybrid_vir = abs(y_hybrid_vir - y_test); mean2 = mean(error_hybrid_vir);

%% 5 建立原始数据和虚拟样本的混合kriging代理模型


