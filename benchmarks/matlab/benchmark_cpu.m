fprintf('\nloading...');
tmp = imread('./in/mitosis-5d0000.tif');
for i = 1:335
    filename = sprintf('./in/mitosis-5d%04d.tif', i);
    %fprintf('%s\n', filename);
    in = imread(filename);
    tmp = cat(3, tmp, in);
end
fprintf('\nloading complete\n');

for dim = 1:5
    n = dim;
    if n == 1
        input_nd = reshape(tmp, [1 22020096]);      %1d
    end
    if n == 2
        input_nd = reshape(tmp, [256 86016]);       %2d
    end
    if n == 3
        input_nd = reshape(tmp, [256 256 336]);     %3d
    end
    if n == 4
        input_nd = reshape(tmp, [256 256 2 168]);   %4d
    end
    if n == 5
        input_nd = reshape(tmp, [256 256 2 24 7]);   %5d
    end
    nsteps = 100;   
    
    fprintf('\nmax');
    if n == 1
        mask = uint8(zeros(1,22020096));
        [w, h] = size(mask);
        mask(1,h*0.05:h*0.8) = 255;
    end
    
    if n == 2
        mask = uint8(zeros(256,86016));
        [w, h] = size(mask);
        mask(w*0.05:w*.8,h*0.05:h*.8) = 255;
    end
    
    if n == 3
        mask = uint8(zeros(256,256,336));
        [w, h, d] = size(mask);
        mask(w*0.05:w*0.8,h*0.05:h*0.8,d*0.05:d*0.8) = 255;
    end
    
    if n == 4
        mask = uint8(zeros(256,256,2,168));
        [w, h, d, t] = size(mask);
        mask(w*0.05:w*0.8,h*0.05:h*0.8,d*0.05:d*0.8,t*0.05:t*0.8) = 255;
    end
    
    if n == 5
        mask = uint8(zeros(256,256,2,24,7));
        [w, h, d, t, t2] = size(mask);
        mask(w*0.05:w*0.8,h*0.05:h*0.8,d*0.05:d*0.8,t*0.05:t*0.8,t2*0.05:t2*0.8) = 255;
    end
    tic;
    for i = 1:nsteps
        result_max = max(input_nd,mask);
    end
    time_max = toc;
    tmp_max = reshape(result_max, [256 256 336]);
    fprintf('\nmax complete\n');
    
    fprintf('\nmean');
    strel_mean = create_3xcube_mean_es_el(n);
    tic;
    for i = 1:nsteps
        result_mean = convn(input_nd, strel_mean, 'same');
    end
    time_mean = toc;
    tmp_mean = reshape(result_mean, [256 256 336]);
    fprintf('\nmean complete\n');
    
    
    fprintf('\nsep dilate')
    strel_sep = cell(1,5);
    for i = 1:dim
        strel_dim = ones(1,dim);
        strel_dim(i) = 3;
        strel_sep{i} = ones(strel_dim);
    end
    
    tic;
    for i = 1:nsteps   
       dilate_sep_result_tmp = imdilate(input_nd, strel_sep{1});
       for j = 2:dim
           if (mod(j,2) == 0)
               dilate_sep_result = imdilate(dilate_sep_result_tmp, strel_sep{j});
           else
               dilate_sep_result_tmp = imdilate(dilate_sep_result, strel_sep{j});
           end
       end
    end
    time_dilate_sep = toc;
    if (mod(dim,2) == 1)
        dilate_sep_result = dilate_sep_result_tmp;
    end
    dilate_sep_result = reshape(dilate_sep_result, [256 256 336]);
    saveImages(dilate_sep_result, strcat(num2str(n),'/sep dilate'));
    fprintf('\nsep dilate complete')
    
    fprintf('\ndilate(hypercube)')
    if n == 1
        my_str_el = [1, 1, 1];
    else
        my_str_el = create_3xcube_es_el(n);
    end
    tic;
    for i = 1:nsteps
        result_dilate_hypercube = imdilate(input_nd, my_str_el);
    end
    time_dilate_hypercube = toc;
    tmp_dilate_hypercube = reshape(result_dilate_hypercube, [256 256 336]);
    saveImages(tmp_dilate_hypercube, strcat(num2str(n),'/dilate hypercube'));
    fprintf('\ndilate(hypercube) complete\n');
    
    fprintf('\ndilate(cross)')
    strel_cross = create_3xcross_es_el(n);
    tic;
    for i = 1:nsteps
        result_dilate_cross = imdilate(input_nd, strel_cross);
    end
    time_dilate_cross = toc;
    tmp_dilate_cross = reshape(result_dilate_cross, [256 256 336]);
    saveImages(tmp_dilate_cross, strcat(num2str(n),'/dilate cross'));
    fprintf('\ndilate(cross) complete\n');
    
    fprintf('\nnegative');
    tic;
    for i = 1:nsteps
        result_negative = imcomplement(input_nd);
    end
    time_negative = toc;
    tmp_negative = reshape(result_negative, [256 256 336]);
    saveImages(tmp_negative, strcat(num2str(n),'/negative'));
    fprintf('\nnegative complete\n');
    
    fprintf('\ngraythresh');
    thresh = 109;
    threshf = thresh/255;
    tic;
    for i = 1:nsteps
        if n < 4
            result_graythresh = imbinarize(input_nd, threshf);
        else
            result_graythresh(input_nd>=thresh) = 255;
            result_graythresh(input_nd<thresh) = 0;
        end
    end
    time_graythresh = toc;
    tmp_graythresh = im2uint8(result_graythresh);
    tmp_graythresh = reshape(tmp_graythresh, [256 256 336]);
    saveImages(tmp_graythresh, strcat(num2str(n),'/thresh'));
    fprintf('\ngraythresh complete\n');
    
    fprintf('\ncopy');
    tic;
    for i = 1:nsteps
        result_copy = input_nd;
    end
    time_copy = toc;
    tmp_copy = reshape(result_copy, [256 256 336]);
    fprintf('\ncopy complete\n');
    %{
    fprintf('\ndeep copy');
    tic;  
    d = [];
    for i = 1:n
        d = cat(1, d, size(input_nd, n));
    end
    for i = 1:nsteps
        result_deepcopy = zeros(d);
        result_deepcopy = feval('class',input_nd);
        p = properties(p);
        for j = 1:length(p)
            result_deepcopy.(p{i}) = tmp.(p{i});
        end
    end
    time_deepcopy = toc;
    whos result_deepcopy;
    tmp_deepcopy = reshape(result_deepcopy, [256 256 336]);
    fprintf('\ndeep copy complete\n');
    %}
    
    fprintf('\ncopy + atribuicao');
    tic;  
    %{
    d = [];
    for i = 1:n
        d = cat(1, d, size(input_nd, n));
    end
    tamanho = 1;
    for i = 1:n
        tamanho = tamanho * d(i);
    end
    %}
    for i = 1:nsteps
        result_deepcopy = input_nd;
        result_deepcopy(1) = -1;
    end
    time_copy_atrib = toc;
    tmp_deepcopy = reshape(result_deepcopy, [256 256 336]);
    fprintf('\ncopy + atribuicao complete\n');
    
    tic;
    for i = 1:n
        %for j = 1:tamanho
            result_deepcopy(1) = -1;
        %end
    end
    time_atrib = toc;
    time_copy_final = time_copy_atrib - time_atrib; 
    
    %{
    fprintf('\ncopy CPU-GPU');
    tic;
    for i = 1:nsteps
        result_copy_cpu_gpu = gpuArray(input_nd);
    end
    time_copy_cpu_gpu = toc;
    fprintf('\ncopy CPU-GPU complete\n');
    
    fprintf('\ncopy GPU-CPU');
    tic;
    for i = 1:nsteps
        result_copy_gpu_cpu = gather(result_copy_cpu_gpu);
    end
    time_copy_gpu_cpu = toc;
    fprintf('\ncopy GPU-CPU complete\n');
    tmp_copy_gpu_cpu = reshape(result_copy_gpu_cpu, [256 256 336]);
    %}
    filename_time_cpu = sprintf('./out/operations_time_%dd.txt', n);
    file_time_cpu = fopen(filename_time_cpu, 'w');
    fprintf(file_time_cpu, 'Times of execution in CPU:\n');
    fprintf(file_time_cpu, '\ncopy                   = %f', time_copy);
    %fprintf(file_time_cpu, '\ndeepcopy                   = %f', time_copy_atrib);
    %fprintf(file_time_cpu, '\ncopy cpu to gpu        = %f', time_copy_cpu_gpu);
    %fprintf(file_time_cpu, '\ncopy gpu to cpu        = %f', time_copy_gpu_cpu);
    fprintf(file_time_cpu, '\nmax                    = %f', time_max);
    fprintf(file_time_cpu, '\ndilate(cross)          = %f', time_dilate_cross);
    fprintf(file_time_cpu, '\ndilate(hypercube)      = %f', time_dilate_hypercube);
    fprintf(file_time_cpu, '\ndilate sep cube        = %f', time_dilate_sep);
    fprintf(file_time_cpu, '\ngraythresh             = %f', time_graythresh);
    fprintf(file_time_cpu, '\nmean                   = %f', time_mean);
    fprintf(file_time_cpu, '\nnegative               = %f', time_negative);
    fprintf(file_time_cpu, '\n\ntime_copy_atrib      = %f', time_copy_atrib);
    fprintf(file_time_cpu, '\ntime_atrib           = %f', time_atrib);
    fprintf(file_time_cpu, '\ntime_copy_final      = %f', time_copy_final);
    fclose(file_time_cpu);
