from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from configs.constants import WORK_DIR_DOCKER, TIMEOUT_DOCKER


def getDockerCommandLineExecutor():
    docker=DockerCommandLineCodeExecutor(
        work_dir=WORK_DIR_DOCKER,
        timeout=TIMEOUT_DOCKER
    )

    return docker


async def start_docker_container(docker):
    print("Starting Docker Container")
    await docker.start()
    print("Docker Container Started")


async def stop_docker_container(docker):
    print("Stopping Docker Container")
    await docker.stop()
    print("Docker Container Stopped")