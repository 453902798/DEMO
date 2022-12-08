function [LB,UB] = Gaussian(x,y,bias)%(a=100,b=CL)
    c1 = sqrt(-(x(:,2)-x(:,1)).^2./log(y(:,2)/100)/2);
    c2 = sqrt(-(x(:,3)-x(:,1)).^2./log(y(:,3)/100)/2);
    LB = -sqrt(-(2*c1.^2)*log(bias/100))+x(:,1);
    UB = sqrt(-(2*c2.^2)*log(bias/100))+x(:,1);
    
    m = size(x,1);
    for i =1:m
        if LB(i)<0
            LB(i)=0;
        end
    end
    
end

