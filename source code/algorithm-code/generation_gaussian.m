function x_vir = generation_gaussian(LB, UB, num, d)
    if d == 1
        x1 = mgd(num,1,UB(1)-LB(1)/2,UB(1)-LB(1)/6)';R1 = randperm(num); [~,pos1] = sort(R1); x1(1,:) = x1(1,pos1); 
        x_vir = x1;
    elseif d == 2
        x1 = mgd(num,1,UB(1)-LB(1)/2,UB(1)-LB(1)/6)';R1 = randperm(num); [~,pos1] = sort(R1); x1(1,:) = x1(1,pos1); 
        x2 = mgd(num,1,UB(2)-LB(2)/2,UB(2)-LB(2)/6)';R2 = randperm(num); [~,pos2] = sort(R2); x2(1,:) = x2(1,pos2); 
        x_vir = [x1;x2];
    elseif d == 3
        x1 = mgd(num,1,UB(1)-LB(1)/2,UB(1)-LB(1)/6)';R1 = randperm(num); [~,pos1] = sort(R1); x1(1,:) = x1(1,pos1); 
        x2 = mgd(num,1,UB(2)-LB(2)/2,UB(2)-LB(2)/6)';R2 = randperm(num); [~,pos2] = sort(R2); x2(1,:) = x2(1,pos2); 
        x3 = mgd(num,1,UB(3)-LB(3)/2,UB(3)-LB(3)/6)';R3 = randperm(num); [~,pos3] = sort(R3); x3(1,:) = x3(1,pos3); 
        x_vir = [x1;x2;x3];
    elseif d == 4
        x1 = mgd(num,1,UB(1)-LB(1)/2,UB(1)-LB(1)/6)';R1 = randperm(num); [~,pos1] = sort(R1); x1(1,:) = x1(1,pos1); 
        x2 = mgd(num,1,UB(2)-LB(2)/2,UB(2)-LB(2)/6)';R2 = randperm(num); [~,pos2] = sort(R2); x2(1,:) = x2(1,pos2); 
        x3 = mgd(num,1,UB(3)-LB(3)/2,UB(3)-LB(3)/6)';R3 = randperm(num); [~,pos3] = sort(R3); x3(1,:) = x3(1,pos3); 
        x4 = mgd(num,1,UB(4)-LB(4)/2,UB(4)-LB(4)/6)';R4 = randperm(num); [~,pos4] = sort(R4); x4(1,:) = x4(1,pos4); 
        x_vir = [x1;x2;x3;x4];
    elseif d == 5
        x1 = mgd(num,1,UB(1)-LB(1)/2,UB(1)-LB(1)/6)';R1 = randperm(num); [~,pos1] = sort(R1); x1(1,:) = x1(1,pos1); 
        x2 = mgd(num,1,UB(2)-LB(2)/2,UB(2)-LB(2)/6)';R2 = randperm(num); [~,pos2] = sort(R2); x2(1,:) = x2(1,pos2); 
        x3 = mgd(num,1,UB(3)-LB(3)/2,UB(3)-LB(3)/6)';R3 = randperm(num); [~,pos3] = sort(R3); x3(1,:) = x3(1,pos3); 
        x4 = mgd(num,1,UB(4)-LB(4)/2,UB(4)-LB(4)/6)';R4 = randperm(num); [~,pos4] = sort(R4); x4(1,:) = x4(1,pos4); 
        x5 = mgd(num,1,UB(5)-LB(5)/2,UB(5)-LB(5)/6)';R5 = randperm(num); [~,pos5] = sort(R5); x5(1,:) = x5(1,pos5);
        x_vir = [x1;x2;x3;x4;x5];
    elseif d == 6
        x1 = mgd(num,1,UB(1)-LB(1)/2,UB(1)-LB(1)/6)';R1 = randperm(num); [~,pos1] = sort(R1); x1(1,:) = x1(1,pos1); 
        x2 = mgd(num,1,UB(2)-LB(2)/2,UB(2)-LB(2)/6)';R2 = randperm(num); [~,pos2] = sort(R2); x2(1,:) = x2(1,pos2); 
        x3 = mgd(num,1,UB(3)-LB(3)/2,UB(3)-LB(3)/6)';R3 = randperm(num); [~,pos3] = sort(R3); x3(1,:) = x3(1,pos3); 
        x4 = mgd(num,1,UB(4)-LB(4)/2,UB(4)-LB(4)/6)';R4 = randperm(num); [~,pos4] = sort(R4); x4(1,:) = x4(1,pos4); 
        x5 = mgd(num,1,UB(5)-LB(5)/2,UB(5)-LB(5)/6)';R5 = randperm(num); [~,pos5] = sort(R5); x5(1,:) = x5(1,pos5);
        x6 = mgd(num,1,UB(6)-LB(6)/2,UB(6)-LB(6)/6)';
        x_vir = [x1;x2;x3;x4;x5;x6];
end

