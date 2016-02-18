cd ../../../
export PYTHONPATH=dependencies/mac/lib:$PYTHONPATH
ppython -m toontown.uberdog.ServiceStart --base-channel 1000000 --max-channels 999999 --stateserver 4002 --astron-ip 127.0.0.1:7100 --eventlogger-ip 127.0.0.1:7198