end
%{
fprintf('\nsaving...');
for i = 1:336
    outfilename = sprintf('./out_cpu/out_mean/out%04d.tif', i-1);
    out = tmp_mean(:,:,i);
    imwrite(uint8(out), outfilename);
    
    outfilename = sprintf('./out_cpu/out_dilate_sep/out%04d.tif', i-1);
    out = dilate_sep_result(:,:,i);
    imwrite(uint8(out), outfilename);
    
    outfilename = sprintf('./out_cpu/out_dilate_hypercube/out%04d.tif', i-1);
    out = result_dilate_hypercube(:,:,i);
    imwrite(uint8(out), outfilename);
    
    outfilename = sprintf('./out_cpu/out_dilate_cross/out%04d.tif', i-1);
    out = tmp_dilate_cross(:,:,i);
    imwrite(uint8(out), outfilename);
    
    outfilename = sprintf('./out_cpu/out_negative/out%04d.tif', i-1);
    out = tmp_negative(:,:,i);
    imwrite(uint8(out), outfilename);
    
    outfilename = sprintf('./out_cpu/out_graythresh/out%04d.tif', i-1);
    out = tmp_graythresh(:,:,i);
    imwrite(uint8(out), outfilename);
    
    outfilename = sprintf('./out_cpu/out_copy/out%04d.tif', i-1);
    out = tmp_copy(:,:,i);
    imwrite(uint8(out), outfilename);
    
    outfilename = sprintf('./out_cpu/out_deepcopy/out%04d.tif', i-1);
    out = tmp_deepcopy(:,:,i);
    imwrite(uint8(out), outfilename);
    
    
    outfilename = sprintf('./out_copy_GPU-CPU/out%04d.tif', i-1); out =
    tmp_copy_gpu_cpu(:,:,i); imwrite(uint8(out), outfilename);
    
    
end
    %}
fprintf('\nsave complete\n');