function x_vir = generation_uniform(LB, UB, num, d)
    if d == 1
        x1 = LB(1):(UB(1)-LB(1))/(num-1):UB(1);R1 = randperm(num);[~,pos1] = sort(R1);x1(1,:) = x1(1,pos1);  
        x_vir = x1;
    elseif d == 2
        x1 = LB(1):(UB(1)-LB(1))/(num-1):UB(1);R1 = randperm(num);[~,pos1] = sort(R1);x1(1,:) = x1(1,pos1);  
        x2 = LB(2):(UB(2)-LB(2))/(num-1):UB(2);R2 = randperm(num);[~,pos2] = sort(R2);x2(1,:) = x2(1,pos2); 
        x_vir = [x1;x2];
    elseif d == 3
        x1 = LB(1):(UB(1)-LB(1))/(num-1):UB(1);R1 = randperm(num);[~,pos1] = sort(R1);x1(1,:) = x1(1,pos1);  
        x2 = LB(2):(UB(2)-LB(2))/(num-1):UB(2);R2 = randperm(num);[~,pos2] = sort(R2);x2(1,:) = x2(1,pos2); 
        x3 = LB(3):(UB(3)-LB(3))/(num-1):UB(3);R3 = randperm(num);[~,pos3] = sort(R3);x3(1,:) = x3(1,pos3);
        x_vir = [x1;x2;x3];
    elseif d == 4
        x1 = LB(1):(UB(1)-LB(1))/(num-1):UB(1);R1 = randperm(num);[~,pos1] = sort(R1);x1(1,:) = x1(1,pos1);  
        x2 = LB(2):(UB(2)-LB(2))/(num-1):UB(2);R2 = randperm(num);[~,pos2] = sort(R2);x2(1,:) = x2(1,pos2); 
        x3 = LB(3):(UB(3)-LB(3))/(num-1):UB(3);R3 = randperm(num);[~,pos3] = sort(R3);x3(1,:) = x3(1,pos3);
        x4 = LB(4):(UB(4)-LB(4))/(num-1):UB(4);R4 = randperm(num);[~,pos4] = sort(R4);x4(1,:) = x4(1,pos4); 
        x_vir = [x1;x2;x3;x4];
    elseif d == 5
        x1 = LB(1):(UB(1)-LB(1))/(num-1):UB(1);R1 = randperm(num);[~,pos1] = sort(R1);x1(1,:) = x1(1,pos1);  
        x2 = LB(2):(UB(2)-LB(2))/(num-1):UB(2);R2 = randperm(num);[~,pos2] = sort(R2);x2(1,:) = x2(1,pos2); 
        x3 = LB(3):(UB(3)-LB(3))/(num-1):UB(3);R3 = randperm(num);[~,pos3] = sort(R3);x3(1,:) = x3(1,pos3);
        x4 = LB(4):(UB(4)-LB(4))/(num-1):UB(4);R4 = randperm(num);[~,pos4] = sort(R4);x4(1,:) = x4(1,pos4); 
        x5 = LB(5):(UB(5)-LB(5))/(num-1):UB(5);R5 = randperm(num);[~,pos5] = sort(R5);x5(1,:) = x5(1,pos5);
        x_vir = [x1;x2;x3;x4;x5];
    elseif d == 6
        x1 = LB(1):(UB(1)-LB(1))/(num-1):UB(1);R1 = randperm(num);[~,pos1] = sort(R1);x1(1,:) = x1(1,pos1);  
        x2 = LB(2):(UB(2)-LB(2))/(num-1):UB(2);R2 = randperm(num);[~,pos2] = sort(R2);x2(1,:) = x2(1,pos2); 
        x3 = LB(3):(UB(3)-LB(3))/(num-1):UB(3);R3 = randperm(num);[~,pos3] = sort(R3);x3(1,:) = x3(1,pos3);
        x4 = LB(4):(UB(4)-LB(4))/(num-1):UB(4);R4 = randperm(num);[~,pos4] = sort(R4);x4(1,:) = x4(1,pos4); 
        x5 = LB(5):(UB(5)-LB(5))/(num-1):UB(5);R5 = randperm(num);[~,pos5] = sort(R5);x5(1,:) = x5(1,pos5); 
        x6 = LB(6):(UB(6)-LB(6))/(num-1):UB(6);R6 = randperm(num);[~,pos6] = sort(R6);x6(1,:) = x6(1,pos6);
        x_vir = [x1;x2;x3;x4;x5;x6];
    elseif d == 7
        x1 = LB(1):(UB(1)-LB(1))/(num-1):UB(1);R1 = randperm(num);[~,pos1] = sort(R1);x1(1,:) = x1(1,pos1);  
        x2 = LB(2):(UB(2)-LB(2))/(num-1):UB(2);R2 = randperm(num);[~,pos2] = sort(R2);x2(1,:) = x2(1,pos2); 
        x3 = LB(3):(UB(3)-LB(3))/(num-1):UB(3);R3 = randperm(num);[~,pos3] = sort(R3);x3(1,:) = x3(1,pos3);
        x4 = LB(4):(UB(4)-LB(4))/(num-1):UB(4);R4 = randperm(num);[~,pos4] = sort(R4);x4(1,:) = x4(1,pos4); 
        x5 = LB(5):(UB(5)-LB(5))/(num-1):UB(5);R5 = randperm(num);[~,pos5] = sort(R5);x5(1,:) = x5(1,pos5); 
        x6 = LB(6):(UB(6)-LB(6))/(num-1):UB(6);R6 = randperm(num);[~,pos6] = sort(R6);x6(1,:) = x6(1,pos6);
        x7 = LB(7):(UB(7)-LB(7))/(num-1):UB(7);R7 = randperm(num);[~,pos7] = sort(R7);x7(1,:) = x7(1,pos7);
        x_vir = [x1;x2;x3;x4;x5;x6;x7];
    elseif d == 8
        x1 = LB(1):(UB(1)-LB(1))/(num-1):UB(1);R1 = randperm(num);[~,pos1] = sort(R1);x1(1,:) = x1(1,pos1);  
        x2 = LB(2):(UB(2)-LB(2))/(num-1):UB(2);R2 = randperm(num);[~,pos2] = sort(R2);x2(1,:) = x2(1,pos2); 
        x3 = LB(3):(UB(3)-LB(3))/(num-1):UB(3);R3 = randperm(num);[~,pos3] = sort(R3);x3(1,:) = x3(1,pos3);
        x4 = LB(4):(UB(4)-LB(4))/(num-1):UB(4);R4 = randperm(num);[~,pos4] = sort(R4);x4(1,:) = x4(1,pos4); 
        x5 = LB(5):(UB(5)-LB(5))/(num-1):UB(5);R5 = randperm(num);[~,pos5] = sort(R5);x5(1,:) = x5(1,pos5); 
        x6 = LB(6):(UB(6)-LB(6))/(num-1):UB(6);R6 = randperm(num);[~,pos6] = sort(R6);x6(1,:) = x6(1,pos6);
        x7 = LB(7):(UB(7)-LB(7))/(num-1):UB(7);R7 = randperm(num);[~,pos7] = sort(R7);x7(1,:) = x7(1,pos7);
        x8 = LB(8):(UB(8)-LB(8))/(num-1):UB(8);
        x_vir = [x1;x2;x3;x4;x5;x6;x7;x8];
end

