# Network Discord RPC bridge
I made this for bridging the Discord rich presence from my qemu/kvm machine to host where my discord was 
running but in theory it should work with any windows and linux machine.
It works by first creating pipe for discord to `\\.\pipe\discord-ipc-0` in windows(guest) then 
communicating with the socat receiver in linux(host) where socat writes it into `/run/user/1000/discord-ipc-0`.

# Requirements
You need socat in your host machine and this script and python intepreter in your guest machine.

# Running
1. First run </br>`socat TCP-LISTEN:<port>,reuseaddr UNIX-CONNECT:/run/user/1000/discord-ipc-0` in your host.
2. Then Run the connect.py in your guest </br>`python connect.py <your host ipv4 address> <port your used earlier>`.
3. Launch your game.
4. Enjoy.


