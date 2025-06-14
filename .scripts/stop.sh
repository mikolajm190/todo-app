#!/bin/bash

echo "🧹 Stopping containers and removing pod..."
podman pod stop todopod
podman pod rm todopod
