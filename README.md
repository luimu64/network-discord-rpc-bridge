# Network Discord RPC bridge
I made this for bridging the Discord rich presence from my qemu/kvm machine to host where my discord was 
running but in theory it should work with any windows and linux machine.
It works by first creating pipe for discord to `\\.\pipe\discord-ipc-0` in windows(guest) then 
communicating with the socat receiver in linux(host) where socat writes it into `/run/user/1000/discord-ipc-0`.

# Requirements
You need socat in your host machine and either the prebuilt binary from releases or this script and python intepreter in your guest.

# Running
1. First run </br>`socat TCP-LISTEN:<port>,reuseaddr,fork,max-children=1 UNIX-CONNECT:/run/user/1000/discord-ipc-0` in your host.
2. Edit config.cfg according to your ip address and port
3. Do one of these:
  a) Run the connect.py in your guest with python intepreter
  b) Run the exe from releases
4. Launch your game.


