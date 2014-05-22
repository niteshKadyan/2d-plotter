#filename: compile.sh
#adjust path to source code

 
PKG_CONFIG_PATH=/usr/lib/pkgconfig:${PKG_CONFIG_PATH}
export PKG_CONFIG_PATH
 
#adjust name of output file and code file
for i in *.cpp; do
    echo "compiling $i"
    g++ -ggdb `pkg-config --cflags opencv` -o `basename $i .cpp` $i `pkg-config --libs opencv`;
done
