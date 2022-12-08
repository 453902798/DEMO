function [chrom,fitness] = GA(LB, UB, num, x, y, w1, w2, w3)
    %% 基础参数
    N = num;  %种群内个体数目
    N_chrom = 2; %染色体节点数，也即变量个数。
    iter = 50; %迭代次数
    mut = 0.2;  %突变概率
    acr = 0.2; %交叉概率
    best = 1;
    chrom_range = [LB,UB]';%每个节点的值的区间
    chrom = zeros(N, N_chrom);%存放染色体的矩阵
    chrom_best_out = zeros(2, iter);%存放每一代的最优适应度
    fitness = zeros(N, 1);%存放染色体的适应度
    fitness_ave = zeros(1, iter);%存放每一代的平均适应度
    fitness_best = zeros(1, iter);%存放每一代的最优适应度
    chrom_best = zeros(1, N_chrom+1);%存放当前代的最优染色体与适应度
    %% 建立预测误差预测模型
    [~,~,dmodel] = kriging(x,y);
    [~,~,net] = RBF(x,y);
    [~,~,model] = SVR(x,y);

    %% 初始化，这只是用于生成第一代个体，并计算其适应度函数
    chrom = Initialize(N, N_chrom, chrom_range); %初始化染色体
    fitness = CalFitness(chrom, N, dmodel, net, model, w1, w2, w3); %计算适应度
    chrom_best = FindBest(chrom, fitness, N_chrom); %寻找最优染色体
    chrom_best_out(:,1) = chrom_best(1:2)';
    fitness_best(1) = chrom_best(end); %将当前最优存入矩阵当中
    fitness_ave(1) = CalAveFitness(fitness); %将当前平均适应度存入矩阵当中
    %% 用于生成以下其余各代，一共迭代多少步就一共有多少代
    for t = 2:iter
        chrom = MutChrom(chrom, mut, N, N_chrom, chrom_range, t, iter); %变异
        chrom = AcrChrom(chrom, acr, N, N_chrom); %交叉
        fitness = CalFitness(chrom, N, dmodel, net, model, w1, w2, w3); %计算适应度
        chrom_best_temp = FindBest(chrom, fitness, N_chrom); %寻找最优染色体
        if chrom_best_temp(end)<chrom_best(end) %替换掉当前储存的最优
            chrom_best = chrom_best_temp;
        end
        %%替换掉最劣
        [chrom, fitness] = ReplaceWorse(chrom, chrom_best, fitness);
        chrom_best_out(:,t) = chrom_best(1:2)';
        fitness_best(t) = chrom_best(end); %将当前最优存入矩阵当中
        fitness_ave(t) = CalAveFitness(fitness); %将当前平均适应度存入矩阵当中
    end
end

