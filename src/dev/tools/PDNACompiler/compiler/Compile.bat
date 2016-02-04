@echo off

title Toontown Empire PDNA Compiler

echo Enter .DNA file name.

cd ../../../../
"dependencies/panda/python/ppython.exe" -m dev.tools.PDNACompiler.compiler.compile.py