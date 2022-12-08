function [chrom,fitness] = GA(LB, UB, num, x, y, w1, w2, w3)
    %% ��������
    N = num;  %��Ⱥ�ڸ�����Ŀ
    N_chrom = 2; %Ⱦɫ��ڵ�����Ҳ������������
    iter = 50; %��������
    mut = 0.2;  %ͻ�����
    acr = 0.2; %�������
    best = 1;
    chrom_range = [LB,UB]';%ÿ���ڵ��ֵ������
    chrom = zeros(N, N_chrom);%���Ⱦɫ��ľ���
    chrom_best_out = zeros(2, iter);%���ÿһ����������Ӧ��
    fitness = zeros(N, 1);%���Ⱦɫ�����Ӧ��
    fitness_ave = zeros(1, iter);%���ÿһ����ƽ����Ӧ��
    fitness_best = zeros(1, iter);%���ÿһ����������Ӧ��
    chrom_best = zeros(1, N_chrom+1);%��ŵ�ǰ��������Ⱦɫ������Ӧ��
    %% ����Ԥ�����Ԥ��ģ��
    [~,~,dmodel] = kriging(x,y);
    [~,~,net] = RBF(x,y);
    [~,~,model] = SVR(x,y);

    %% ��ʼ������ֻ���������ɵ�һ�����壬����������Ӧ�Ⱥ���
    chrom = Initialize(N, N_chrom, chrom_range); %��ʼ��Ⱦɫ��
    fitness = CalFitness(chrom, N, dmodel, net, model, w1, w2, w3); %������Ӧ��
    chrom_best = FindBest(chrom, fitness, N_chrom); %Ѱ������Ⱦɫ��
    chrom_best_out(:,1) = chrom_best(1:2)';
    fitness_best(1) = chrom_best(end); %����ǰ���Ŵ��������
    fitness_ave(1) = CalAveFitness(fitness); %����ǰƽ����Ӧ�ȴ��������
    %% ���������������������һ���������ٲ���һ���ж��ٴ�
    for t = 2:iter
        chrom = MutChrom(chrom, mut, N, N_chrom, chrom_range, t, iter); %����
        chrom = AcrChrom(chrom, acr, N, N_chrom); %����
        fitness = CalFitness(chrom, N, dmodel, net, model, w1, w2, w3); %������Ӧ��
        chrom_best_temp = FindBest(chrom, fitness, N_chrom); %Ѱ������Ⱦɫ��
        if chrom_best_temp(end)<chrom_best(end) %�滻����ǰ���������
            chrom_best = chrom_best_temp;
        end
        %%�滻������
        [chrom, fitness] = ReplaceWorse(chrom, chrom_best, fitness);
        chrom_best_out(:,t) = chrom_best(1:2)';
        fitness_best(t) = chrom_best(end); %����ǰ���Ŵ��������
        fitness_ave(t) = CalAveFitness(fitness); %����ǰƽ����Ӧ�ȴ��������
    end
end

