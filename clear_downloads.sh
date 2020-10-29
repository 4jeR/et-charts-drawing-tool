#!/bin/bash
cd web/downloads/
    rm -rf *
    mkdir codes

    cd codes
        touch .gitkeep
        cd ..
    mkdir images
    cd images
        touch .gitkeep
        cd ..
    cd ../../
exit