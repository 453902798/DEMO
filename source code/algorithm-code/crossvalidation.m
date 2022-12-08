%% ��ϴ���ģ��
%% 1 SVR֧���������ع飨error_1��error_2�ĵڶ������ΪȨ�أ�
%% 1.1 ��ջ���
clc %��մ���
clear all %��չ�����
close all %���ͼ�δ���

%% ����������
LHS_stybtang10;
for i = 1:250
   y(i) = stybtang10(x(:,i)); 
end
data_x = x;
data_y = y;
%% 1.2.2 ѵ�����D�D������
[s,t] = size(x);
p_train = [x(:,t/5+1:t/5*2),x(:,t/5*2+1:t/5*3),x(:,t/5*3+1:t/5*4),x(:,t/5*4+1:t/5*5)]';
t_train = [y(:,t/5+1:t/5*2),y(:,t/5*2+1:t/5*3),y(:,t/5*3+1:t/5*4),y(:,t/5*4+1:t/5*5)]';
 
%% 1.2.3 ���Լ��D�D������
p_test = x(:,1:t/5)';
t_test = y(:,1:t/5)';
 
%% 1.3 ���ݹ�һ��
max1 = max(data_x');
min1 = min(data_x');
max2 = max(data_y');
min2 = min(data_y');
P_train = (p_train-min1)./(max1-min1);
P_test = (p_test-min1)./(max1-min1);
T_train = (t_train-min2)./(max2-min2);
T_test = (t_test-min2)./(max2-min2);
 
%% 1.4 SVMģ�ʹ���/ѵ��
%% 1.4.1 Ѱ�����c����/g����
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
        cg(i,j) = libsvm_svmtrain(T_train,P_train,cmd);
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

%% 1.4.2 ����/ѵ��SVM  
cmd = [' -t 2',' -c ',num2str(bestc),' -g ',num2str(bestg),' -s 3 -p 0.01'];
model = libsvm_svmtrain(T_train,P_train,cmd);

%% 1.5 SVM����Ԥ��
[Predict_2,error_2,decision_values2] = svmpredict(T_test,P_test,model);
value_SVR_test = Predict_2;
%error_1��error_2�ĵڶ���ΪMean squared error��������ΪSquared correlation coefficient

%% 1.6.1 ����һ��
true_value_SVR_test = value_SVR_test.*(max2-min2)+min2;
error_SVR_test = abs(true_value_SVR_test-t_test);
mean_error_SVR_test = mean(error_SVR_test);


%% 2 Kriging��ģ(mean_XDWC�ĵ�����ΪȨ��)
%% 2.3.1 ģ�Ͳ������ã���������������޸ģ���˵����
theta = 10; 
lob = 1e-1;
upb = 20;

%% 2.3.2 ����ģ�ͣ����캯��ģ��Ϊ��˹ģ�ͣ�
[dmodel, perf] = dacefit(P_train, T_train, @regpoly0, @corrgauss, theta, lob, upb);
%% 2.3.3 Ԥ��ģ�ͣ�YXΪ�۲�ֵ
[YX_test,MSE_test] = predictor(P_test, dmodel);
value_Kriging_test = YX_test;

%% 2.4 ����һ��
true_value_Kriging_test = value_Kriging_test.*(max2-min2)+min2;
XDWC_test = abs(true_value_Kriging_test-t_test);
error_Kriging_test = XDWC_test;
mean_error_Kriging_test = mean(XDWC_test);

%% 3 ���������(RBF)(test_error_1,test_error_2,test_error_3�ֱ�Ϊ���ֲ�ͬλ�û�������) 
%% 3.2 ���ݹ�һ��
%% ���ݹ�һ��
max1 = max(data_x');
min1 = min(data_x');
max2 = max(data_y');
min2 = min(data_y');
P_train = (p_train-min1)./(max1-min1);
P_train = P_train';
P_test = (p_test-min1)./(max1-min1);
P_test = P_test';
T_train = (t_train-min2)./(max2-min2);
T_train = T_train';
T_test = (t_test-min2)./(max2-min2);
T_test = T_test';

%% 3.3 ����RBFģ��
goal = 10e-20;%��������Ŀ��
spread = 1.0;%spread����sigmaֵ Ҳ��ƽ���ȡ�
MN = 100;%������Ԫ����
DF = 2;%ÿ�μӽ������������
net = newrb(P_train,T_train,goal,spread,MN,DF);

%% 3.4 ��Ϻ�Ԥ��
% ���Լ�
T_fit_test = sim(net,P_test);
value_RBF_test = T_fit_test';
%% ����һ��
true_value_RBF_test = value_RBF_test.*(max2-min2)+min2;
error_RBF_test = abs(t_test - true_value_RBF_test);
mean_error_RBF_test = mean(error_RBF_test);
%% 4 ��ϴ���ģ��
%% %���ֱ�Ϊerror_Kriging��error_RBF��error_SVR��
%% Ԥ��ֵ�ֱ�Ϊvalue_Kriging_test��value_RBF_test��value_SVR_test
w1_test = [];
w2_test = [];
w3_test = [];
value_hybrid_surrogate_test = [];
[m2,n2] = size(value_Kriging_test);
for i = 1:m2
    w1_test(i) = (1./error_Kriging_test(i))^2./((1./error_Kriging_test(i))^2+(1./error_RBF_test(i))^2+(1./error_SVR_test(i))^2);
    w2_test(i) = (1./error_RBF_test(i))^2./((1./error_Kriging_test(i))^2+(1./error_RBF_test(i))^2+(1./error_SVR_test(i))^2);
    w3_test(i) = (1./error_SVR_test(i))^2./((1./error_Kriging_test(i))^2+(1./error_RBF_test(i))^2+(1./error_SVR_test(i))^2);
    value_hybrid_surrogate_test(i) = w1_test(i)*true_value_Kriging_test(i)+w2_test(i)*true_value_RBF_test(i)+w3_test(i)*true_value_SVR_test(i);
end
value_hybrid_surrogate_test = value_hybrid_surrogate_test';
error_hybrid_surrogate_test = abs(t_test-value_hybrid_surrogate_test);
mean_error_hybrid_surrogate_test = mean(error_hybrid_surrogate_test);
%% ����MAE
mean1 = mean(abs(error_hybrid_surrogate_test./t_test));
mean2 = mean(abs(error_Kriging_test./t_test));
mean3 = mean(abs(error_RBF_test./t_test));
mean4 = mean(abs(error_SVR_test./t_test));
mean0 = [mean1;mean2;mean3;mean4];
