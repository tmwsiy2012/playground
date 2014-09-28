import subprocess

server_executable='./jre1.7.0_67/bin/java -Xmx1024M -Xms1024M -jar ./minecraft_server.1.8.jar nogui'
proc = subprocess.Popen(server_executable,
                        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
tmp_str = proc.stdout.readline()
while 'Done' not in tmp_str:
    tmp_str = proc.stdout.readline()

'''
while True:
    proc.stdin.write('world\n')
    proc.stdin.flush()
    proc_read = proc.stdout.readline()
    if proc_read:
        print proc_read
'''