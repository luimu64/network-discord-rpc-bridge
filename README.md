# Network Discord RPC bridge
I made this for bridging the Discord rich presence from my qemu/kvm machine to host where my discord was 
running but in theory it should work with any windows and linux machine.
It works by first creating pipe for discord to `\\.\pipe\discord-ipc-0` in windows(guest) then 
communicating with the socat receiver in linux(host) where socat writes it into `/run/user/1000/discord-ipc-0`.

# Requirements
You need socat in your host machine and either the prepackaged exe from releases or this script and python intepreter in your guest.

# Running
1. Do one of these in host:
</br>a) Run `socat TCP-LISTEN:<port>,reuseaddr,fork,max-children=1 UNIX-CONNECT:/run/user/1000/discord-ipc-0` in your host
</br>b) Edit and run the rpc script from this repo in your host
3. Edit config.cfg according to your ip address and port
4. Do one of these in guest:
</br>a) Run the connect.py with python intepreter
</br>b) Run the connect.exe from releases
4. Launch your game.


