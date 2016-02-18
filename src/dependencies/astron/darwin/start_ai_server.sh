cd ../../../
export PYTHONPATH=dependencies/mac/lib:$PYTHONPATH
ppython -m toontown.ai.ServiceStart --base-channel 401000000\
 --max-channels 999999 --stateserver 4002 --astron-ip 127.0.0.1:7100\
  --eventlogger-ip 127.0.0.1:7198\
   --district-name "Nutty Falls"

