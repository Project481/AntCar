function   [xoff,yoff,Radius,params] = fitCircle(x,y)
%
%   [xc yx R a] = fitCircle(x,y)
% 
   x=x(:); %put in col
   y=y(:);
   params=[x y ones(size(x))]\(-(x.^2+y.^2));
   xoff = -.5*params(1);
   yoff = -.5*params(2);
   Radius  =  sqrt((params(1)^2+params(2)^2)/4-params(3));