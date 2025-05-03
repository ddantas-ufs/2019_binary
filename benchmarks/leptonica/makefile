

BENCHMARK_LEPTONICA_NAME    = benchmark_leptonica

ROOTPATH           = .
OUTPUT_ROOTPATH    = $(ROOTPATH)
OUTPUT_BINPATH     = $(OUTPUT_ROOTPATH)/bin

CC               = g++
COMPILER_FLAGS   = -g -pg
FPIC             = -fPIC 

LEPTONICA_PATH        = /home/ddantas/script/lib/leptonica
LEPTONICA_INCLUDEPATH = $(LEPTONICA_PATH)/include/leptonica
LEPTONICA_LIBPATH     = $(LEPTONICA_PATH)/lib
LEPTONICA_INCLUDEDIR  = -I $(LEPTONICA_INCLUDEPATH)
LEPTONICA_LIBDIR      = -L $(LEPTONICA_LIBPATH)
LEPTONICA_LIBRARIES   = -lleptonica

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(LEPTONICA_LIBPATH)


LINUXAMD64_DIRS_LIBS =  $(INCLUDE_DIR) \
                        $(LEPTONICA_INCLUDEDIR) \
                        $(LEPTONICA_LIBDIR) \
                        $(LEPTONICA_LIBRARIES) \




LINUXAMD64_DEMO_BENCHMARK_LEPTONICA = $(CC) $(COMPILER_FLAGS) \
                        -o $(OUTPUT_BINPATH)/demo_$(BENCHMARK_LEPTONICA_NAME) \
                         ./$(BENCHMARK_LEPTONICA_NAME)_new.cpp ./timer.cpp \
                         $(LINUXAMD64_DIRS_LIBS) \



demobenchmark:
	$(LINUXAMD64_DEMO_BENCHMARK_LEPTONICA)


rundemobenchmark:
	cd $(OUTPUT_BINPATH); ./demo_$(BENCHMARK_LEPTONICA_NAME) ../../../mosaic2d/saida2.tif 200 /tmp

