#!/bin/bash

ssh -i cs224w.pem -N -L 8888:localhost:8888 ubuntu@18.232.165.122

ssh -i cs224w.pem ubuntu@18.232.165.122