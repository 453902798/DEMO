x = [];
for i =1:4
    n = 50;%采样个数
    st = 0;
    en = 1;%范围
    mu = (en - st)/n;
    for i = 1:n
        x1(1,i) = st+mu*(i-1)+rand(1)*mu;
    end
    x1 = round(x1,2);
    R = randperm(n);
    %语法格式：R = randperm(n)
    %函数功能：将数字1:n进行随机排列，排列结果存储在行向量内
    %EX: 输入 randperm(3)  输出 3 1 2
    [~,pos] = sort(R);
    x1(1,:) = x1(1,pos);
    %所有行按照第2行排序的下标对应
    x = [x;x1];
end
