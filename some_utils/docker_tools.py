import tempfile
import time
import logging
import subprocess

import requests

logger = logging.getLogger(__name__)


def process_with_dump(cmd, silenced=False):
    logger.info(cmd)
    if not silenced:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        for line in proc.stdout:
            print(line.decode('utf8').rstrip())
    else:
        cmd += ' > /dev/null 2>&1'
        print(cmd)
        proc = subprocess.Popen(cmd, shell=True)
    proc.wait()


def execute_script_on_container(container_id, script_rows):
    with tempfile.NamedTemporaryFile('wt') as temp:
        temp.write('\n'.join(script_rows))
        temp.flush()
        process_with_dump(f"docker exec -i {container_id} bash < {temp.name}")

    import os
    print(f"{os.path.exists(temp.name)=}")


def get_container_ids():
    res = subprocess.check_output("docker ps", shell=True)
    ids = []

    for enne, line in enumerate(res.decode('utf8').split('\n')):
        if not enne or not line.strip():   # headers
            continue
        ids.append(line.split(' ')[0])
    return ids


def kill_all_container():
    logger.info("kill all container")
    for id_container in get_container_ids():
        cmd = f"docker kill {id_container}"
        process_with_dump(cmd, silenced=True)


def wait_progress_end(progress_endpoint):
    while 1:
        res = requests.get(progress_endpoint).json()
        if res:
            if res[-1] == 'end':
                break
            logger.info('... wait')
        time.sleep(2.5)


def delete_images(initial_name='*'):
    res = subprocess.check_output("docker images", shell=True)
    for enne, line in enumerate(res.decode('utf8').split('\n')):
        if enne == 0:  # headers
            continue
        line = line.strip()
        if initial_name == '*' or line.startswith(initial_name):
            vals = [chunk for chunk in line.split(' ') if chunk.strip()]
            if vals:
                cmd = f"docker rmi {vals[2]}"
                logger.info(cmd)
                subprocess.check_output(cmd, shell=True)


def delete_old_containers():
    cmd = "docker rm $(docker ps -aq)"
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        logger.info("no old containers")


if __name__ == '__main__':
    delete_images('<none>')
