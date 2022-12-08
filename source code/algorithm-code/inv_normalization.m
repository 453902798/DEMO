function y = inv_normalization(max, min, x)
    y = x.*(max-min)'+min';
end

