# -*- coding: utf-8 -*-
from derex.runner.project import Project
from types import SimpleNamespace

import docker
import pytest


def test_ensure_volumes_present(mocker):
    from derex.runner.docker_utils import ensure_volumes_present
    from derex.runner.docker_utils import VOLUMES

    client = mocker.patch("derex.runner.docker_utils.client")

    client.volumes.list.return_value = []
    ensure_volumes_present()
    assert client.volumes.create.call_count > 3
    client.volumes.create.assert_any_call("derex_mysql")
    client.volumes.create.assert_any_call("derex_mongodb")

    client.volumes.create.reset_mock()
    client.volumes.list.return_value = [SimpleNamespace(name=name) for name in VOLUMES]
    ensure_volumes_present()
    client.volumes.create.assert_not_called()


def test_check_services(mocker):
    from derex.runner.docker_utils import check_services

    api_client = mocker.patch("derex.runner.docker_utils.client.api")

    container_info = {"State": {"Status": "running", "Health": {"Status": "healthy"}}}
    api_client.inspect_container.return_value = container_info
    assert check_services(["mysql"])

    api_client.inspect_container.side_effect = docker.errors.NotFound(
        "mysql container not found"
    )
    assert check_services(["mysql"]) is False


def test_wait_for_service(mocker):
    from derex.runner.docker_utils import wait_for_service

    # Test that a RuntimeError is raised if the container doesn't
    # exists
    with pytest.raises(RuntimeError):
        wait_for_service("service", 1)

    container_info = {"State": {"Status": "running", "Health": {"Status": "healthy"}}}
    api_client = mocker.patch("derex.runner.docker_utils.client.api")
    api_client.inspect_container.return_value = container_info

    # Test that the result is successfull when the container
    # is running or restarting and healthy
    result = wait_for_service("service", 1)
    api_client.inspect_container.assert_called_with("service")
    assert result == 0

    container_info["State"]["Status"] = "restarting"
    result = wait_for_service("service", 1)
    assert result == 0

    # Test that a RuntimeError is raised if the container status is
    # exited
    container_info["State"]["Status"] = "exited"
    with pytest.raises(RuntimeError):
        wait_for_service("service", 1)

    # Test that a TimeoutError is raised if the container status is
    # unhealthy
    container_info["State"]["Status"] = "running"
    container_info["State"]["Health"]["Status"] = "unhealthy"
    with pytest.raises(TimeoutError):
        wait_for_service("service", 1)

    # Test that a NotImplementedError is raised if the container doesn't
    # define an healtcheck
    container_info["State"]["Health"] = None
    with pytest.raises(NotImplementedError):
        wait_for_service("service", 1)


def test_get_final_image(mocker, minimal_project):
    from derex.runner.docker_utils import image_exists

    mocker.patch(
        "derex.runner.docker_utils.docker.APIClient",
        return_value=mocker.Mock(
            images=mocker.Mock(return_value=DOCKER_DAEMON_IMAGES_RESPONSE)
        ),
    )
    with minimal_project:
        project = Project()
        image_exists(project)


DOCKER_DAEMON_IMAGES_RESPONSE = [
    {
        "Containers": -1,
        "Created": 1568757938,
        "Id": "sha256:e7d35cfa3056cf59688f75d3d5e3b7ac2c38a00ef64058937cf8bcfa078ff81f",
        "Labels": None,
        "ParentId": "",
        "RepoDigests": [
            "derex/openedx-ironwood@sha256:ced32894ea157b1fad9d894343059666492a928714d769ae3dd4eab09de99e59"
        ],
        "RepoTags": None,
        "SharedSize": -1,
        "Size": 1665836550,
        "VirtualSize": 1665836550,
    }
]
