function x = saveImages(img, name)
for i = 1:336
    outfilename = sprintf(strcat('out/',name,'/out%04d.tif'), i-1);
    %fprintf('%s\n', outfilename);
    saveImg = img(:,:,i);
    imwrite(saveImg, outfilename);
end
end