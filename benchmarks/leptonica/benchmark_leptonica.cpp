
// atoi
#include <stdlib.h>

// printf
#include <stdio.h>

// strlen
#include <cstring>

// leptonica
#include <allheaders.h>

// TimerStart, ElapsedTime
#include "timer.h"


#if defined(WIN32) || defined(_WIN32) 
  #define DIRSEP "\\"
  #define MKDIR  "md"
#else 
  #define DIRSEP "/" 
  #define MKDIR  "mkdir -p"
#endif


void saveResult(PIX* out, char* outPath, const char* filename)
{
  char* outString   = (char*) "%s%sout_leptonica_%s.tif";
  char* outFilename = (char*) malloc(strlen(outPath) + 255);

  sprintf(outFilename, outString, outPath, DIRSEP, filename);

  printf("Writing output to: %s\n", outFilename); 
  
  pixWrite(outFilename, out, IFF_TIFF);
}  


int main (int argc, char *argv[])
{
  char* usage = (char*) "\n\
    This program reads an image file and saves \n\
the results after benchmarking some operations. Usage is as follows:\n\
\n\
benchmark_leptonica <input file> <steps> <output folder>\n\
\n\
";

  int nargs = 3;

  if (argc < nargs + 1)
  {
    printf("%s", usage);
    exit(1);
  }
  char *inFilename = argv[1]; // name of the input file
  int nSteps = atoi(argv[2]); // number of tests 
  char *outPath = argv[3]; // name of the output folder


  PIX* img = pixRead(inFilename);
  int w = pixGetWidth(img);
  int h = pixGetHeight(img);
  int d;
  pixGetDimensions(img, NULL, NULL, &d);
  printf("Image dimensions: (%d, %d)\n", w, h);
  printf("Image depth: %d bpp\n", d);
  
  saveResult(img, outPath, "gray");

  // Create mask
  PIX* mask_gray = pixCopy(NULL, img);
  int x0 = 0.05 * w;
  int x1 = 0.8 * w;
  int y0 = 0.05 * h;
  int y1 = 0.8 * h;
  int val;
  for (int x = 0; x < w; x++)
  {
    for (int y = 0; y < h; y++)
    {
      if (x >= x0 and x <= x1 and y >= y0 and y <= y1)
      {
	val = 255;
      }
      else
      {
        val = 0;
      }
      pixSetPixel(mask_gray, x, y, val);
    }
  }
  saveResult(mask_gray, outPath, "mask_gray");  


  //resetMorphBoundaryCondition(SYMMETRIC_MORPH_BC);

  // Threshold
  int thresh = 109;
  PIX* img_bw = pixThresholdToBinary(img, thresh);
  saveResult(img_bw, outPath, "bw");

  PIX* mask_bw = pixThresholdToBinary(mask_gray, thresh);
  saveResult(mask_bw, outPath, "mask_bw");


  // image to save generic binary result
  PIX* result_bw;
  
  // image to save invert binary result
  PIX* invert_bw;

  // Not
  // https://github.com/DanBloomberg/leptonica/blob/master/src/pix3.c
  invert_bw = pixInvert(NULL, img_bw); // allocates memory space
  pixInvert(invert_bw, img_bw);        // uses previously allocated space
  saveResult(result_bw, outPath, "invert_bw");

  
  // Max
  // https://github.com/DanBloomberg/leptonica/blob/master/src/pix3.c
  result_bw = pixOr(NULL, mask_bw, img_bw);  // allocates memory space
  pixOr(result_bw, mask_bw, img_bw);   // uses previously allocated space
  saveResult(result_bw, outPath, "max_bw");
    

  // Copy
  pixCopy(result_bw, img_bw);
  saveResult(result_bw, outPath, "copy_bw");

  
  // Unpack
  // https://github.com/DanBloomberg/leptonica/blob/master/src/pixconv.c
  PIX* result_gray = NULL;
  int depth = 8;
  int invert = 0;
  result_gray = pixUnpackBinary(img_bw, depth, invert);
  saveResult(result_gray, outPath, "unpack_gray");
  pixDestroy(&result_gray);

  // SEL create
  // https://github.com/DanBloomberg/leptonica/blob/master/src/sel1.c
  // selCreateBrick(), with input (h, w, cy, cx, val)
  SEL* se_0     = selCreateBrick(1, 3, 0, 1, SEL_HIT); // horizontal, 1x3
  SEL* se_1     = selCreateBrick(3, 1, 1, 0, SEL_HIT); // vertical,   3x1
  SEL* se_cube  = selCreateBrick(3, 3, 1, 1, SEL_HIT);
  SEL* se_cross = selCreateBrick(3, 3, 1, 1, SEL_HIT);
  selSetElement(se_cross, 0, 0, SEL_DONT_CARE);
  selSetElement(se_cross, 0, 2, SEL_DONT_CARE);
  selSetElement(se_cross, 2, 2, SEL_DONT_CARE);
  selSetElement(se_cross, 2, 0, SEL_DONT_CARE);
  


  // image to save partial dilation result
  PIX* result_bw0 = pixCopy(NULL, img_bw);

  
  // Dilate by cross rasterop
  TimerStart();
  pixDilate(result_bw, invert_bw, se_cross);
  printf("Time spent on %8d         Dilate Cross Rasterop:         %s\n", nSteps, getTimeElapsedInSeconds());
  saveResult(result_bw,  outPath, "dilate_cross_rasterop");
  
  // Dilate by cube rasterop
  TimerStart();
  pixDilate(result_bw, invert_bw, se_cube);
  printf("Time spent on %8d         Dilate Cube Rasterop:          %s\n", nSteps, getTimeElapsedInSeconds());
  saveResult(result_bw,  outPath, "dilate_cube_rasterop");
  
  // Dilate by cube separated rasterop
  TimerStart();
  pixDilate(result_bw0, invert_bw,  se_0);
  pixDilate(result_bw,  result_bw0, se_1);
  printf("Time spent on %8d         Dilate Sep Cube Rasterop:      %s\n", nSteps, getTimeElapsedInSeconds());
  saveResult(result_bw,  outPath, "dilate_sepcube_rasterop");
  
  // Dilate by cube separated DWA
  PIX* input_border_bw   = pixAddBorder(invert_bw, 32, 0);
  PIX* result_border_bw0 = pixCopy(NULL, input_border_bw);
  PIX* result_border_bw  = pixCopy(NULL, input_border_bw);

  pixDestroy(&result_bw);
  pixDestroy(&result_bw0);
  
  TimerStart();
  input_border_bw   = pixAddBorder(invert_bw, 32, 0);
  pixFMorphopGen_1(result_border_bw0, input_border_bw,   L_MORPH_DILATE, "sel_3h");
  pixFMorphopGen_1(result_border_bw,  result_border_bw0, L_MORPH_DILATE, "sel_3v");
  result_bw = pixRemoveBorder(result_border_bw, 32);
  printf("Time spent on %8d         Dilate Sep Cube DWA:           %s\n", nSteps, getTimeElapsedInSeconds());

  result_bw0 = pixRemoveBorder(result_border_bw0, 32);
  saveResult(result_bw0, outPath, "dilate_sepcube_dwa_partial");
  saveResult(result_bw,  outPath, "dilate_sepcube_dwa_final");

  // Dilate by cube separated DWA v2
  pixDestroy(&result_bw);
  pixDestroy(&result_bw0);

  result_bw = pixCopy(NULL, invert_bw);
  
  TimerStart();
  pixDilateBrickDwa(result_bw, invert_bw, 3, 3);
  printf("Time spent on %8d         Dilate Sep Cube DWA v2:        %s\n", nSteps, getTimeElapsedInSeconds());
  saveResult(result_bw,  outPath, "dilate_sepcube_dwa_v2_final");

  

  return 0;
}
