x = [];
for i =1:4
    n = 50;%��������
    st = 0;
    en = 1;%��Χ
    mu = (en - st)/n;
    for i = 1:n
        x1(1,i) = st+mu*(i-1)+rand(1)*mu;
    end
    x1 = round(x1,2);
    R = randperm(n);
    %�﷨��ʽ��R = randperm(n)
    %�������ܣ�������1:n����������У����н���洢����������
    %EX: ���� randperm(3)  ��� 3 1 2
    [~,pos] = sort(R);
    x1(1,:) = x1(1,pos);
    %�����а��յ�2��������±��Ӧ
    x = [x;x1];
end
