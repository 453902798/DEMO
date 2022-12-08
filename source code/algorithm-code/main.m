clc 
clear all 
close all 
%% 1 ����ԭʼԤ��ģ��
% ����train����Ԥ��ģ�ͣ����train��Ԥ�����
% ����
load data_x 
load data_y 
x = data_x; 
y = data_y; 
[x_train,y_train,x_test,y_test] = normalization(x,y);%��һ��
x_nor = [x_train,x_test]; y_nor = [y_train,y_test]; %���彨ģ
[y_Kriging,~,dmodel] = kriging(x_train,y_train);
[y_RBF,~,net] = RBF(x_train,y_train);
[y_SVR,~,model] = SVR(x_train,y_train);
% Ԥ�����
[value_Kriging,~] = predictor(x_test', dmodel);value_Kriging = value_Kriging';error_Kriging = abs(value_Kriging - y_test);
value_RBF = sim(net,x_test);error_RBF = abs(value_RBF - y_test);
[~,~,value_SVR] = svmpredict(eye(size(x_test',1),1),x_test',model);value_SVR = value_SVR';error_SVR = abs(value_SVR - y_test);
% ����Ȩ��
mean1 = mean(error_Kriging); mean2 = mean(error_RBF); mean3 = mean(error_SVR); 
mse1 = mse(error_Kriging); mse2 = mse(error_RBF); mse3 = mse(error_SVR);
w11 = 1./(mean1)^2./(1./(mean1)^2+1./(mean2)^2+1./(mean3)^2);
w12 = 1./(mean2)^2./(1./(mean1)^2+1./(mean2)^2+1./(mean3)^2);
w13 = 1./(mean3)^2./(1./(mean1)^2+1./(mean2)^2+1./(mean3)^2);
y_hybrid_test = w11*value_Kriging+w12*value_RBF+w13*value_SVR;
y_hybrid_train = w11*y_Kriging+w12*y_RBF+w13*y_SVR;
error_hybrid_test = abs(y_hybrid_test - y_test); mean4 = mean(error_hybrid_test); mse4 = mse(error_hybrid_test);
error_hybrid_train = abs(y_hybrid_train - y_train);

%% 2 ������������
[m,n] = size(x_nor);
CL = mean(x_nor,2);

% ��ÿһ��x�������࣬��CL��߹��NL����CL�ұ߹��NU
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

% ������ƫ��skl��sku
sp = 1;
skl = (NL./(NL+NU+sp))';
sku = (NU./(NL+NU+sp))';

% �������������������
NL_vir = round(skl.*NL);
NU_vir = round(sku.*NU);

% ��������չ����,�ø�˹����(������(CL,1)����MIN,skl����(MAX,sku))
MIN = min(x_nor');
MAX = max(x_nor');
x_kuo = [CL';MIN;MAX]';
y_kuo = [ones(6,1)';skl;sku]';
bias = 0.1;

% [LB,UB] = Gaussian(x_kuo,y_kuo,bias);
LB = CL - 1./sku'.*(CL - MIN');
UB = CL + 1./skl'.*(MAX' - CL);
% �ı�����������Ⱥ��������������Ⱥ���/��˹�����Ⱥ���

%% 3 �����������
num = 400; %����������������
x_vir = generation(LB, UB, num);% �ı������ʽ�����Ȳ���/��˹����
[value_Kriging_vir,~] = predictor(x_vir', dmodel);value_Kriging_vir = value_Kriging_vir';
value_RBF_vir = sim(net,x_vir);
[~,~,value_SVR_vir] = svmpredict(eye(size(x_vir',1),1),x_vir',model);value_SVR_vir = value_SVR_vir';
y_vir = w11*value_Kriging_vir+w12*value_RBF_vir+w13*value_SVR_vir;

%% 4 ������������Ԥ��ģ��
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

%% 5 ����ԭʼ���ݺ����������Ļ�ϴ���ģ��
% ԭģ��Ԥ�� mean4
y1 = y_hybrid_test;
% ��������ģ��Ԥ�� mean8
y2 = y_hybrid_vir;
% ���ջ��Ԥ��ֵ
w31 = 1./(mean4)^2./(1./(mean4)^2+1./(mean8)^2);w32 = 1./(mean8)^2./(1./(mean4)^2+1./(mean8)^2);
y_hybrid_hybrid = w31*y1 + w32*y2;
error_hybrid_hybrid = abs(y_hybrid_hybrid - y_test); mean9 = mean(error_hybrid_hybrid);mse9 = mse(error_hybrid_hybrid);
%% 6 ���������ϴ���ģ��
x_total = [x_train, x_vir];
y_total = [y_train, y_vir];
[y_Kriging_total,~,dmodel_total] = kriging(x_total,y_total);
[y_RBF_total,~,net_total] = RBF(x_total,y_total);
[y_SVR_total,~,model_total] = SVR(x_total,y_total);
[value_Kriging_total,~] = predictor(x_test', dmodel_total);value_Kriging_total = value_Kriging_total';error_Kriging_total = abs(value_Kriging_total - y_test);
value_RBF_total = sim(net_total,x_test);error_RBF_total = abs(value_RBF_vir - y_test);
[~,~,value_SVR_total] = svmpredict(eye(size(x_test',1),1),x_test',model_total);value_SVR_total = value_SVR_total';error_SVR_total = abs(value_SVR_total - y_test);
mean10 = mean(error_Kriging_total); mean11 = mean(error_RBF_total); mean12 = mean(error_SVR_total); 
w41 = 1./(mean10)^2./(1./(mean10)^2+1./(mean11)^2+1./(mean12)^2);
w42 = 1./(mean11)^2./(1./(mean10)^2+1./(mean11)^2+1./(mean12)^2);
w43 = 1./(mean12)^2./(1./(mean10)^2+1./(mean11)^2+1./(mean12)^2);
y_hybrid_total = w21*value_Kriging_total+w22*value_RBF_total+w23*value_SVR_total;
error_hybrid_total = abs(y_hybrid_total - y_test); mean13 = mean(error_hybrid_total);mse13 = mse(error_hybrid_total);
